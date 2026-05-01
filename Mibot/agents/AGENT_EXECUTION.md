# ExecutionAgent

## Propósito

Convertir señales aprobadas por riesgo en acciones concretas:

- Modo actual: **simulación / paper trading**.
- Modo futuro: ejecución real mediante la CLOB API de Polymarket.

## Entradas

- Lista de `Signal` filtradas.
- `MarketState` correspondiente a cada señal.
- Estado del portafolio simulado.

## Salidas

- Portafolio actualizado.
- Log detallado de “órdenes” ejecutadas (simuladas por ahora).

## Modo Simulación (actual)

- Asumir ejecución al `mid_price` del mercado.
- Actualizar balances: cash, cantidad de shares por outcome.
- Guardar log en CSV/JSON.

## Modo Live (futuro)

- Requiere:
  - `POLYMARKET_API_KEY`
  - `POLYMARKET_API_SECRET`
  - `POLYMARKET_API_PASSPHRASE`

- Configurar:
  - `client.set_api_creds(...)` con las credenciales.
  - Implementar métodos `place_order`, `cancel_order`, etc.

## Interfaz propuesta

```python
class ExecutionAgent:
    def __init__(self, clob_client, mode: str = "simulation"):
        self.client = clob_client
        self.mode = mode
        self.portfolio = {}  # estructura a definir

    def apply_signals(self, signals: list[Signal], market_states: dict[str, MarketState]) -> None:
        """
        Aplica señales. En modo simulación, actualiza portafolio virtual.
        En modo live (futuro), enviará órdenes reales.
        """
        ...

    def get_portfolio_state(self) -> dict:
        """
        Devuelve el estado actual del portafolio.
        """
        ...
```

## Checklist

- [ ] Implementar modo `simulation` primero.
- [ ] Definir estructura de portafolio (cash, posiciones).
- [ ] Añadir logging de cada acción ejecutada.
- [ ] Dejar hooks claros para el modo `live` cuando se habilite la API.
