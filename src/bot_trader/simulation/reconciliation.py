"""Bounded posting accounting and an independent synthetic batch oracle.

Neither component matches orders or invents executions. The native adapter maps
platform SYNTH-USD to SYN-USD.SIM, whose base balance key is SYN and quote balance
key is actual USD. This module supports only that declared technical cash scope.
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal, Inexact, localcontext
from typing import Any, Literal

from bot_trader.core.events import canonical_bytes, content_hash, exact_ns

ZERO = Decimal(0)
TERMINAL = frozenset({"FILLED", "CANCELED", "DENIED", "REJECTED", "EXPIRED"})


def _decimal(value: object, *, positive: bool = False, signed: bool = False) -> Decimal:
    if not isinstance(value, str):
        raise ValueError("Accounting amounts require explicit decimal strings.")
    number = Decimal(value)
    if not number.is_finite() or (not signed and number < ZERO):
        raise ValueError("Accounting amounts must be finite with the declared sign.")
    if positive and number <= ZERO:
        raise ValueError("Fill price and quantity must be positive.")
    return number


def _text(number: Decimal) -> str:
    if not number:
        return "0"
    value = format(number, "f")
    return value.rstrip("0").rstrip(".") if "." in value else value


def _identity(value: object) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= 128:
        raise ValueError("A persistent accounting identity is required.")
    return value


@dataclass(frozen=True)
class Posting:
    fill_id: str
    order_id: str
    signal_id: str
    quote_id: str
    side: Literal["buy", "sell"]
    quantity: Decimal
    price: Decimal
    fee_usd: Decimal
    cash_delta_usd: Decimal
    inventory_delta: Decimal
    at_ns: int
    ts_event_ns: int
    ts_init_ns: int
    source_hash: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "fill_id": self.fill_id,
            "order_id": self.order_id,
            "signal_id": self.signal_id,
            "quote_id": self.quote_id,
            "side": self.side,
            "quantity": _text(self.quantity),
            "price": _text(self.price),
            "fee_usd": _text(self.fee_usd),
            "cash_delta_usd": _text(self.cash_delta_usd),
            "inventory_delta": _text(self.inventory_delta),
            "at_ns": self.at_ns,
            "ts_event_ns": self.ts_event_ns,
            "ts_init_ns": self.ts_init_ns,
            "source_hash": self.source_hash,
        }


class PostingLedger:
    """Append-only fill effects for one bounded technical cash account.

    Identical redelivery has no effect. A conflicting fill identity, short sale,
    overspend or invalid amount leaves the previous state unchanged. Reservations
    are reconciled from native state, never invented as posting-ledger fills.
    """

    def __init__(self, initial_cash_usd: Decimal | str) -> None:
        self.initial_cash_usd = _decimal(str(initial_cash_usd))
        self.cash_usd = self.initial_cash_usd
        self.inventory = ZERO
        self.fees_usd = ZERO
        self._postings: tuple[Posting, ...] = ()
        self._identities: dict[str, str] = {}

    @property
    def postings(self) -> tuple[Posting, ...]:
        return self._postings

    def apply(self, fill: dict[str, Any]) -> bool:
        fill_id = _identity(fill["id"])
        fingerprint = content_hash(fill)
        prior = self._identities.get(fill_id)
        if prior is not None:
            if fingerprint != prior:
                raise ValueError("Conflicting duplicate fill identity.")
            return False
        if len(self._postings) >= 1000:
            raise ValueError("The bounded technical posting limit is exhausted.")
        if fill["currency"] != "USD" or fill["side"] not in ("buy", "sell"):
            raise ValueError("Only USD spot buy/sell posting effects are supported.")
        side: Literal["buy", "sell"] = "buy" if fill["side"] == "buy" else "sell"
        quantity = _decimal(fill["quantity"], positive=True)
        price = _decimal(fill["price"], positive=True)
        fee = _decimal(fill["fee"])
        at, event, init = (exact_ns(fill[key]) for key in ("at", "ts_event", "ts_init"))
        if at < max(event, init) or init < event:
            raise ValueError("Posting clocks are incompatible.")
        if self._postings and at < self._postings[-1].at_ns:
            raise ValueError("Out-of-order posting is not silently reordered.")
        with localcontext() as context:
            context.prec = 80
            context.traps[Inexact] = True
            notional = price * quantity
            cash_delta = -notional - fee if side == "buy" else notional - fee
            inventory_delta = quantity if side == "buy" else -quantity
            cash = self.cash_usd + cash_delta
            inventory = self.inventory + inventory_delta
            fees = self.fees_usd + fee
            if cash < ZERO or inventory < ZERO:
                raise ValueError("A native fill would overspend cash or create a short position.")
        posting = Posting(
            fill_id=fill_id,
            order_id=_identity(fill["order_id"]),
            signal_id=_identity(fill["signal_id"]),
            quote_id=_identity(fill["quote_id"]),
            side=side,
            quantity=quantity,
            price=price,
            fee_usd=fee,
            cash_delta_usd=cash_delta,
            inventory_delta=inventory_delta,
            at_ns=at,
            ts_event_ns=event,
            ts_init_ns=init,
            source_hash=fingerprint,
        )
        self.cash_usd, self.inventory, self.fees_usd = cash, inventory, fees
        self._postings += (posting,)
        self._identities[fill_id] = fingerprint
        return True

    def state(self) -> dict[str, Any]:
        return {
            "initial_cash_usd": _text(self.initial_cash_usd),
            "cash_usd": _text(self.cash_usd),
            "inventory": _text(self.inventory),
            "fees_usd": _text(self.fees_usd),
            "postings": [posting.as_dict() for posting in self.postings],
        }


def reconcile(request: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Compare raw-fill batch arithmetic, posting effects and native state.

    Duplicate raw rows are deduplicated by identity plus full payload. No fill is
    inferred from an order status. Unknown, open, partial or cancellation-pending
    native state cannot pass reconciliation even when cash totals happen to agree.
    All pricing checks concern the declared synthetic quote/depth assumptions.
    """
    if (
        request.get("mode") != "technical"
        or request.get("synthetic") is not True
        or request.get("partition") != "development"
        or request.get("instrument") != "SYNTH-USD"
    ):
        raise ValueError("Only the synthetic development cash-account contract is admitted.")
    initial = _decimal(request["initial_cash_usd"])
    rate = _decimal(request["policy"]["fee_rate"])
    if rate > 1:
        raise ValueError("The declared technical fee rate is unsupported.")
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: object = None) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    check(
        "native_completed_without_errors",
        result.get("status") == "completed" and not result.get("errors"),
    )
    check(
        "synthetic_scope",
        result.get("synthetic") is True and result.get("financial_validation") is False,
    )
    check("request_identity", result.get("request_hash") == content_hash(request))
    commands: dict[str, dict[str, Any]] = {}
    for command in request["commands"]:
        cid = _identity(command["id"])
        if command["kind"] not in {"market", "cancel"}:
            raise ValueError("Unknown command kind in the bounded accounting contract.")
        if cid in commands and canonical_bytes(commands[cid]) != canonical_bytes(command):
            raise ValueError("Conflicting duplicate command identity in reconciliation input.")
        commands[cid] = command
    markets = {key: value for key, value in commands.items() if value["kind"] == "market"}
    quotes = {_identity(quote["id"]): quote for quote in request["quotes"]}
    if len(quotes) != len(request["quotes"]):
        raise ValueError("Quote identities must already be unique after normalization.")
    for command in commands.values():
        if command["quote_id"] not in quotes:
            raise ValueError("Command refers to an unknown quote.")
        if command["kind"] == "cancel" and command["target"] not in markets:
            raise ValueError("Cancellation refers to an unknown market command.")

    raw_fills = result.get("fills", [])
    if not isinstance(raw_fills, list) or len(raw_fills) > 1000:
        raise ValueError("The technical oracle accepts at most 1000 fill rows.")
    # This independent batch path deliberately does not read posting-ledger effects.
    unique: dict[str, dict[str, Any]] = {}
    duplicates = 0
    for fill in raw_fills:
        fid = _identity(fill["id"])
        if fid in unique:
            if canonical_bytes(unique[fid]) != canonical_bytes(fill):
                raise ValueError("Conflicting duplicate fill in raw oracle input.")
            duplicates += 1
        else:
            unique[fid] = fill
    filled_by_order: dict[str, Decimal] = {}
    consumed: dict[tuple[str, str, Decimal], Decimal] = {}
    with localcontext() as context:
        context.prec = 80
        context.traps[Inexact] = True
        gross_buy = gross_sell = bought = sold = fees = ZERO
        prefix_cash, prefix_quantity = initial, ZERO
        for fid, fill in unique.items():
            quantity = _decimal(fill["quantity"], positive=True)
            price = _decimal(fill["price"], positive=True)
            fee = _decimal(fill["fee"])
            side = fill["side"]
            if side not in ("buy", "sell") or fill["currency"] != "USD":
                raise ValueError("Raw fills require USD fees and explicit buy/sell side.")
            order_id, quote_id = fill["order_id"], fill["quote_id"]
            if order_id not in markets or quote_id not in quotes:
                raise ValueError("Fill refers to an unknown market command or quote.")
            command, quote = markets[order_id], quotes[quote_id]
            check(
                "fill_lineage:" + fid,
                command["quote_id"] == quote_id
                and command["signal_id"] == fill["signal_id"]
                and command["side"] == side,
            )
            at, event, init = (exact_ns(fill[key]) for key in ("at", "ts_event", "ts_init"))
            decision = exact_ns(command["decision_ns"])
            submitted = exact_ns(command["submitted_ns"])
            available = exact_ns(quote["available_ns"])
            quote_event = exact_ns(quote["event_ns"])
            quote_init = exact_ns(quote["engine_init_ns"])
            check(
                "causal_bound_quote:" + fid,
                submitted > decision
                and quote_event >= decision
                and available >= decision
                and submitted == quote_init
                and at == quote_init
                and at >= max(submitted, available, event, init)
                and init >= event >= submitted
                and at - quote_event <= request["policy"]["max_quote_age_ns"],
            )
            levels = quote["asks"] if side == "buy" else quote["bids"]
            capacities = {_decimal(p, positive=True): _decimal(q, positive=True) for p, q in levels}
            key = (quote_id, side, price)
            consumed[key] = consumed.get(key, ZERO) + quantity
            check(
                "price_and_depth_capacity:" + fid,
                price in capacities and consumed[key] <= capacities.get(price, ZERO),
            )
            raw_fee = quantity * price * rate
            with localcontext() as monetary_rounding:
                monetary_rounding.traps[Inexact] = False
                expected_fee = raw_fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
            check("fee_quantization:" + fid, fee == expected_fee)
            filled_by_order[order_id] = filled_by_order.get(order_id, ZERO) + quantity
            check(
                "ordered_quantity:" + fid,
                filled_by_order[order_id] <= _decimal(command["quantity"], positive=True),
            )
            fees += fee
            if side == "buy":
                bought += quantity
                gross_buy += quantity * price
            else:
                sold += quantity
                gross_sell += quantity * price
            prefix_cash = initial - gross_buy + gross_sell - fees
            prefix_quantity = bought - sold
            check("long_cash_prefix:" + fid, prefix_cash >= ZERO and prefix_quantity >= ZERO)
        expected_cash = initial - gross_buy + gross_sell - fees
        expected_inventory = bought - sold

    ledger = PostingLedger(initial)
    for fill in raw_fills:
        ledger.apply(fill)
    check(
        "ledger_equals_independent_batch",
        ledger.cash_usd == expected_cash
        and ledger.inventory == expected_inventory
        and ledger.fees_usd == fees,
    )

    orders = result.get("orders", [])
    order_ids: set[str] = set()
    unresolved: list[str] = []
    for order in orders:
        oid = _identity(order["id"])
        if oid in order_ids or oid not in markets:
            raise ValueError("Native order identity is duplicated or unknown.")
        order_ids.add(oid)
        qty = _decimal(order["quantity"], positive=True)
        filled = _decimal(order["filled"])
        remaining = _decimal(order["remaining"])
        status = order["status"]
        check(
            "order_arithmetic:" + oid,
            qty == _decimal(markets[oid]["quantity"])
            and order["side"] == markets[oid]["side"]
            and filled == filled_by_order.get(oid, ZERO)
            and qty == filled + remaining,
        )
        check("terminal_order:" + oid, status in TERMINAL)
        if status not in TERMINAL:
            unresolved.append(oid)
        if status == "FILLED":
            check("filled_complete:" + oid, remaining == ZERO and filled == qty)
        elif status in {"DENIED", "REJECTED"}:
            check("rejection_has_no_fill:" + oid, filled == ZERO)
        elif status == "CANCELED":
            cancellations = [
                c for c in commands.values() if c["kind"] == "cancel" and c["target"] == oid
            ]
            confirmations = [
                event
                for event in result.get("events", [])
                if event.get("kind") == "native_order_event"
                and event.get("event_type") == "OrderCanceled"
                and event.get("client_order_id") == oid
            ]
            confirmed = bool(cancellations) and any(
                exact_ns(event["at"]) >= exact_ns(command["submitted_ns"])
                for event in confirmations
                for command in cancellations
            )
            check("cancellation_confirmed:" + oid, confirmed)
            if not confirmed:
                unresolved.append(oid)
    check("every_market_command_has_native_state", order_ids == set(markets))
    unresolved.extend(sorted(set(markets) - order_ids))
    for state_index, state in enumerate([*result.get("snapshots", []), result]):
        balances = state.get("cash", {})
        free = state.get("free", {})
        reserved = state.get("reserved", {})
        complete = all(set(values) == {"USD", "SYN"} for values in (balances, free, reserved))
        check(f"balance_keys:{state_index}", complete)
        if complete:
            check(
                f"free_plus_reserved:{state_index}",
                all(
                    _decimal(free[currency]) + _decimal(reserved[currency])
                    == _decimal(balances[currency])
                    for currency in ("USD", "SYN")
                ),
            )
    native_cash = result.get("cash", {})
    if set(native_cash) == {"USD", "SYN"}:
        check(
            "native_totals_equal_independent_batch",
            _decimal(native_cash["USD"]) == expected_cash
            and _decimal(native_cash["SYN"]) == expected_inventory,
        )
    else:
        check("native_totals_equal_independent_batch", False)
    positions = result.get("positions", [])
    quantities = [_decimal(p["signed_quantity"], signed=True) for p in positions]
    check(
        "native_positions_long_only",
        all(qty >= ZERO for qty in quantities)
        and len({_identity(p["id"]) for p in positions}) == len(positions),
    )
    position_total = sum(quantities, ZERO)
    check("native_position_equals_inventory", position_total == expected_inventory)
    reserved = result.get("reserved", {})
    check(
        "terminal_market_reservations_zero",
        not unresolved
        and set(reserved) == {"USD", "SYN"}
        and all(_decimal(value) == ZERO for value in reserved.values()),
    )
    check("no_unresolved_order_state", not unresolved, sorted(set(unresolved)))
    problems = [entry["name"] for entry in checks if not entry["passed"]]
    return {
        "schema_version": 2,
        "kind": "synthetic-posting-reconciliation",
        "passed": not problems,
        "checks": checks,
        "problems": problems,
        "unresolved_orders": sorted(set(unresolved)),
        **ledger.state(),
        "duplicate_fill_rows_suppressed": duplicates,
        "batch_oracle": {
            "cash_usd": _text(expected_cash),
            "inventory": _text(expected_inventory),
            "fees_usd": _text(fees),
            "purchase_flows_usd": _text(gross_buy),
            "sale_flows_usd": _text(gross_sell),
        },
        "financial_validation": False,
        "scope": "Technical Decimal flows only; no matching, returns or market valuation.",
    }
