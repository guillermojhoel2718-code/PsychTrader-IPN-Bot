# Sistema de trading para rondas de Ethereum 15m en Polymarket

Este documento describe el sistema de trading que usará un bot basado en IA para operar en **rondas de 15 minutos y de 5 minutos de Ethereum en Polymarket**, usando un wallet de MetaMask aislado y una capa de seguridad (`preusetools`).  
El objetivo es **probar la psicología del mercado** y no maximizar el tamaño del capital (por ahora solo se usarán ~10–20 USD de prueba).

---

## 1. Variables básicas del sistema

El bot maneja estas variables observables:

- `Δ5m`: cambio de precio de ETH en los últimos 5 minutos (en dólares).
- `Δ15m`: cambio de precio de ETH en los últimos 15 minutos (en dólares).
- `price_now`: precio actual de ETH.
- `t`: segundos restantes de la ronda (15 minutos = 900 s).
- `bet_price`: precio de la cuota en Polymarket, entre 0 y 1 (por ejemplo 0.90 = 90 centavos).
- `pos_size`: tamaño de la apuesta (1, 3 o 5 dólares; hoy se limita a 5 USD máximo por entrada).
- `pnl_session`: resultado acumulado de la sesión (en dólares).
- `vol_state`: estado de volatilidad, puede ser:
  - `low` (baja),
  - `medium` (media),
  - `high` (alta).
- `trend_state`: estado de tendencia, elegido manualmente por el trader en cada ronda (entrada libre en un formulario), con valores posibles:
  - `bull` (alcista),
  - `bear` (bajista),
  - `indecise` (lateral/indecisa).

Hay un **formulario manual** donde el trader marca `trend_state` para cada ronda, según cómo ve el comportamiento de las velas y de la cuota.

---

## 2. Reglas de entrada (compra)

### 2.1 Regla de tendencia de corto plazo

- Si `Δ5m ≥ 1` → tendencia alcista de corto plazo.  
- Si `Δ5m o 5 min ≤ -1` → tendencia bajista de corto plazo.  
- Si `Δ15m ≥ 3` → tendencia alcista fuerte.  
- Si `Δ15m ≤ -3` → tendencia bajista fuerte.  

### 2.2 Momento de entrada en el reloj

- Regla base: solo considerar entrar cuando `t ∈ [150, 180]` (entre 3:00 y 2:30 restantes).  
- Si se cumple una condición de entrada, preferir ejecutar alrededor de `t ≈ 165`, no más tarde, a menos que la tendencia alcista/bajista sea muy clara.  
- Nunca abrir nuevas apuestas si `t ≤ 30`.  

Horarios:
- En horario **día** (por ejemplo 08:00–20:00), solo se consideran entradas si `t ≤ 120` (faltan 2 minutos o menos).  
- Fuera de horario día, se permite una ventana algo más amplia, pero siempre siguiendo los límites de riesgo.

### 2.3 Tamaño de apuesta según movimiento

Define `diff = |price_now − price_ref|`, donde `price_ref` es el precio de ETH al inicio de la ronda.

- Si `diff ≥ 2` → `pos_size = 5`.  
- Si `1 ≤ diff < 2` → `pos_size = 3`.  
- Si `diff < 1` y no hay tendencia clara → `pos_size = 1` (máximo 1 dólar en indecisa).  

Selección de dirección:

- Si `trend_state = "bull"` → apostar a up.  
- Si `trend_state = "bear"` → apostar a down.  
- Si `trend_state = "indecise"` → solo `pos_size ≤ 1` y solo si `bet_price ∈ [0.4, 0.6]`.

### 2.4 Filtro de precio de la apuesta

- Si `bet_price ≥ 0.90` → no abrir nuevas posiciones.  
- Si `t ≤ 60` y `bet_price ≈ 0.90` y el trader decide entrar, entonces `pos_size = 1`.

---

## 3. Reglas de salida (cashout / cierre)

### 3.1 Cashout por indecisión con pequeño profit

- Si el bot abre una posición y, dentro de los siguientes 60 s:
  - `PnL > 0` (ya está en verde),
  - el mercado entra en estado `indecise` (rango estrecho de oscilación de `bet_price` en 30–60 s),
- entonces ejecutar `cashout` y cerrar.

El rango de oscilación de `bet_price` en 30–60 s se define como:

- En **noche**: 0.30–0.80 (30–80 centavos) como rango normal.  
- En **día**: 0.15–0.40 (15–40 centavos).  
Si el precio permanece dentro de estos rangos, se marca como `indecise`.

### 3.2 Cashout rápido en indecisa al final

- Si `t ≤ 50` y el mercado sigue en estado `indecise` y `PnL ≥ 0.20` → ejecutar `cashout`.

### 3.3 Cashout por remontada

- Si en algún momento `PnL ≤ -2` y luego `PnL ≥ +2` **antes** de `t ≤ 60`, entonces ejecutar `cashout` inmediatamente.

---

## 4. Reglas de gestión de riesgo / filtros de mercado

### 4.1 Pausa por pérdidas

- Si `pnl_session ≤ -10` → dejar de realizar nuevas entradas durante al menos 30 minutos.

### 4.2 No sobreoperar en condiciones difíciles

- Si `|Δ15m| ≥ 6` (post‑rally fuerte) y `t ≤ 60`, **no** abrir nuevas entradas.  
- Si `3 ≤ |Δ15m| ≤ 4` (corrección), ajustar el objetivo de `take_profit` a `+1` o `+2` USD; no buscar más.  

Horario:
- Definimos bloque `"day"` y `"night"`.  
- En `"day"` se limita el número máximo de operaciones por hora (por ejemplo 10–15).  
- En `"night"` se permite un poco más de flexibilidad, pero siempre con límites de riesgo.

### 4.3 Solo una apuesta fuerte en tendencia clara

- Si `trend_state = "bull"` y `|Δ15m| ≥ 3` → limitar a **1 posición máxima** simultánea.  
- Esta posición se abre cuando el precio está cerca de una “última resistencia” (máximo local reciente en 15 min).

---

## 5. Observaciones de psicología del mercado (reglas cualitativas)

Estas son ideas empíricas que pueden codificarse más adelante:

- Si hay **dos velas grandes** (±5–6 dólares) consecutivas y el `bet_price` converge hacia `0.50`, el mercado se marca como `indecise`.  
- Si `Δ15m ≥ 3` (alcista fuerte), luego hay una corrección que lleva `bet_price` a `0.4–0.6` y se mantiene `indecise` en los últimos 60–90 s, entonces hay mayor probabilidad de cierre en up.  
- Cuando en los últimos minutos **rompe el precio de entrada** (de up o down) con un ciclo alcista claro de 1 minuto, se puede abrir posición a favor de esa ruptura.  
- Cuando la volatilidad es baja, la tendencia tiende a mantenerse más tiempo; en alta volatilidad conviene cashout más rápido.

---

## 6. Infraestructura con skills y preusetools

El sistema debe montarse siguiendo:

1. **Skills de Claude**:
   - `skill_polymarket_tracker` – lee el mercado de ETH 15m, calcula `Δ5m`, `Δ15m`, `t`, `bet_price`, `vol_state`.  
   - `skill_entry_logic` – aplica reglas 2.1–2.4 y decide si emitir `TradeSignal`.  
   - `skill_exit_logic` – aplica reglas 3.1–3.3 y decide `Cashout` o `Hold`.  
   - `skill_risk_safety` (pre‑tool) – valida cada señal antes de llegar a MetaMask, asegurando:
     - importe < 5 dólares,
     - `pnl_session > -10`,
     - contratos permitidos,
     - gas razonable, etc.

2. **MetaHook (MetaMask hook en el navegador)**:
   - Solo responde a eventos `execute_trade({ txData, chainId, wallet })` que cumplan el esquema validado por `skill_risk_safety`.  
   - Nunca firma mensajes arbitrarios generados directamente por Claude.

3. **Deployment**:
   - Piensa correr el bot en UCloud (o similar) 24/7, solo para rondas de Ethereum 15m.  
   - El wallet de MetaMask usado será uno **aparte**, con 10–20 USD de prueba.  