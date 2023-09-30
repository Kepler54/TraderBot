import sys
import logging
from os import getenv
from asyncio import run
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from data_analysis import DataAnalysis
from aiogram import Bot, Dispatcher, F
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboard:
    """Keyboard class"""
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="Отмена", callback_data="cancel")


class UserStates(StatesGroup):
    """User state machine class"""
    coin_pair_state = State()
    amount_state = State()


load_dotenv('.env')
BOT_TOKEN = getenv("BOT_TOKEN")
USER_ID = getenv("USER_ID")
sticker = "CAACAgIAAxkBAAEJxo9ku-Igyz6eO-Ly0z2sMfIQ4yNufgACtgkAAnlc4gnGTnKNypclSC8E"

kb = Keyboard()
dp = Dispatcher()
us = UserStates()
trade = DataAnalysis()


@dp.message(CommandStart(), F.from_user.id == int(USER_ID))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Main start function
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    await message.bot.send_sticker(message.from_user.id, sticker)
    try:
        trade.create_db()
        await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n\n{trade.get_full_info()}")
    except IndexError:
        await state.set_state(us.coin_pair_state)
        await message.answer(
            'Введите валютную пару строчными символами "eth_btc": ',
            reply_markup=kb.inline_keyboard.as_markup()
        )


@dp.message(us.coin_pair_state, F.from_user.id == int(USER_ID))
async def get_coin_pair_name(message: Message, state: FSMContext) -> None:
    """
    Coin pair and amount data input function
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(coin_pair_state=message.text)
    await state.set_state(us.amount_state)
    await message.answer(
        "Введите сумму входа на рынок: ",
        reply_markup=kb.inline_keyboard.as_markup()
    )


@dp.message(us.amount_state, F.from_user.id == int(USER_ID))
async def get_amount_value(message: Message, state: FSMContext) -> None:
    """
    Coin pair and amount data save function
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(amount_state=message.text)
    coin_pair = await state.get_data()
    amount = await state.get_data()
    trade.get_data_db(coin_pair, amount)
    await state.clear()
    await message.answer("Данные сохранены!")


@dp.callback_query()
async def callback_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Callback cancel function
    :param callback: CallbackQuery
    :param state: FSMContext
    :return: None
    """
    if state is None:
        return
    await state.clear()
    await callback.message.delete()


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Other message handling function
    :param message: Message
    :return: None
    """
    await message.answer("Не понял!")


async def main() -> None:
    """
    Entry point
    :return: None
    """
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    run(main())
