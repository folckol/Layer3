import os
import random

import aiohttp
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

import openpyxl

from GMStrickAuto import *

class Form(StatesGroup):
    Wallets = State()
    PrivateKeys = State()
    Proxies = State()

    DeleteWallets = State()

bot = Bot(token='')
dp = Dispatcher(bot, storage=MemoryStorage())


async def is_user_in_channel(user_id):
    for channel in [-1001868025034, -1001828079590]:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["left", "kicked"]:
                pass
            else:
                return False
        except Exception as e:
            print(e)
            return False

    return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        try:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
        except:
            user = User(
                telegram_id=message.from_user.id
            )
        session.add(user)
        session.commit()

    await bot.send_message(
        message.chat.id,
        "Привет, {}".format(message.from_user.first_name),
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            types.KeyboardButton('Добавить аккаунты'),
            types.KeyboardButton('Удалить аккаунты'),
            types.KeyboardButton('Посмотреть мои аккаунты')
        ),
    )

@dp.message_handler(lambda message: message.text == 'Отмена', state='*')
async def start_(message: types.Message):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        try:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username
            )
        except:
            user = User(
                telegram_id=message.from_user.id
            )
        session.add(user)
        session.commit()

    await bot.send_message(
        message.chat.id,
        "Вы находитесь в главном меню".format(message.from_user.first_name),
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            types.KeyboardButton('Добавить аккаунты'),
            types.KeyboardButton('Удалить аккаунты'),
            types.KeyboardButton('Посмотреть мои аккаунты'),
        ),
    )

@dp.message_handler(lambda message: message.text == 'Добавить аккаунты', state='*')
async def delete_accounts(message: types.Message, state: FSMContext):

    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'), InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if user.records and len(user.records) == 100:
        await bot.send_message(
            message.chat.id,
            'Количество загруженных аккаунтов насчитывает 100, вы не можете загрузить больше аккаунтов.'
        )
        return
    else:
        if user.records and len(user.records) < 100:
            await state.set_state(accsCount=(100-len(user.records)))
        else:
            await state.set_state(accsCount=100)


    session.close()

    await bot.send_message(
        message.chat.id,
        'Отправьте мне документ с адресами кошельков.',
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton('Отмена')
        )
    )
    await state.set_state(Form.Wallets.state)

@dp.message_handler(lambda message: message.text == 'Удалить аккаунты', state='*')
async def add_accounts(message: types.Message, state: FSMContext):

    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'), InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return


    await bot.send_message(
        message.chat.id,
        'Отправьте мне документ с адресами кошельков, которые нужно удалить.',
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton('Отмена')
        )
    )
    await state.set_state(Form.DeleteWallets.state)

@dp.message_handler(state=Form.DeleteWallets, content_types=['document'])
async def handle_delete_wallets(message: types.Message, state: FSMContext):
    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'),
                InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

        # print('awdad')

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)

    # указать путь для сохранения файла
    local_file_path = f"{random.randint(1000000,10000000)}.txt"

    # скачать файл
    await bot.download_file(file_info.file_path, local_file_path)

    # открыть и обработать файл

    wallets = []

    with open(local_file_path, 'r') as file:
        for i in file:
            wallet = i.rstrip()
            if '0x' not in wallet[:4] or len(wallet) != 42:
                await message.answer('Некоторые ваши данные указаны в неверном формате, перепроверьте файл и отправьте его заново.')
                return

            wallets.append(wallet)

    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

    for record in user.records:
        if record.address in wallets:
            session.query(Record).filter_by(Record.id == record.id).delete()
            session.commit()

    session.close()

    await bot.send_message(
        message.chat.id,
        'Кошельки, указанные в вашем текстовике были успешно удалены'
    )

    os.remove(os.getcwd() + f'\\{local_file_path}')

    # здесь вы можете добавить логику обработки документа с кошельками
    await state.set_state(Form.PrivateKeys.state)


@dp.message_handler(state=Form.Wallets, content_types=['document'])
async def handle_wallets(message: types.Message, state: FSMContext):
    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'),
                InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

        # print('awdad')

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)

    # указать путь для сохранения файла
    local_file_path = f"{random.randint(1000000,10000000)}.txt"

    # скачать файл
    await bot.download_file(file_info.file_path, local_file_path)

    # открыть и обработать файл

    wallets = []

    with open(local_file_path, 'r') as file:
        for i in file:
            wallet = i.rstrip()
            if '0x' not in wallet[:4] or len(wallet) != 42:
                await message.answer('Некоторые ваши данные указаны в неверном формате, перепроверьте файл и отправьте его заново.')
                return

            wallets.append(wallet)

    await state.update_data(wallets=wallets)


    await bot.send_message(
        message.chat.id,
        'Принял ваш документ с кошельками. Отправьте текстовик с приватными ключами.'
    )

    os.remove(os.getcwd() + f'\\{local_file_path}')

    # здесь вы можете добавить логику обработки документа с кошельками
    await state.set_state(Form.PrivateKeys.state)

@dp.message_handler(state=Form.PrivateKeys, content_types=['document'])
async def handle_private_keys(message: types.Message, state: FSMContext):

    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'), InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)

    # указать путь для сохранения файла
    local_file_path = f"{random.randint(1000000, 10000000)}.txt"

    # скачать файл
    await bot.download_file(file_info.file_path, local_file_path)

    # открыть и обработать файл

    privates = []

    with open(local_file_path, 'r') as file:
        for i in file:
            wallet = i.rstrip()
            if '0x' not in wallet[:4] or len(wallet) != 66:
                await message.answer('Некоторые ваши данные указаны в неверном формате, перепроверьте файл и отправьте его заново.')
                return

            privates.append(wallet)

    await state.update_data(privates=privates)


    await bot.send_message(
        message.chat.id,
        'Принял ваш документ с приватными ключами. Отправьте текстовик с прокси (обратите внимание, что софт поддерживает только http прокси).'
    )
    # здесь вы можете добавить логику обработки документа с приватными ключами

    os.remove(os.getcwd() + f'\\{local_file_path}')

    await state.set_state(Form.Proxies.state)

@dp.message_handler(state=Form.Proxies, content_types=['document'])
async def handle_proxies(message: types.Message, state: FSMContext):

    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'), InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

    file_id = message.document.file_id
    file_info = await bot.get_file(file_id)

    # указать путь для сохранения файла
    local_file_path = f"{random.randint(1000000, 10000000)}.txt"

    # скачать файл
    await bot.download_file(file_info.file_path, local_file_path)

    # открыть и обработать файл

    proxies = []

    with open(local_file_path, 'r') as file:
        for i in file:
            proxy = i.rstrip()
            if proxy.count(':') != 3:
                await message.answer(
                    'Некоторые ваши данные указаны в неверном формате, перепроверьте файл и отправьте его заново.')
                return

            proxies.append(proxy)

    os.remove(os.getcwd() + f'\\{local_file_path}')


    data = await state.get_data()

    if len(data['wallets']) != len(data['privates']) != len(proxies):
        await message.answer(
            'У ваших текстовиков разный размер, посторите попытку заново:\n'
            f"Адресса: {len(data['wallets'])} строк\n"
            f"Приватные ключи: {len(data['privates'])} строк\n"
            f"Прокси: {len(proxies)} строк",reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            types.KeyboardButton('Добавить аккаунты'),
            types.KeyboardButton('Удалить аккаунты'),
            types.KeyboardButton('Посмотреть мои аккаунты'),
        ))
        await state.finish()

    else:

        Session = sessionmaker(bind=engine)
        session = Session()

        accsCount = await state.get_state()

        all_data = []

        for i in range(accsCount['accsCount']):
            rec = Record(id=str(uuid.uuid4()),
                         user=str(message.from_user.id),
                         address=data['wallets'][i],
                         private=data['privates'][i],
                         proxy=proxies[i],
                         GMstrick=0,
                         NeedTasks=True
                         )
            all_data.append(rec)

        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        user.records = all_data

        session.commit()
        session.close()

        await bot.send_message(
            message.chat.id,
            'Принял ваш документ с прокси. Все документы успешно обработаны.'
        )
        # здесь вы можете добавить логику обработки документа с прокси
        await state.finish()

@dp.message_handler(lambda message: message.text == 'Посмотреть мои аккаунты')
async def show_accounts(message: types.Message):

    if not await is_user_in_channel(message.from_user.id):
        await bot.send_message(
            message.chat.id,
            'Чтобы пользоваться данным ботом, осуществите подписку на каналы Alpha Rescue',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Alpha Rescue', url='https://t.me/rescue_alpha'), InlineKeyboardButton(text='Rescue Parser', url='https://t.me/rescue_parser'))
        )
        return

    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if user:
        wb = openpyxl.Workbook()
        ws = wb.active

        local_file_path = f"accounts-{random.randint(1000000, 10000000)}.xlsx"

        # Добавляем заголовки в первую строку
        ws.append(["Address", "Private", "Proxy", "Last GM Date", "GM Strick", "XP"])

        accounts = user.records

        # Добавляем несколько строк данных
        for account in accounts:
            ws.append([account.address, account.private, account.proxy, account.date, account.GMstrick, account.XP])

        # Сохраняем книгу в файл

        wb.save(local_file_path)
        with open(local_file_path, 'rb') as file:
            await bot.send_document(message.chat.id, file)

        os.remove(os.getcwd() + f'\\{local_file_path}')

    session.close()

if __name__ == '__main__':
    executor.start_polling(dp)
