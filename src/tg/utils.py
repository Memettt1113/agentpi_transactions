from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import settings
from src.dto import TransactionTypeEnum


if TYPE_CHECKING:
    from src.dto import TransactionDTO

bot = settings.bot
chat_ids = settings.chats

logger = getLogger(__name__)


async def send_message_to_group(transaction: TransactionDTO) -> None:

    if settings.is_stop:
        return

    url = f"https://tonscan.org/tx/{transaction.tx_hash}"

    message = (
        f"Новая покупка <b>{transaction.name}</b> от {settings.min_price} TON\n\n"
        f"🔒 Хэш: <code>{transaction.tx_hash}</code>\n"
        f"💰 Получено: {transaction.amount} {transaction.name}\n"
        f"💵 Цена: {transaction.price} TON\n"
        f"👤 Покупатель: <code>{transaction.user_wallet}</code>"
    )

    buttons = [
        [InlineKeyboardButton(
            text="📎 Сделка",
            url=url
        )],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(1)

    for chat_id in chat_ids:
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard.as_markup()
        )


def validate_transaction(transaction: TransactionDTO | None) -> bool:
    if not transaction:
        logger.info("No transaction.")
        return False

    if transaction.type != TransactionTypeEnum.BUY.value:
        logger.info(transaction.type)
        logger.info("Transaction TYPE is not BUY!")
        return False

    if transaction.price < settings.min_price:
        return False

    return True
