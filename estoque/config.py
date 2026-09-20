from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações declarativas carregadas do ambiente ou de um arquivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="ESTOQUE_",
        extra="ignore",
    )

    serial_port: str | None = Field(
        default=None,
        description="Porta serial USB configurada explicitamente no ambiente",
    )
    serial_baudrate: int = Field(
        default=9600,
        description="Velocidade da porta serial em bps",
        gt=0,
    )
    serial_timeout_seconds: float = Field(
        default=1.0,
        description="Tempo máximo para aguardar uma linha serial",
        gt=0.0,
    )
    serial_startup_delay_seconds: float = Field(
        default=2.0,
        description="Tempo de estabilização após abrir a porta serial",
        ge=0.0,
    )
    serial_reconnect_delay_seconds: float = Field(
        default=2.0,
        description="Intervalo entre tentativas de conexão serial",
        ge=0.0,
    )

    leitor_pin: str = Field(
        default="D2",
        description="Identificador do pino utilizado pelo leitor",
        min_length=1,
    )

    server_host: str = Field(
        default="0.0.0.0",
        description="Endereço de bind do servidor Tornado",
        min_length=1,
    )
    server_port: int = Field(
        default=8888,
        description="Porta TCP para o servidor HTTP/WebSocket",
        ge=1,
        le=65535,
    )

    dir_dados: str | None = Field(
        default=None,
        description="Diretório do 'banco de dados' local"
    )
