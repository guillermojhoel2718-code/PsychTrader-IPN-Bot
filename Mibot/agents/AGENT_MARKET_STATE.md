# MarketStateAgent

## Propósito

Transformar los datos crudos de Polymarket en objetos de estado estructurados (`MarketState`) que sean fáciles de usar por la estrategia.

## Responsabilidades

- Mapear el formato de `get_markets()` a un `MarketState` interno.
- Incorporar datos del order book (mid price, spread, liquidez).
- Calcular métricas derivadas simples (tendencia, volatilidad básica, etc.).

## Entradas

- `raw_market`: dict de un mercado de Polymarket.
- `order_book`: dict con el libro de órdenes de ese mercado.

## Salidas

- Objeto `MarketState` (puede ser dataclass) con campos:
  - `market_id`
  - `question`
  - `slug`
  - `tags`
  - `outcomes`: lista de outcomes con:
    - `outcome_name`
    - `last_price`
    - `mid_price`
    - `bid_ask_spread`
    - `liquidity`
  - `metadata` (fechas, iconos, etc.).

## Interfaz propuesta (Python)

```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class OutcomeState:
    outcome_name: str
    last_price: float | None
    mid_price: float | None
    bid_ask_spread: float | None
    liquidity: float | None

@dataclass
class MarketState:
    market_id: str
    question: str
    slug: str
    tags: list[str]
    outcomes: List[OutcomeState]
    raw: Dict[str, Any]

class MarketStateAgent:
    def build_market_state(self, raw_market: dict, order_book: dict | None = None) -> MarketState:
        """
        Construye un MarketState a partir de un dict de mercado y, opcionalmente, su order book.
        """
        ...
```

## Requisitos técnicos

- No asumir aún presencia de credenciales CLOB.
- Mantener `raw` para poder acceder a datos completos si la estrategia los requiere.
- Diseñar teniendo en mente extensión futura a features para IA (features vectoriales).

## Checklist de implementación

- [ ] Definir `OutcomeState` y `MarketState` como dataclasses.
- [ ] Implementar `build_market_state(raw_market, order_book)`.
- [ ] Calcular mid price y spread si se dispone de order book.
- [ ] Añadir tests sencillos con mercados de ejemplo obtenidos con `DataIngestionAgent`.
