# Agentes del sistema ETH 15m Psychology

Este documento describe los agentes lógicos que componen el sistema de trading para rondas ETH 15m en Polymarket, basado en el repo `polymarket/agents`.

---

## 1. MarketWatcherAgent

**Rol:** Observador de mercado.

- Suscribe a los mercados de Polymarket tipo "ETH up or down 15m".
- Usa el skill `polymarket_tracker` para:
  - leer el último precio de ETH (`price_now`),
  - calcular `delta_5m` y `delta_15m`,
  - calcular `t` (segundos restantes),
  - leer `bet_price` (cuota actual del mercado),
  - estimar `vol_state` según el rango de precios reciente,
  - adjuntar `trend_state` provisional (o el ingresado manualmente).
- Publica un objeto `MarketState` en un bus interno (cola o simple llamada a función).

---

## 2. DecisionAgent

**Rol:** Tomar decisiones de entrada/salida según la psicología de mercado.

- Cuando NO hay posición abierta:
  - Consume `MarketState` desde `MarketWatcherAgent`.
  - Llama a `entry_logic(MarketState, Settings)`:
    - Si devuelve `TradeSignal`, lo envía a `RiskAgent`.
    - Si devuelve `None`, no hace nada.

- Cuando hay posición abierta:
  - Llama a `exit_logic(MarketState, Position, Settings)`:
    - Si devuelve `"CLOSE"`, genera una señal de cierre y la envía a `RiskAgent`.
    - Si devuelve `"HOLD"`, mantiene la posición.

---

## 3. RiskAgent

**Rol:** Guardia de seguridad (preusetools).

- Recibe:
  - `TradeSignal` (para abrir posición),
  - o `ExitAction` (para cerrar posición).
- Usa el skill `risk_safety` para validar:
  - Tamaño de la posición (`pos_size` <= límite).
  - `pnl_session` > límite de pérdida permitido.
  - Contratos y mercados permitidos.
  - Límites de gas.
  - Ventanas de tiempo (no entrar con `t <= 30`).

- Salida:
  - `ValidatedSignal` en caso de aprobación.
  - `None` si se rechaza (log detail del motivo).

---

## 4. ExecutionAgent

**Rol:** Ejecutar operaciones en Polymarket.

- Recibe `ValidatedSignal` desde `RiskAgent`.
- Dependiendo de la configuración:
  - Opción A: usa la API CLOB de Polymarket:
    - construye una orden usando el cliente interno (`Polymarket` / `ClobClient` del repo original).
    - firma la orden con la clave privada configurada para el bot.
    - envía la orden al endpoint correspondiente.
  - Opción B: envía la orden a un hook de MetaMask:
    - empaqueta la señal en un objeto que un script en el navegador interpreta para generar una transacción/firma.
    - nunca maneja directamente la seed de MetaMask (solo se comunica con el hook).

- Registra:
  - resultado de la orden,
  - fees y gas,
  - actualización de `Position` y `pnl_session`.

---

## 5. Integración con `polymarket/agents`

El módulo `psych_eth15m` debe integrarse con el CLI de `polymarket/agents` de forma que se pueda correr:

- `python cli.py psych-eth15m --dry-run`
  - Ejecuta el bot en modo simulación, sin enviar órdenes reales.
- `python cli.py psych-eth15m --live`
  - Ejecuta el bot en vivo, usando `ExecutionAgent` con API CLOB o MetaMask hook, según configuración.

Los agentes comparten acceso a:

- `Settings` (derivado de `settings.json`),
- un registro de `pnl_session`,
- logs de operaciones y estados de mercado.

Cada agente debe ser lo más **puro y desacoplado** posible:
- `MarketWatcherAgent` no decide nada.
- `DecisionAgent` no toca la red.
- `RiskAgent` solo valida.
- `ExecutionAgent` solo ejecuta.

Esto hace que el sistema sea fácil de probar, simular y extender.