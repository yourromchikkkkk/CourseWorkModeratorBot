import logging
from aiogram import Bot, Dispatcher, executor, types
import time
import configurator
from filters import isAdminFilter, MemberCanRestrictFilter
from dictionary import bad_words, other_bot, other_lang

# log level
logging.basicConfig(level=logging.INFO)

# bot initialization
bot = Bot(token=configurator.TOKEN)
dp = Dispatcher(bot)

# filter activator
dp.filters_factory.bind(isAdminFilter)


# ban command (only for admins)
@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("This command must be a reply for a message!")
        return

    await message.bot.delete_message(chat_id=configurator.GROUP_ID, message_id=message.message_id)
    await message.bot.kick_chat_member(chat_id=configurator.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Користувач забанений\n"
                                         "Він не зможе попасти в цю бесіду, якщо його хтось не додасть :3")


# mute command (works improperly)
@dp.message_handler(is_admin=True, commands=["mute"], commands_prefix="!/")
async def cmd_mute(message: types.Message):
    if not message.reply_to_message:
        await message.reply("This command must be a reply for a message!")
        return

    await message.bot.ban_chat_member(chat_id=configurator.GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply("Користувач \"замучений\"\n"
                                         "Він не зможе тепер писати, поки його не \"розмутять\" :3")


# join message delete
@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: types.Message):
    await message.delete()
    await message.answer(f"Пампарам-пампарам,приветствую {message.from_user.first_name}!")


# left message delete
@dp.message_handler(content_types=["left_chat_member"])
async def on_user_left(message: types.Message):
    await message.delete()
    await message.answer(f"Користувач {message.from_user.first_name} покинув нас(")


# bot reaction to command /start
@dp.message_handler(commands=['start'])
async def starting(message):
    try:
        await message.reply('Воу, молодий, куда стартуєш, не в бесіді ж!\n'
                            'Жартую, я бот, написаний в ході вивчення курсу '
                            'Прикладого програмування студентом Мацуєвим Романом.')
    except OSError:
        print("StartingError - Sending again after 3 seconds!!!")
        time.sleep(3)
        await message.reply('Воу, молодий, куда стартуєш, не в бесіді ж!')
        await message.delete()


# bot reaction to command /help
@dp.message_handler(commands=['help'])
async def helper(message):
    try:
        await message.answer("Ти що, не програміст? Гугл допоможе!")
    except OSError:
        print("HelperError - Sending again after 3 seconds!!!")
        time.sleep(3)
        await message.answer("Ти що, не програміст? Гугл допоможе!")


# deleting words from list "bad_words"
@dp.message_handler()
async def filter_our_messages(message: types.Message):
    for i in range(0, len(bad_words)):
        if bad_words[i] in message.text.lower():
            try:
                await message.delete()
            except OSError:
                print("BadWordsError - Sending again after 3 seconds!!!")
                time.sleep(3)
                await message.delete()
                print(message.text + " delited")


## deleting words from list "other_lang"
@dp.message_handler()
async def filter_english_message(message: types.Message):
    for i in range(0, len(other_lang)):
        if other_lang[i] in message.text.lower():
            try:
                await message.delete()
            except OSError:
                print("BadWordsError - Sending again after 3 seconds!!!")
                time.sleep(3)
                await message.delete()
                print(message.text + " delited")
# bot sunning
if __name__ == '__main__':
    try:  # Пытаемся выполнить команду приведеную ниже
        executor.start_polling(dp, skip_updates=True)  # Запускаем бота
    except OSError:  # Игнорируем ошибку по таймауту, если телеграмм успел разорвать соединение сс времени прошлой сесии
        print("PollingError - Sending again after 5 seconds!!!")  # Выводим ошибку в консоль
        time.sleep(5)  # Делаем паузу в 5 секунд и выполняем команду приведеную ниже
        executor.start_polling(dp, skip_updates=True)  # Запускаем бота
