# RiskSafetyAgent

## Propósito

Aplicar reglas de riesgo al conjunto de señales generadas por `StrategyAgent` para evitar sobreexposición y comportamientos peligrosos.

## Entradas

- Lista de `Signal` (entradas + salidas).
- Estado del portafolio (simulado o real):
  - cash disponible,
  - posiciones abiertas,
  - exposición por tema/mercado/outcome.

## Salidas

- Lista filtrada de `Signal` (solo las que pasan los checks de riesgo).

## Reglas típicas

- Máximo tamaño por trade (ej. 1–5% del capital).
- Máximo número de posiciones abiertas simultáneas.
- Máxima exposición por tema (ej. no más de X% en “elecciones USA”).
- Bloqueo si hay error repetido de API o si no hay datos suficientes.

## Interfaz propuesta

```python
class RiskSafetyAgent:
    def filter_signals(self, signals: list[Signal], portfolio_state: dict) -> list[Signal]:
        """
        Recibe señales crudas y devuelve solo las permitidas según las reglas de riesgo.
        """
        ...

    def check_global_limits(self, portfolio_state: dict) -> bool:
        """
        Retorna True si el sistema puede seguir operando (no se exceden límites globales).
        """
        ...
```

## Checklist

- [ ] Definir estructura mínima de `portfolio_state`.
- [ ] Implementar `filter_signals` con al menos 1–2 reglas sencillas.
- [ ] Implementar `check_global_limits` para detectar estado “crítico”.