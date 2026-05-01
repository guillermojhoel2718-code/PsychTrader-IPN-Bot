# DataIngestionAgent

## Propósito

Conectar con Polymarket (CLOB y APIs públicas) y producir datos crudos listos para procesar: lista de mercados, order books, y series temporales básicas.

## Responsabilidades

- Obtener mercados desde `ClobClient.get_markets()`.
- Filtrar mercados por tags, texto o slugs.
- Obtener order books por mercado/outcome.
- (Opcional) Guardar snapshots en CSV para backtesting.

## Entradas

- `clob_client`: instancia de `ClobClient` ya configurada (modo solo lectura).
- `filters`:
  - `text_contains`: lista de palabras clave (ej. ["ETH", "BTC"]).
  - `tags`: lista de tags Polymarket.
  - `max_markets`: número máximo de mercados a devolver.

## Salidas

- `markets`: lista de diccionarios de mercados filtrados.
- `order_book_by_market`: estructura `{market_id: order_book_data}`.

## Interfaz propuesta (Python)

```python
class DataIngestionAgent:
    def __init__(self, clob_client):
        self.client = clob_client

    def fetch_markets(self, filters: dict) -> list:
        """
        Devuelve una lista de mercados filtrados según `filters`.
        """
        ...

    def fetch_order_book(self, market: dict) -> dict:
        """
        Devuelve el order book para un mercado específico.
        """
        ...

    def fetch_markets_with_books(self, filters: dict) -> list[dict]:
        """
        Devuelve una lista de mercados, cada uno enriquecido con su order book.
        """
        ...

    def save_snapshot(self, data: list[dict], path: str) -> None:
        """
        Guarda un snapshot de datos en CSV/JSON para backtesting.
        """
        ...
```

## Requisitos técnicos

- Usar `py_clob_client` para `get_markets()`.
- Para order books, usar métodos públicos adecuados (a definir según versión de la librería).
- No depender de credenciales CLOB (funcionar en modo público/solo lectura).

## Checklist de implementación

- [ ] Crear clase `DataIngestionAgent` en `your_bot/src/data_ingestion/agent.py`.
- [ ] Implementar `fetch_markets` con filtros básicos.
- [ ] Implementar `fetch_order_book` (aunque inicialmente sea un stub).
- [ ] Implementar `fetch_markets_with_books`.
- [ ] Añadir opción de guardar snapshots en CSV/JSON.