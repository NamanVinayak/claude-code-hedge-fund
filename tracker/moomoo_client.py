from moomoo import *
import pandas as pd


class MoomooClient:
    def __init__(self, host='127.0.0.1', port=11111):
        self.ctx = OpenSecTradeContext(host=host, port=port, filter_trdmarket=TrdMarket.US)

    def place_entry(self, ticker, side, qty, price):
        """Place entry order. side='long' or 'short'."""
        trd_side = TrdSide.BUY if side == 'long' else TrdSide.SELL
        ret, data = self.ctx.place_order(
            price=price, qty=qty, code=f'US.{ticker}',
            trd_side=trd_side, order_type=OrderType.NORMAL,
            trd_env=TrdEnv.SIMULATE, time_in_force=TimeInForce.DAY,
            remark=f'entry {side} {ticker}'
        )
        if ret != RET_OK:
            raise Exception(f"Entry order failed: {data}")
        return str(data['order_id'].iloc[0])

    def place_stop(self, ticker, side, qty, price):
        """Place stop loss. side is the ENTRY side — stop goes opposite."""
        trd_side = TrdSide.SELL if side == 'long' else TrdSide.BUY
        ret, data = self.ctx.place_order(
            price=price, qty=qty, code=f'US.{ticker}',
            trd_side=trd_side, order_type=OrderType.STOP,
            trd_env=TrdEnv.SIMULATE, time_in_force=TimeInForce.DAY,
            remark=f'stop {ticker} @ {price}'
        )
        if ret != RET_OK:
            raise Exception(f"Stop order failed: {data}")
        return str(data['order_id'].iloc[0])

    def place_target(self, ticker, side, qty, price):
        """Place take-profit. side is the ENTRY side — target goes opposite."""
        trd_side = TrdSide.SELL if side == 'long' else TrdSide.BUY
        ret, data = self.ctx.place_order(
            price=price, qty=qty, code=f'US.{ticker}',
            trd_side=trd_side, order_type=OrderType.NORMAL,
            trd_env=TrdEnv.SIMULATE, time_in_force=TimeInForce.DAY,
            remark=f'target {ticker} @ {price}'
        )
        if ret != RET_OK:
            raise Exception(f"Target order failed: {data}")
        return str(data['order_id'].iloc[0])

    def cancel_order(self, order_id):
        """Cancel a specific order."""
        try:
            self.ctx.modify_order(
                modify_order_op=ModifyOrderOp.CANCEL,
                order_id=order_id, qty=0, price=0,
                trd_env=TrdEnv.SIMULATE
            )
        except Exception:
            pass  # order may already be filled/cancelled

    def flatten_position(self, ticker, qty, side):
        """Close position at market. side is the POSITION side."""
        trd_side = TrdSide.SELL if side == 'long' else TrdSide.BUY
        ret, data = self.ctx.place_order(
            price=0, qty=qty, code=f'US.{ticker}',
            trd_side=trd_side, order_type=OrderType.MARKET,
            trd_env=TrdEnv.SIMULATE,
            remark=f'flatten {ticker}'
        )
        return ret == RET_OK

    def get_positions(self):
        ret, data = self.ctx.position_list_query(trd_env=TrdEnv.SIMULATE)
        return data if ret == RET_OK else pd.DataFrame()

    def get_orders(self):
        ret, data = self.ctx.order_list_query(trd_env=TrdEnv.SIMULATE)
        return data if ret == RET_OK else pd.DataFrame()

    def get_account_info(self):
        ret, data = self.ctx.accinfo_query(trd_env=TrdEnv.SIMULATE)
        return data if ret == RET_OK else None

    def close(self):
        self.ctx.close()
