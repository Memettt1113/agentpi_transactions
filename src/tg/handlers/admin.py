from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ChatMemberUpdated
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER

from logging import getLogger

from src.config import settings

router = Router()

logger = getLogger(__name__)

admins = settings.admins.split(",")


@router.message(Command("start"))
async def start_command(message: types.Message, state):
    if str(message.from_user.id) in admins:
        settings.chats.append(message.from_user.id)
        settings.is_stop = False

        await message.answer("Бот запущен.")


@router.message(Command("price"))
async def show_tokens(message: types.Message, state):
    if str(message.from_user.id) in admins:
        min_price = message.text.split()[1]

        try:
            min_price = float(min_price)
            if min_price <= 0:
                return None

            settings.min_price = min_price

            await message.answer(
                f"Минимальная цена сделки установлена на {min_price} TON"
            )
        except ValueError:
            return None


@router.message(Command("stop"))
async def stop_handler(message: types.Message, state):
    if str(message.from_user.id) in admins:
        settings.is_stop = True

        await message.answer("Бот остановлен.")


@router.my_chat_member()
async def on_bot_added(update: ChatMemberUpdated):
    old_status = update.old_chat_member.status
    new_status = update.new_chat_member.status

    logger.info(old_status)
    logger.info(new_status)
    chat_id = update.chat.id
    logger.info(chat_id)

    if (
        old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.MEMBER]
        and new_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]
    ):
        settings.chats.append(chat_id)

    if new_status == ChatMemberStatus.KICKED:
        settings.chats.remove(chat_id)

    logger.info(settings.chats)