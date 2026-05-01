# Notas de agentes y comandos útiles (ETH 15m Psychology)

Estas notas explican cómo usar el módulo `psych_eth15m` dentro del repo `polymarket/agents` y qué partes del framework original se reutilizan.

## 1. Estructura del módulo `psych_eth15m`

Carpeta sugerida:

- `agents/psych_eth15m/`
  - `__init__.py`
  - `strategy.py`
  - `market_watcher.py`
  - `decision_agent.py`
  - `risk_agent.py`
  - `execution_agent.py`
  - `config/claude.md`
  - `config/settings.json`
  - `skills/entry_logic.md`
  - `skills/exit_logic.md`
  - `skills/risk_safety.md`

Cada archivo:

- `market_watcher.py`:
  - implementa `MarketWatcherAgent`, que crea `MarketState` usando `agents/polymarket/polymarket.py`.
- `decision_agent.py`:
  - implementa `DecisionAgent`, que usa los skills `entry_logic` y `exit_logic`.
- `risk_agent.py`:
  - implementa `RiskAgent`, que usa el skill `risk_safety` para producir `ValidatedSignal`.
- `execution_agent.py`:
  - implementa `ExecutionAgent`, que llama al cliente Polymarket (CLOB/API).

## 2. Uso del CLI original

Comando base del repo: [web:43]

```bash
python scripts/python/cli.py
```

Queremos agregar un comando nuevo, por ejemplo `psych-eth15m`, que:

- Modo dry-run:

```bash
python scripts/python/cli.py psych-eth15m --mode dry-run --rounds 100
```

- Modo live (peligroso, solo con poco capital):

```bash
python scripts/python/cli.py psych-eth15m --mode live
```

Internamente, el comando debe:

1. Cargar `settings.json`.
2. Instanciar:
   - `MarketWatcherAgent`,
   - `DecisionAgent`,
   - `RiskAgent`,
   - `ExecutionAgent`.
3. Entrar en un loop:
   - Actualizar `MarketState`.
   - Evaluar entrada/salida.
   - Aplicar `risk_safety`.
   - Ejecutar o simular la orden.

## 3. Funciones Python que se recomiendan reutilizar (no reescribir)

Desde el repo original (`agents/polymarket`): [web:43]

- `Polymarket` (clase principal para conectarse a la API y ejecutar órdenes).
- `GammaMarketClient` (para obtener datos de mercados y eventos).
- Modelos de `objects.py` para representar:
  - mercados, órdenes, trades, etc.

En lugar de escribir tu propio cliente HTTP, usa estas clases y utilidades.

## 4. Comandos útiles en desarrollo

### 4.1 Ver mercados

```bash
python scripts/python/cli.py get-all-markets --limit 10 --sort-by volume
```

Permite ver mercados activos y sus IDs, que usarás en `settings.json` para ETH 15m.

### 4.2 Modo prueba con tu estrategia

Una vez integrado `psych_eth15m` con el CLI:

```bash
# Simulación (no envía órdenes reales)
python scripts/python/cli.py psych-eth15m --mode dry-run --rounds 50 --log-file logs/psych_eth15m_test.jsonl
```

Esto debería:
- simular 50 rondas de ETH 15m,
- aplicar tus reglas de entrada/salida,
- guardar logs en `logs/psych_eth15m_test.jsonl`.

### 4.3 Modo live controlado (después de probar)

```bash
# Live trading con wallet de prueba y límites de risk_safety
python scripts/python/cli.py psych-eth15m --mode live --max-trades 20
```

- Requiere `.env` configurado con:
  - `POLYGON_WALLET_PRIVATE_KEY` o equivalente.
- El `RiskAgent` debe tener habilitados límites estrictos de:
  - tamaño máximo por trade,
  - pérdida máxima de sesión,
  - contratos permitidos.

## 5. Qué partes del repo original se pueden ignorar en esta fase

En esta estrategia ETH 15m, se ignoran:

- Integraciones con LLM/OPENAI (aunque la repo menciona LLMs, no se usan en producción).
- Integraciones con Chroma y RAG (no necesarias para tu primera versión).
- Cualquier ejemplo que requiera `OPENAI_API_KEY`.

Más adelante, si quieres añadir capa de IA para filtrar noticias, puedes mirar esas partes, pero no son necesarias para que el bot funcione con tus reglas actuales.