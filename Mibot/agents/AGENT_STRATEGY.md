# StrategyAgent

## Propósito

Generar señales de trading (entrada, salida, no acción) a partir de `MarketState` y parámetros de estrategia.

## Sub-agentes

- `EntryLogicAgent`
- `ExitLogicAgent`

> Nota: el control de riesgo se documenta por separado en `AGENT_RISK_SAFETY.md`.

## Entradas

- Uno o varios `MarketState`.
- Parámetros de estrategia (config/JSON):
  - mercados objetivo (ej. ETH, BTC, elecciones),
  - umbrales de precio/probabilidad,
  - horizonte temporal.

## Salidas

- Lista de **señales**:
  - `type`: "ENTRY" | "EXIT"
  - `market_id`
  - `outcome_name`
  - `side`: "BUY" | "SELL"
  - `price_target`
  - `size_target` (en USD o “units” abstractas)
  - `reason`: texto breve.

## Interfaz propuesta

```python
@dataclass
class Signal:
    type: str        # "ENTRY" | "EXIT"
    market_id: str
    outcome_name: str
    side: str        # "BUY" | "SELL"
    price_target: float | None
    size_target: float | None
    reason: str

class EntryLogicAgent:
    def generate_entry_signals(self, market_states: list[MarketState]) -> list[Signal]:
        """
        Recorre los MarketState y genera señales de entrada.
        """
        ...

class ExitLogicAgent:
    def generate_exit_signals(self, market_states: list[MarketState], portfolio_state: dict) -> list[Signal]:
        """
        Dado el portafolio actual y el estado de mercado, genera señales de salida.
        """
        ...
```

## Requisitos

- Empezar con reglas simples (thresholds) antes de IA avanzada.
- No interactuar con la API de Polymarket directamente; solo producir señales.

## Checklist

- [ ] Definir dataclass `Signal`.
- [ ] Implementar `EntryLogicAgent.generate_entry_signals`.
- [ ] Implementar `ExitLogicAgent.generate_exit_signals`.
- [ ] Documentar las primeras reglas de ejemplo en comentarios/config.
