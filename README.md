# PsychTrader IPN Bot – Polymarket

Sistema modular de trading para Polymarket, diseñado para ejecutarse 24/7 en modo simulación (paper trading) mientras se habilita el acceso completo a la CLOB API.

## Arquitectura por Agentes

El bot utiliza una arquitectura modular basada en agentes especializados para garantizar robustez y escalabilidad:

1.  **DataIngestion**: Captura de datos en tiempo real desde Polymarket y fuentes externas.
2.  **MarketState**: Procesamiento y mantenimiento del estado actual del mercado.
3.  **Strategy**: Generación de señales de trading basadas en modelos y datos históricos.
4.  **RiskSafety**: Validación de riesgos, gestión de exposición y filtros de seguridad.
5.  **Execution**: Gestión de órdenes y ejecución en la CLOB (Central Limit Order Book).
6.  **Monitoring**: Supervisión del rendimiento, logs y alertas en tiempo real.

## Estructura del Proyecto

```text
PsychTrader-IPN-Bot/
├── agents/             # Código fuente de los agentes especializados
├── Mibot/              # Implementación principal y scripts de utilidad
│   ├── hooks/          # Hooks para extensiones del bot
│   ├── skills/         # Habilidades específicas de los agentes
│   ├── calcularpnl.py  # Cálculo de Profit & Loss
│   └── ...
├── docs/               # Documentación detallada y guías de ejemplo
├── .gitignore          # Archivos excluidos del repositorio
└── README.md           # Este archivo
```

## Configuración e Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/guillermojhoel2718-code/PsychTrader-IPN-Bot.git
cd PsychTrader-IPN-Bot
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Activar en Windows:
.\venv\Scripts\Activate
# Activar en Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install py-clob-client python-dotenv eth-account
```

### 4. Configuración local (.env)
Crea un archivo `.env` en la raíz del proyecto (o dentro de `Mibot/` según sea necesario) con tus credenciales. **NUNCA compartas ni subas este archivo.**

```env
POLYMARKET_PRIVATE_KEY=tu_clave_privada_aqui
POLYMARKET_FUNDER_ADDRESS=tu_direccion_aqui
POLYMARKET_CLOB_HOST=https://clob.polymarket.com
POLYMARKET_CHAIN_ID=137
POLY_BUILDER_CODE=tu_codigo_builder
```

## Estado del Proyecto
- Conexión a Polymarket CLOB probada con `py-clob-client`.
- Arquitectura documentada en archivos `.md` dentro de `Mibot/`.
- Seguridad: No se incluyen claves ni secretos en el historial de Git.
