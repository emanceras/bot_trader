"""One native rc7 bar context; no hand-written fill engine."""
import argparse
from decimal import Decimal
import importlib.metadata
import json
from pathlib import Path
import sys
import sysconfig
import traceback

from nautilus_trader.backtest import BacktestEngine, BacktestEngineConfig, SimulationModule
from nautilus_trader.execution import MakerTakerFeeModel, StaticLatencyModel
from nautilus_trader.model import (AccountType, AggregationSource, Bar, BarAggregation, BarSpecification,
    BarType, BookType, ClientOrderId, Currency, CurrencyPair, CurrencyType, InstrumentId,
    InstrumentStatus, MarketStatusAction, Money, OmsType, OrderSide, Price, PriceType,
    Quantity, QuoteTick, StrategyId, Symbol, TimeInForce, Venue)
from nautilus_trader.trading import Strategy, StrategyConfig
from nautilus_worker import book_view, decimal_text
from bar_fixtures import closed_eligible


def run(case):
    assert sys.version_info[:3]==(3,13,16) and not sysconfig.get_config_var('Py_GIL_DISABLED')
    assert importlib.metadata.version('nautilus-trader')=='2.0.0rc7'
    iid=InstrumentId.from_str('SYN-USD.SIM');venue=Venue('SIM');usd=Currency.from_str('USD')
    base=Currency('SYN',8,0,'Invented technical token',CurrencyType.CRYPTO);Currency.register(base,overwrite=True)
    instrument=CurrencyPair(iid,Symbol('SYN-USD'),base,usd,2,2,Price.from_str('0.01'),Quantity.from_str('0.01'),0,0,
        min_quantity=Quantity.from_str('0.01'),min_notional=Money.from_decimal(Decimal('10.00'),usd))
    bt=BarType(iid,BarSpecification(1,BarAggregation.MINUTE,PriceType.LAST),AggregationSource.EXTERNAL)
    trace=[];fills=[];errors=[];decision=None;sent=False;cancel_sent=False
    engine=BacktestEngine(BacktestEngineConfig(run_analysis=False,bypass_logging=True))
    cache=engine.cache

    def emit(kind,at,**fields):
        trace.append({'sequence':len(trace)+1,'kind':kind,'at':at,**fields})

    class Observer(SimulationModule):
        def pre_process(self,data):
            emit('module_pre_process',data.ts_init,data_type=type(data).__name__,ts_event=data.ts_event,ts_init=data.ts_init)
        def process(self,ts_now,context):
            emit('module_book_snapshot',ts_now,books=[book_view(b) for b in context.order_books],
                 origin='native exposed venue book; no guarantee of every internal OHLC substep')
            return None

    engine.add_venue(venue=venue,oms_type=OmsType.NETTING,account_type=AccountType.CASH,
        starting_balances=[Money.from_decimal(Decimal('1000.00'),usd),Money.from_decimal(Decimal(0),base)],
        base_currency=None,book_type=BookType.L1_MBP,
        fee_model=MakerTakerFeeModel(Decimal(case['maker_fee']),Decimal(case['taker_fee'])),
        latency_model=StaticLatencyModel(base_latency_nanos=case['latency_ns']),
        modules=[Observer()],use_message_queue=True,use_market_order_acks=True,use_random_ids=False,
        liquidity_consumption=True,allow_cash_borrowing=False,bar_execution=case['bar_execution'],
        bar_adaptive_high_low_ordering=case['adaptive'],trade_execution=False)
    engine.add_instrument(instrument)

    class Probe(Strategy):
        def __init__(self):
            super().__init__(StrategyConfig(strategy_id=StrategyId('bar-probe'),order_id_tag='B',log_events=False,log_commands=False))
        def guard(self,fn,*args):
            try:fn(*args)
            except Exception as exc:
                errors.append({'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()})
        def on_start(self):
            self.subscribe_bars(bt);self.subscribe_quotes(iid)
        def on_bar(self,bar):self.guard(self.bar,bar)
        def bar(self,bar):
            nonlocal decision
            now=self.clock.timestamp_ns()
            source=next(b for b in case['bars'] if b['ts_event']==bar.ts_event and b['ts_init']==bar.ts_init)
            emit('bar_callback',now,bar=bar.to_dict(),source_id=source['id'],modeled_available_ns=source['available_ns'],
                 source_label=source['label'],source_close_ns=source['close_ns'])
            if case['mode']=='timestamp':return
            if source['id']!='N' or decision is not None:return
            if not closed_eligible(now,source['close_ns'],source['available_ns']):
                emit('signal_blocked_unavailable_close',now);return
            decision={'at':now,'ready_at':now+case['decision_processing_ns'],'bar_id':'N','known_close':str(bar.close),
                      'side':'BUY','quantity':case['quantity']}
            emit('decision',now,decision=decision)
            if case['mode']=='native':self.submit('native_bar_close',bar.ts_event,bar.ts_init)
        def submit(self,origin,event_ns,available_ns):
            nonlocal sent
            if sent:raise ValueError('One intention only; duplicate submission forbidden')
            now=self.clock.timestamp_ns();sent=True
            emit('submit_intent',now,decision_at=decision['at'],price_source=origin,source_event_ns=event_ns,
                 source_available_ns=available_ns,nominal_arrival_ns=now+case['latency_ns'],
                 nominal_arrival_is_observed=False)
            order=self.order_factory.market(instrument_id=iid,order_side=OrderSide.BUY,
                quantity=Quantity.from_str(case['quantity']),time_in_force=TimeInForce.GTC,
                client_order_id=ClientOrderId('bar-probe-buy'))
            self.submit_order(order)
        def on_quote(self,quote):self.guard(self.quote,quote)
        def quote(self,quote):
            now=self.clock.timestamp_ns()
            source=next((q for q in case['quotes'] if q['event_ns']==quote.ts_event and q['available_ns']==quote.ts_init),None)
            emit('quote_callback',now,quote=quote.to_dict(),origin=source['origin'] if source else 'native_generated_or_unmapped_quote')
            if case['mode']!='causal' or sent:return
            if not decision or now<decision['ready_at']:
                emit('quote_skipped',now,reason='decision_not_ready');return
            if quote.ts_event<decision['ready_at'] or quote.ts_init<decision['ready_at']:
                emit('quote_skipped',now,reason='event_precedes_decision_no_retroactive_use');return
            if now-quote.ts_event>case['execution_policy']['max_quote_age_ns']:
                emit('quote_skipped',now,reason='quote_age');return
            if Decimal(case['quantity'])>Decimal(str(quote.ask_size)) or Decimal(case['quantity'])>Decimal(case['execution_policy']['max_order_quantity']):
                emit('quote_skipped',now,reason='declared_capacity_guard');return
            self.submit(source['id'] if source else 'unmapped_quote',quote.ts_event,quote.ts_init)
        def record(self,event):
            emit('native_order_event',self.clock.timestamp_ns(),event_type=type(event).__name__,ts_event=event.ts_event,ts_init=event.ts_init,
                 **{k:str(getattr(event,k)) for k in ['client_order_id','venue_order_id','trade_id','reason'] if hasattr(event,k)})
        def on_order_submitted(self,event):self.guard(self.record,event)
        def on_order_accepted(self,event):self.guard(self.record,event)
        def on_order_rejected(self,event):self.guard(self.record,event)
        def on_order_denied(self,event):self.guard(self.record,event)
        def on_order_pending_cancel(self,event):self.guard(self.record,event)
        def on_order_canceled(self,event):self.guard(self.record,event)
        def on_order_filled(self,event):self.guard(self.filled,event)
        def filled(self,event):
            self.record(event)
            if event.commission is None:raise ValueError('Missing commission is not zero')
            row={'at':self.clock.timestamp_ns(),'ts_event':event.ts_event,'ts_init':event.ts_init,
                 'fill_id':str(event.trade_id),'order_id':str(event.client_order_id),'side':event.order_side.name,
                 'quantity':str(event.last_qty),'price':str(event.last_px),'fee':decimal_text(event.commission),
                 'fee_currency':str(event.commission.currency),'liquidity_role':event.liquidity_side.name.lower(),
                 'origin':'native OrderFilled; no injected fill'}
            fills.append(row);emit('fill',row['at'],fill=row)

    engine.add_strategy(Probe())
    data=[]
    for b in case['bars']:
        assert Decimal(b['low'])<=min(Decimal(b['open']),Decimal(b['close']))<=max(Decimal(b['open']),Decimal(b['close']))<=Decimal(b['high'])
        data.append(Bar(bt,Price.from_str(b['open']),Price.from_str(b['high']),Price.from_str(b['low']),Price.from_str(b['close']),Quantity.from_str(b['volume']),b['ts_event'],b['ts_init']))
    quote_inputs=[]
    for q in case['quotes']:
        half=Decimal(case['execution_policy']['spread_usd'])/2;mid=Decimal(q['mid'])
        ask=mid+half;bid=mid-half
        quote_inputs.append({**q,'bid':str(bid),'ask':str(ask),'size':case['execution_policy']['visible_quantity_assumption'],
                             'future_bar_HLC_exposed':False,'kind':'synthetic_execution_assumption_not_observed_quote'})
        data.append(QuoteTick(iid,Price.from_str(str(bid)),Price.from_str(str(ask)),
            Quantity.from_str(case['execution_policy']['visible_quantity_assumption']),Quantity.from_str(case['execution_policy']['visible_quantity_assumption']),q['event_ns'],q['available_ns']))
    start=min(d.ts_init for d in data)-1;last=max(d.ts_init for d in data)
    data.append(InstrumentStatus(iid,MarketStatusAction.NONE,last+1_000_000_000,last+1_000_000_000,reason='common terminal clock drain; no market quote'))
    engine.add_data(data,sort=True);engine.run(start=start,end=last+1_000_000_001)
    account=cache.account_for_venue(venue)
    result={'case_id':case['id'],'engine':'NautilusTrader2.0.0rc7','python':sys.version,'configuration':case,
        'native_config':{'bar_execution':case['bar_execution'],'bar_adaptive_high_low_ordering':case['adaptive'],
                         'StaticLatencyModel.base_latency_nanos':case['latency_ns'],'use_message_queue':True,'risk_enabled':True,'custom_fill_model':False},
        'decision':decision,'trace':trace,'fills':fills,'synthetic_quote_inputs':quote_inputs,'callback_errors':errors,
        'balances':{str(k):decimal_text(v) for k,v in account.balances_total().items()},
        'free':{str(k):decimal_text(v) for k,v in account.balances_free().items()},
        'reserved':{str(k):decimal_text(v) for k,v in account.balances_locked().items()},
        'orders':[{'id':str(o.client_order_id),'status':o.status.name,'filled':str(o.filled_qty),'remaining':str(o.leaves_qty)} for o in cache.orders()],
        'positions':[{'id':str(p.id),'quantity':str(p.quantity),'side':p.side.name} for p in cache.positions()],
        'observability_limits':['OrderAccepted is an observed proxy, not a separate exchange-arrival callback','Module book snapshots do not certify all internal intrabar substeps'],
        'terminal_marker_ns':last+1_000_000_000}
    engine.dispose();return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bundle',type=Path,required=True);parser.add_argument('--case',required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();case=next(c for c in json.loads(args.bundle.read_text())['cases'] if c['id']==args.case)
    result=run(case)
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'case_id':args.case,'callback_errors':len(result['callback_errors']),'fills':result['fills']}))


if __name__=='__main__':main()
