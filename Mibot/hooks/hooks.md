# Hooks de ejecución y preusetools (Risk Safety Hook)

Este documento explica cómo el sistema ETH 15m Psychology conecta la lógica de trading con la ejecución real de órdenes usando un *hook de seguridad* (preusetools).

## 1. Flujo general

1. `DecisionAgent` genera:
   - un `TradeSignal` (entrada),
   - o una orden de salida (cashout).

2. `RiskAgent` recibe el `TradeSignal` y llama al skill `risk_safety`:
   - Aplica límites de:
     - tamaño máximo por trade,
     - pérdida máxima de sesión,
     - contratos permitidos,
     - gas máximo,
     - ventana de tiempo (`t > 30` para nuevas entradas).

3. Si pasa todos los checks, `risk_safety` devuelve un `ValidatedSignal`.

4. El *hook de ejecución* recibe ese `ValidatedSignal` y decide:
   - Opción A: construir y enviar una orden vía API CLOB de Polymarket.
   - Opción B: construir un mensaje para un hook de MetaMask en el navegador.

En cualquier caso, **solo el hook de ejecución habla con la red**. La lógica de trading no toca claves privadas.

## 2. Objeto ValidatedSignal

El objeto `ValidatedSignal` debe contener:

- `direction`: `"UP"` o `"DOWN"`.
- `pos_size`: tamaño en USD (ya validado).
- `market_id`: ID del mercado ETH 15m en Polymarket.
- `side`: `BUY` o `SELL` en el CLOB.
- `max_slippage_bps`: slippage máximo permitido.
- `wallet_address`: dirección de la cuenta que opera.
- `timestamp`: hora en que se generó.
- `risk_flags`: lista de flags (por ejemplo, `["within_limits", "session_ok"]`).

El hook de ejecución solo acepta `ValidatedSignal` con `risk_flags` adecuados.

## 3. Hook para API CLOB (recomendado)

En la variante “API directa de Polymarket”:

- El hook es una función como:

```python
def execute_clob_order(validated_signal: ValidatedSignal, polymarket_client) -> str:
    """
    Envía una orden al CLOB de Polymarket usando el cliente oficial.
    Recibe un ValidatedSignal y un cliente ya configurado con la clave privada.
    Devuelve el ID de la orden o lanza una excepción en caso de error.
    """
    ...
```

- `polymarket_client` se basa en las clases ya presentes en el repo:
  - `Polymarket` y `GammaMarketClient` para identificar el mercado y enviar la orden. [web:43][web:52]

Este enfoque no requiere MetaMask en tiempo real; la clave privada se gestiona en `.env`.

## 4. Hook para MetaMask (opcional)

En la variante “MetaMask + navegador”:

- El hook implementa un canal de comunicación con el navegador:
  - por ejemplo, WebSocket local, HTTP o una cola de mensajes.

- Flujo:
  1. `execute_metamask_hook(validated_signal)` envía un mensaje JSON al navegador:
     - `{"type": "execute_trade", "signal": { ...campos de ValidatedSignal... }}`
  2. Un script en el navegador escucha ese mensaje y:
     - construye una transacción o firma adecuada,
     - llama a `window.ethereum.request(...)` para MetaMask.

Este documento se centra en la variante CLOB + API; MetaMask se deja como aprendizaje avanzado.

## 5. Papel de preusetools

`preusetools` es el concepto de “pre herramienta de seguridad”:

- `risk_safety` y el hook de ejecución implementan preusetools:
  - **Nada** se manda a la red sin pasar por estas capas.
- Es más fácil razonar y testear:
  - puedes simular muchas sesiones,
  - revisar logs de `ValidatedSignal`,
  - luego recién activar la ruta real de ejecución.