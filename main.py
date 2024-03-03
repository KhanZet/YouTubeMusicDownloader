import asyncio
import random
import subprocess
from pytube import YouTube

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandObject
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message

bot = Bot('7027329507:AAFCL5XLMXNq-ugAhIXfUG9gYLYFdP2P-e8', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


def download_youtube_audio(video_url):
    # Создаем объект YouTube для получения информации о видео
    yt = YouTube(video_url)

    # Название видео
    video_title = yt.title

    # Указание пути к ffmpeg
    ffmpeg_location = r'путь\к\ffmpeg\bin'  # Укажите ваш путь к ffmpeg

    # Имя выходного файла в формате MP3
    output_file_path = f"{video_title}.mp3"

    # Команда для скачивания аудио с использованием yt-dlp и добавления метаданных с ffmpeg
    command = [
        'yt-dlp',
        '-x',  # Извлекать аудио
        '--audio-format', 'mp3',  # Формат аудио
        '--audio-quality', '0',  # Качество аудио
        '--ffmpeg-location', ffmpeg_location,  # Указываем путь к ffmpeg
        '--postprocessor-args',
        f"ffmpeg:-metadata title=\"{video_title}\" -metadata artist=\"YT\"",  # Добавление метаданных
        video_url,
        '-o', output_file_path,  # Имя выходного файла
    ]

    # Выполнение команды
    result = subprocess.run(command, capture_output=True, text=True)

    # Проверяем, завершилась ли команда успешно
    if result.returncode == 0:
        print('Аудиодорожка скачана и сохранена как:', output_file_path)
        return output_file_path
    else:
        print('Произошла ошибка при скачивании аудиодорожки')
        return None


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Hi <b>{message.from_user.first_name}</b>")
    print(message)


@dp.message(Command(commands=["rn", "random-number"]))
async def random_number(message: Message, command: CommandObject):
    try:
        a, b = [int(n) for n in command.args.split("-")]
        rnum = random.randint(a, b)
        await message.reply(f"Random number from {a} to {b} is {rnum}")
    except ValueError:
        await message.reply(f"Invalid arguments")


@dp.message(F.text == "play")
async def play_games(message: Message):
    x = await message.answer_dice(DiceEmoji.DICE)
    print(x.dice.value)


@dp.message()
async def echo(message: Message):
    await message.answer(f"I don't understand u!")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
