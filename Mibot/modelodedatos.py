from dataclasses import dataclass
from typing import Optional, Literal, List

@dataclass
class MarketState:
    price_now: float
    price_ref: float
    delta_5m: float
    delta_15m: float
    t: int
    bet_price: float
    vol_state: Literal["low", "medium", "high"]
    trend_state: Literal["bull", "bear", "indecise"]
    is_day: bool
    bet_price_window: Optional[List[float]] = None  # últimos 30-60s de precios de cuota

@dataclass
class Position:
    direction: Literal["UP", "DOWN"]
    pos_size: float
    entry_bet_price: float
    entry_time: float
    min_pnl: float = 0.0
    max_pnl: float = 0.0
    open: bool = True

@dataclass
class TradeSignal:
    direction: Literal["UP", "DOWN"]
    pos_size: float
    reason: str

@dataclass
class ExitDecision:
    action: Literal["CLOSE", "HOLD"]
    reason: str