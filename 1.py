import discord
from discord.ext import commands
import youtube_dl
from config import TOKEN

# Настройка бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ссылка на радио поток
RADIO_URL = "https://radiorecord.hostingradio.ru/phonk96.aacp"


# Проверяем, есть ли у пользователя подключение к голосовому каналу
async def ensure_voice(ctx):
    if ctx.author.voice is None:
        await ctx.send("Пожалуйста, подключитесь к голосовому каналу!")
        return False
    return True


# Команда для подключения к голосовому каналу и начала воспроизведения радио
@bot.command(name='playradio')
async def play_radio(ctx):
    if not await ensure_voice(ctx):
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

    ctx.voice_client.stop()
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio(RADIO_URL, **ffmpeg_options))

    await ctx.send("Начинаю воспроизводить радио Record Phonk!")


# Команда для остановки воспроизведения
@bot.command(name='stopradio')
async def stop_radio(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Остановил радио и отключился от канала.")


# Запуск бота
bot.run(TOKEN)
