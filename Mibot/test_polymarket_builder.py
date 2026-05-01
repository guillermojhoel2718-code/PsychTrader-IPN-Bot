import os
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON


def main():
    print(">>> Iniciando test_polymarket_builder.py")
    print("Directorio actual:", os.getcwd())

    load_dotenv()
    print(">>> .env cargado")

    host = os.getenv("POLYMARKET_CLOB_HOST", "https://clob.polymarket.com")
    chain_id = int(os.getenv("POLYMARKET_CHAIN_ID", POLYGON))
    private_key = os.getenv("POLYMARKET_PRIVATE_KEY")
    funder = os.getenv("POLYMARKET_FUNDER_ADDRESS")

    print("Host:", host)
    print("Chain ID:", chain_id)
    print("Private key definida:", bool(private_key))
    print("Funder:", funder)

    if not private_key:
        print("ERROR: Falta POLYMARKET_PRIVATE_KEY en el .env")
        return

    if not private_key.startswith("0x"):
        private_key = "0x" + private_key

    print(">>> Creando ClobClient...")
    client = ClobClient(
        host,
        key=private_key,
        chain_id=chain_id,
        funder=funder,
    )
    print(">>> ClobClient creado correctamente")

    # Obtener mercados
    print(">>> Llamando a client.get_markets()...")
    markets = client.get_markets()

    # Detectar dónde está la lista
    lista = None
    if isinstance(markets, dict) and "data" in markets:
        lista = markets["data"]
    elif isinstance(markets, list):
        lista = markets

    if not lista:
        print("No se encontró lista de mercados en la respuesta.")
        print("Respuesta cruda:", markets)
        return

    print(f"Total de mercados en lista: {len(lista)}")
    print("Primeros 3 mercados (pregunta + slug):")
    for m in lista[:3]: 
        question = m.get("question")
        slug = m.get("market_slug")
        print("-", question, "| slug:", slug)

        # Mostrar también tokens/outcomes
        tokens = m.get("tokens") or []
        for t in tokens:
            print("   Outcome:", t.get("outcome"), "precio:", t.get("price"))
  # 4) Intentar crear / derivar credenciales CLOB
    print("\n>>> Intentando create_or_derive_api_creds()...")
    try:
        creds = client.create_or_derive_api_creds()
        print("Credenciales CLOB generadas / derivadas:")
        print("  key       =", creds.get("key"))
        print("  secret    =", creds.get("secret"))
        print("  passphrase=", creds.get("passphrase"))
    except Exception as e:
        print("ERROR al crear/derivar credenciales CLOB:")
        print(repr(e))

if __name__ == "__main__":
    main()