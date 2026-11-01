// Minimal, synthetic-only component boundary for the approved pinned LEAN source.
// Actual FillModel / CoinbaseFeeModel / SecurityPortfolioManager observations
// are returned without replacing them with expected fills or rounded fees.
// This is not a brokerage adapter, native recovery system or trading algorithm.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text.Json;
using NodaTime;
using QuantConnect;
using QuantConnect.Data;
using QuantConnect.Data.Market;
using QuantConnect.Interfaces;
using QuantConnect.Orders;
using QuantConnect.Orders.Fees;
using QuantConnect.Orders.Fills;
using QuantConnect.Securities;
using QuantConnect.Securities.Crypto;

internal static class SyntheticLeanProbe
{
    private static readonly CultureInfo Inv = CultureInfo.InvariantCulture;

    private static string Text(JsonElement item, string key) => item.GetProperty(key).GetString();
    private static decimal Number(JsonElement item, string key) => decimal.Parse(Text(item, key), Inv);
    private static string Dec(decimal value) => value.ToString("0.############################", Inv);
    private static long Time(JsonElement item, string key) => item.GetProperty(key).GetInt64();

    private static DateTime Utc(long ns)
    {
        if (ns % 100 != 0) throw new NotSupportedException("unsupported_precision: DateTime requires exact 100ns ticks");
        return DateTime.UnixEpoch.AddTicks(ns / 100);
    }

    private sealed class ConfigProvider : ISubscriptionDataConfigProvider
    {
        private readonly SubscriptionDataConfig _config;
        public ConfigProvider(SubscriptionDataConfig config) { _config = config; }
        public List<SubscriptionDataConfig> GetSubscriptionDataConfigs(Symbol symbol = null, bool includeInternalConfigs = false)
            => symbol == null || symbol == _config.Symbol ? new List<SubscriptionDataConfig> { _config } : new List<SubscriptionDataConfig>();
    }

    private sealed class State
    {
        public readonly JsonElement Fixture;
        public readonly TimeKeeper Clock;
        public readonly Symbol Symbol;
        public readonly Crypto Security;
        public readonly SecurityPortfolioManager Portfolio;
        public readonly ConfigProvider Configs;
        public readonly Dictionary<string, Order> Pending = new Dictionary<string, Order>();
        public readonly List<object> NativeEvents = new List<object>();
        public readonly List<object> Fills = new List<object>();
        public readonly List<object> GuardEvents = new List<object>();
        public readonly List<string> Rejected = new List<string>();
        public readonly List<object> Snapshots = new List<object>();
        public readonly List<object> Quotes = new List<object>();
        public readonly List<object> Decisions = new List<object>();
        public readonly Dictionary<string, bool> Maker = new Dictionary<string, bool>();
        public bool ConversionAvailable;
        public string ConversionValue;
        public long Now;
        private int _effectOrdinal;

        public State(JsonElement fixture)
        {
            Fixture = fixture;
            var instrument = fixture.GetProperty("instrument");
            var events = fixture.GetProperty("events").EnumerateArray().ToArray();
            var initialTime = events.Length == 0 ? 0 : events.Min(x => Time(x, "available_ns"));
            Clock = new TimeKeeper(Utc(initialTime), DateTimeZone.Utc);
            Symbol = Symbol.Create(Text(instrument, "base") + Text(instrument, "quote"), SecurityType.Crypto, Market.Coinbase);
            var securities = new SecurityManager(Clock);
            var transactions = new SecurityTransactionManager(null, securities);
            Portfolio = new SecurityPortfolioManager(securities, transactions, new AlgorithmSettings());
            foreach (var amount in fixture.GetProperty("initial_cash").EnumerateObject())
            {
                var quantity = decimal.Parse(amount.Value.GetString(), Inv);
                if (Portfolio.CashBook.ContainsKey(amount.Name)) Portfolio.CashBook[amount.Name].SetAmount(quantity);
                else Portfolio.CashBook.Add(amount.Name, quantity, 0m);
            }
            var config = new SubscriptionDataConfig(typeof(Tick), Symbol, Resolution.Tick,
                DateTimeZone.Utc, DateTimeZone.Utc, false, false, false, tickType: TickType.Quote,
                dataNormalizationMode: DataNormalizationMode.Raw);
            Configs = new ConfigProvider(config);
            var properties = new SymbolProperties("invented technical instrument", Text(instrument, "quote"),
                1m, Number(instrument, "price_tick"), Number(instrument, "quantity_step"), "SYNUSD");
            Security = new Crypto(SecurityExchangeHours.AlwaysOpen(DateTimeZone.Utc),
                Portfolio.CashBook[Text(instrument, "quote")], Portfolio.CashBook[Text(instrument, "base")],
                config, properties, Portfolio.CashBook, RegisteredSecurityDataTypesProvider.Null);
            Security.SetFeeModel(new CoinbaseFeeModel(Number(instrument, "maker_fee"), Number(instrument, "taker_fee")));
            securities.Add(Symbol, Security);
        }

        public void At(long ns) { Now = ns; Clock.SetUtcDateTime(Utc(ns)); }

        public Dictionary<string, decimal> Reserved()
        {
            var result = Portfolio.CashBook.ToDictionary(x => x.Key, _ => 0m);
            foreach (var order in Pending.Values)
            {
                if (order.Direction == OrderDirection.Sell) result[Security.BaseCurrency.Symbol] += order.AbsoluteQuantity;
                else
                {
                    var price = order is LimitOrder limit ? limit.LimitPrice : Security.AskPrice;
                    result[Security.QuoteCurrency.Symbol] += order.AbsoluteQuantity * price
                        + Security.FeeModel.GetOrderFee(new OrderFeeParameters(Security, order)).Value.Amount;
                }
            }
            return result;
        }

        public Dictionary<string, string> Balances() => Portfolio.CashBook.ToDictionary(x => x.Key, x => Dec(x.Value.Amount));

        public void Snapshot(string source)
        {
            var reserved = Reserved();
            Snapshots.Add(new {
                at = Now, source,
                balances = Balances(),
                reserved = reserved.ToDictionary(x => x.Key, x => Dec(x.Value)),
                free = Portfolio.CashBook.ToDictionary(x => x.Key, x => Dec(x.Value.Amount - reserved[x.Key])),
                native_position = Dec(Security.Holdings.Quantity),
                reservation_origin = "harness pending-command policy; no native brokerage reservation claim"
            });
        }

        public void FillPending()
        {
            foreach (var entry in Pending.ToArray())
            {
                var order = entry.Value;
                var outputs = Security.FillModel.Fill(new FillModelParameters(Security, order, Configs,
                    TimeSpan.FromHours(1), new Dictionary<Order, Security> { { order, Security } })).ToList();
                foreach (var output in outputs)
                {
                    // The component FillModel does not allocate broker order/fill IDs.
                    // Keep its actual IDs and separately assign a bridge observation ID.
                    NativeEvents.Add(new {
                        command_id = entry.Key, at = Now, native_order_id = output.OrderId,
                        native_event_id = output.Id, status = output.Status.ToString(),
                        signed_fill_quantity = Dec(output.FillQuantity), price = Dec(output.FillPrice),
                        message = output.Message
                    });
                    if (output.FillQuantity == 0) continue;
                    output.OrderFee = Security.FeeModel.GetOrderFee(new OrderFeeParameters(Security, order));
                    Portfolio.ProcessFills(new List<OrderEvent> { output });
                    Fills.Add(new {
                        venue = "LEAN-COMPONENT-SYNTHETIC", fill_id = "bridge-observation-" + (++_effectOrdinal),
                        command_id = entry.Key, instrument_id = Text(Fixture.GetProperty("instrument"), "id"),
                        side = output.Direction == OrderDirection.Buy ? "BUY" : "SELL",
                        quantity = Dec(output.AbsoluteFillQuantity), price = Dec(output.FillPrice),
                        fee = Dec(output.OrderFee.Value.Amount), fee_currency = output.OrderFee.Value.Currency,
                        liquidity_role = Maker[entry.Key] ? "maker" : "taker",
                        native_order_id = output.OrderId, native_event_id = output.Id,
                        liquidity_role_origin = "submitted order properties; native event has no maker/taker field",
                        effect_identity_origin = "bridge observation ordinal; not a broker fill ID",
                        native_model = Security.FillModel.GetType().FullName,
                        native_fee_model = Security.FeeModel.GetType().FullName
                    });
                    order.Status = output.Status;
                    if (output.Status == OrderStatus.Filled || output.Status == OrderStatus.Canceled) Pending.Remove(entry.Key);
                }
            }
        }

        public void Event(JsonElement item)
        {
            var kind = Text(item, "kind");
            if (kind == "quote")
            {
                var tick = new Tick(Utc(Time(item, "event_ns")), Symbol,
                    Number(item, "bid_size"), Number(item, "bid"), Number(item, "ask_size"), Number(item, "ask"));
                Security.SetMarketPrice(tick);
                Security.BaseCurrency.CurrencyConversion.ConversionRate = Security.Price;
                Quotes.Add(new { at = Now, bid = Dec(tick.BidPrice), ask = Dec(tick.AskPrice),
                    bid_size = Dec(tick.BidSize), ask_size = Dec(tick.AskSize), event_id = Text(item, "event_id") });
                FillPending();
            }
            else if (kind == "conversion")
            {
                Portfolio.CashBook["USDT"].CurrencyConversion.ConversionRate = Number(item, "rate");
                ConversionAvailable = true;
                ConversionValue = Dec(Portfolio.CashBook.ConvertToAccountCurrency(new CashAmount(Portfolio.CashBook["USDT"].Amount, "USDT")).Amount);
                GuardEvents.Add(new { at = Now, kind = "conversion_available", value = ConversionValue,
                    availability_origin = "harness envelope guard", arithmetic_origin = "native CashBook conversion" });
            }
            else if (kind == "bar_open")
            {
                Decisions.Add(new { at = Now, decision = "BLOCK", bar_id = (string)null });
                GuardEvents.Add(new { at = Now, kind = "provisional_bar_excluded_by_harness" });
            }
            else if (kind == "bar_close" || kind == "bar_revision")
            {
                var value = Number(item, "close");
                Security.SetMarketPrice(new TradeBar(Utc(Time(item, "event_ns")), Symbol, value, value, value, value, 0m, TimeSpan.Zero));
                Decisions.Add(new { at = Now, decision = "OBSERVE", bar_id = Text(item, "bar_id"), close = Dec(Security.Price) });
                GuardEvents.Add(new { at = Now, kind = "closed_bar_admitted_by_harness", native_cache_price = Dec(Security.Price) });
            }
            else if (kind == "external")
            {
                GuardEvents.Add(new { at = Now, kind = "external_available_without_market_effect", event_ns = Time(item, "event_ns") });
            }
            else throw new NotSupportedException("event_kind_requires_unimplemented_model:" + kind);
            Snapshot(Text(item, "event_id"));
        }

        public void Command(JsonElement item)
        {
            var cid = Text(item, "command_id");
            var kind = Text(item, "kind");
            if (kind != "market" && kind != "limit") throw new NotSupportedException("command_kind:" + kind);
            var instrument = Fixture.GetProperty("instrument");
            var qty = Number(item, "quantity");
            var buy = Text(item, "side") == "BUY";
            var signed = buy ? qty : -qty;
            var props = new CoinbaseOrderProperties { PostOnly = item.TryGetProperty("post_only", out var post) && post.GetBoolean() };
            Order order = kind == "market"
                ? new MarketOrder(Symbol, signed, Utc(Time(item, "available_ns")), cid, props)
                : new LimitOrder(Symbol, signed, Number(item, "price"), Utc(Time(item, "available_ns")), cid, props);
            var maker = kind == "limit" && (props.PostOnly || (buy ? Number(item, "price") < Security.AskPrice : Number(item, "price") > Security.BidPrice));
            var prospectivePrice = kind == "limit" ? Number(item, "price") : buy ? Security.AskPrice : Security.BidPrice;
            var reserved = Reserved();
            string reason = null;
            if (qty <= 0 || qty % Number(instrument, "quantity_step") != 0) reason = "invalid_quantity_step";
            else if (qty * prospectivePrice < Number(instrument, "minimum_notional")) reason = "below_minimum_notional";
            else if (buy && qty * prospectivePrice + Security.FeeModel.GetOrderFee(new OrderFeeParameters(Security, order)).Value.Amount > Security.QuoteCurrency.Amount - reserved[Security.QuoteCurrency.Symbol]) reason = "insufficient_free_cash";
            else if (!buy && qty > Security.BaseCurrency.Amount - reserved[Security.BaseCurrency.Symbol]) reason = "insufficient_free_inventory";
            if (reason != null)
            {
                Rejected.Add(cid);
                GuardEvents.Add(new { at = Now, kind = "rejected", command_id = cid, reason,
                    origin = "harness boundary guard, not native brokerage rejection" });
            }
            else
            {
                order.Status = OrderStatus.Submitted;
                Maker[cid] = maker;
                Pending.Add(cid, order);
                FillPending();
            }
            Snapshot(cid);
        }

        public object Result()
        {
            var reserved = Reserved();
            return new {
                schema = "bot-trader.synthetic-engine-observation.v1", synthetic = true,
                engine = "LEAN", source_commit = "22404ea28b8d3f3c9eb74d6ed9f0444426f8e417",
                case_id = Text(Fixture, "case_id"), execution_status = "component_observations_emitted",
                route = "native Common FillModel, configured CoinbaseFeeModel and SecurityPortfolioManager; harness schedule/admission/reservations",
                native_brokerage_executed = false, decisions = Decisions, fills = Fills, native_events = NativeEvents,
                observed_quotes = Quotes, guard_events = GuardEvents, snapshots = Snapshots,
                rejected_command_ids = Rejected, balances = Balances(),
                free = Portfolio.CashBook.ToDictionary(x => x.Key, x => Dec(x.Value.Amount - reserved[x.Key])),
                reserved = reserved.ToDictionary(x => x.Key, x => Dec(x.Value)),
                native_position = Dec(Security.Holdings.Quantity),
                open_command_ids = Pending.Keys.ToArray(),
                conversion = new { before = (string)null, after = ConversionAvailable ? ConversionValue : null },
                limitations = new [] {
                    "component route, not default Launcher or complete brokerage lifecycle",
                    "admission, availability and free/reserved fields are harness guards",
                    "native event IDs remain native defaults; bridge IDs are observation identities only",
                    "no L2 consumption, IOC, duplicate transport or recovery implementation",
                    "native fees preserved without result-fitted rounding"
                }
            };
        }
    }

    public static int Main(string[] args)
    {
        try
        {
            if (args.Length != 2) throw new ArgumentException("usage: lean_probe <frozen-engine-cases.json> <case-id>");
            using var document = JsonDocument.Parse(File.ReadAllText(args[0]));
            var fixture = document.RootElement.GetProperty("functional").EnumerateArray().Single(x => Text(x, "case_id") == args[1]);
            if (args[1] != "E1-causality" && args[1] != "E2-accounting" && args[1] != "E3-L1")
                throw new NotSupportedException("case_requires_unimplemented_boundary:" + args[1]);
            var state = new State(fixture);
            var arrivals = new List<(long At, int Ordinal, bool IsCommand, JsonElement Value)>();
            int ordinal = 0;
            foreach (var item in fixture.GetProperty("events").EnumerateArray())
                arrivals.Add((Time(item, "available_ns"), ordinal++, false, item));
            foreach (var item in fixture.GetProperty("commands").EnumerateArray())
                arrivals.Add((checked(Time(item, "available_ns") + Time(fixture, "latency_ns")), ordinal++, true, item));
            foreach (var arrival in arrivals.OrderBy(x => x.At).ThenBy(x => x.Ordinal))
            {
                state.At(arrival.At);
                if (arrival.IsCommand) state.Command(arrival.Value); else state.Event(arrival.Value);
            }
            Console.WriteLine(JsonSerializer.Serialize(state.Result()));
            return 0;
        }
        catch (Exception exc)
        {
            Console.WriteLine(JsonSerializer.Serialize(new { engine = "LEAN", synthetic = true,
                execution_status = exc is NotSupportedException ? "unsupported" : "error",
                exception_type = exc.GetType().FullName, message = exc.Message, detail = exc.ToString() }));
            return 1;
        }
    }
}
