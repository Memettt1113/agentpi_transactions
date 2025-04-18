from pydantic import SecretStr
from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    log_level: str

    server_host: str
    server_port: int

    tg_token: SecretStr
    admins: str
    min_price: float = 10.0
    is_stop: bool = False
    chats: list = []

    _bot: Bot = None
    _dp: Dispatcher = None
    _state_manager = None

    @property
    def bot(self) -> Bot:
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    @property
    def dp(self) -> Dispatcher:
        return self._dp

    @dp.setter
    def dp(self, dp):
        self._dp = dp

    @property
    def state_manager(self):
        return self._state_manager

    @state_manager.setter
    def state_manager(self, state_manager):
        self._state_manager = state_manager

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()


bot = Bot(settings.tg_token.get_secret_value())
dp = Dispatcher()

settings.bot = bot
settings.dp = dp
