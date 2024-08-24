from config import TOKEN, TXTROB, AUDIOROB, WEATHER_API_KEY
import discord
from discord.ext import commands
from gtts import gTTS
import os
import requests
from dotenv import load_dotenv
import asyncio


load_dotenv()

def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric',  # Используйте 'imperial' для Fahrenheit
        'lang': 'ru'  # Для русского языка
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get('cod') != 200:
        return "Не удалось получить данные о погоде. Проверьте название города."

    main = data['main']
    weather = data['weather'][0]
    description = weather['description']
    temperature = main['temp']
    city = data['name']

    return f"Куда Ты собираешься? Останься дома!\nПогода в {city}:\nТемпература: {temperature}°C\nОписание: {description.capitalize()}"



intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Словарь радиостанций
radio_stations = {
    "Gaming": "https://gaming.stream.laut.fm/gaming",
    "Record": "https://radiorecord.hostingradio.ru/rr_main96.aacp",
    "Tiesto": "https://radiorecord.hostingradio.ru/tiesto96.aacp",
    "David Guetta": "https://radiorecord.hostingradio.ru/guetta96.aacp",
    "Armin van Buuren": "https://radiorecord.hostingradio.ru/armin96.aacp",
    "Russian Mix": "https://radiorecord.hostingradio.ru/rus96.aacp",
    "Супердискотека 90-х": "https://radiorecord.hostingradio.ru/sd9096.aacp",
    "Russian Hits": "https://radiorecord.hostingradio.ru/russianhits64.aacp",
    "Chill-Out": "https://radiorecord.hostingradio.ru/chil96.aacp",
    "Deep": "https://radiorecord.hostingradio.ru/deep96.aacp",
    "Megamix": "https://radiorecord.hostingradio.ru/mix96.aacp",
    "Remix": "https://radiorecord.hostingradio.ru/rmx96.aacp",
    "Рекорд 00-х": "https://radiorecord.hostingradio.ru/200096.aacp",
    "Big Hits": "https://radiorecord.hostingradio.ru/bighits96.aacp",
    "Маятник Фуко": "https://radiorecord.hostingradio.ru/mf96.aacp",
    "Chill House": "https://radiorecord.hostingradio.ru/chillhouse96.aacp",
    "Trancemission": "https://radiorecord.hostingradio.ru/tm96.aacp",
    "Record 80-х": "https://radiorecord.hostingradio.ru/198096.aacp",
    "Rock": "https://radiorecord.hostingradio.ru/rock96.aacp",
    "Russian Gold": "https://radiorecord.hostingradio.ru/russiangold96.aacp",
    "Pirate Station": "https://radiorecord.hostingradio.ru/ps96.aacp",
    "Innocence": "https://radiorecord.hostingradio.ru/ibiza96.aacp",
    "Party 24/7": "https://radiorecord.hostingradio.ru/party96.aacp",
    "Record Gold": "https://radiorecord.hostingradio.ru/gold96.aacp",
    "Summer Dance": "https://radiorecord.hostingradio.ru/summerparty96.aacp",
    "На Хайпе": "https://radiorecord.hostingradio.ru/hype96.aacp",
    "Phonk": "https://radiorecord.hostingradio.ru/phonk96.aacp",
    "Руки Вверх!": "https://radiorecord.hostingradio.ru/rv96.aacp",
    "Rap Hits": "https://radiorecord.hostingradio.ru/rap96.aacp",
    "Rap Classics": "https://radiorecord.hostingradio.ru/rapclassics96.aacp",
    "Trance Classics": "https://radiorecord.hostingradio.ru/trancehits96.aacp",
    "VIP House": "https://radiorecord.hostingradio.ru/vip96.aacp",
    "Bass House": "https://radiorecord.hostingradio.ru/jackin96.aacp",
    "Organic": "https://radiorecord.hostingradio.ru/organic96.aacp",
    "Black Rap": "https://radiorecord.hostingradio.ru/yo96.aacp",
    "Summer Lounge": "https://radiorecord.hostingradio.ru/summerlounge64.aacp",
    "D'n'B Classics": "https://radiorecord.hostingradio.ru/drumhits96.aacp",
    "10's Dance": "https://radiorecord.hostingradio.ru/201096.aacp",
    "EDM": "https://radiorecord.hostingradio.ru/club96.aacp",
    "Lo-Fi": "https://radiorecord.hostingradio.ru/lofi96.aacp",
    "Workout": "https://radiorecord.hostingradio.ru/workout96.aacp",
    "Neurofunk": "https://radiorecord.hostingradio.ru/neurofunk96.aacp",
    "Breaks": "https://radiorecord.hostingradio.ru/brks96.aacp",
    "Tropical": "https://radiorecord.hostingradio.ru/trop96.aacp",
    "Tech House": "https://radiorecord.hostingradio.ru/techouse96.aacp",
    "Trap": "https://radiorecord.hostingradio.ru/trap96.aacp",
    "Liquid Funk": "https://radiorecord.hostingradio.ru/liquidfunk96.aacp",
    "Dubstep": "https://radiorecord.hostingradio.ru/dub96.aacp",
    "House Hits": "https://radiorecord.hostingradio.ru/househits96.aacp",
    "GOA/PSY": "https://radiorecord.hostingradio.ru/goa96.aacp",
    "Trancehouse": "https://radiorecord.hostingradio.ru/trancehouse96.aacp",
    "Ambient": "https://radiorecord.hostingradio.ru/ambient96.aacp",
    "TOP 100 EDM": "https://radiorecord.hostingradio.ru/top100edm96.aacp",
    "Dream Dance": "https://radiorecord.hostingradio.ru/dream96.aacp",
    "Techno": "https://radiorecord.hostingradio.ru/techno96.aacp",
    "Live DJ-sets": "https://radiorecord.hostingradio.ru/livedjsets96.aacp",
    "70's Dance": "https://radiorecord.hostingradio.ru/197096.aacp",
    "Technopop": "https://radiorecord.hostingradio.ru/technopop96.aacp",
    "Minimal/Tech": "https://radiorecord.hostingradio.ru/mini96.aacp",
    "Dream Pop": "https://radiorecord.hostingradio.ru/dreampop96.aacp",
    "House Classics": "https://radiorecord.hostingradio.ru/houseclss96.aacp",
    "Uplifting": "https://radiorecord.hostingradio.ru/uplift96.aacp",
    "Eurodance": "https://radiorecord.hostingradio.ru/eurodance96.aacp",
    "60's Dance": "https://radiorecord.hostingradio.ru/cadillac96.aacp",
    "Future Rave": "https://radiorecord.hostingradio.ru/futurerave96.aacp",
    "Future House": "https://radiorecord.hostingradio.ru/fut96.aacp",
    "UK Garage": "https://radiorecord.hostingradio.ru/ukgarage96.aacp",
    "Reggae": "https://radiorecord.hostingradio.ru/reggae96.aacp",
    "Disco/Funk": "https://radiorecord.hostingradio.ru/discofunk96.aacp",
    "Dancecore": "https://radiorecord.hostingradio.ru/dc96.aacp",
    "Hard Bass": "https://radiorecord.hostingradio.ru/hbass96.aacp",
    "Electro": "https://radiorecord.hostingradio.ru/elect96.aacp",
    "Old School": "https://radiorecord.hostingradio.ru/pump96.aacp",
    "Progressive": "https://radiorecord.hostingradio.ru/progr96.aacp",
    "EDM Classics": "https://radiorecord.hostingradio.ru/edmhits96.aacp",
    "Hardstyle": "https://radiorecord.hostingradio.ru/teo96.aacp",
    "Darkside": "https://radiorecord.hostingradio.ru/darkside96.aacp",
    "Synthwave": "https://radiorecord.hostingradio.ru/synth96.aacp",
    "Latina Dance": "https://radiorecord.hostingradio.ru/latina96.aacp",
    "Tecktonik": "https://radiorecord.hostingradio.ru/tecktonik96.aacp",
    "Future Bass": "https://radiorecord.hostingradio.ru/fbass96.aacp",
    "Гоп FM": "https://radiorecord.hostingradio.ru/gop96.aacp",
    "Midtempo": "https://radiorecord.hostingradio.ru/mt96.aacp",
    "Jungle": "https://radiorecord.hostingradio.ru/jungle96.aacp",
    "Hypnotic": "https://radiorecord.hostingradio.ru/hypno96.aacp",
    "Rave FM": "https://radiorecord.hostingradio.ru/rave96.aacp",
    "Moombahton": "https://radiorecord.hostingradio.ru/mmbt96.aacp",
    "2-step": "https://radiorecord.hostingradio.ru/2step96.aacp",
    "Медляк FM": "https://radiorecord.hostingradio.ru/mdl96.aacp",
    "Веснушка FM": "https://radiorecord.hostingradio.ru/deti96.aacp",
    "Groove/Tribal": "https://radiorecord.hostingradio.ru/groovetribal96.aacp",
    "Гастарбайтер FM": "https://radiorecord.hostingradio.ru/gast96.aacp",
    "Нафталин FM": "https://radiorecord.hostingradio.ru/naft96.aacp",
    "Симфония FM": "https://radiorecord.hostingradio.ru/symph96.aacp",
    "Complextro": "https://radiorecord.hostingradio.ru/complextro96.aacp",
    "Christmas Chill": "https://radiorecord.hostingradio.ru/christmaschill96.aacp",
    "Christmas": "https://radiorecord.hostingradio.ru/christmas96.aacp",
    "Русская Зима": "https://radiorecord.hostingradio.ru/ruszima96.aacp"
}


async def ensure_voice(ctx):
    if ctx.author.voice is None:
        await ctx.send("Пожалуйста, подключитесь к голосовому каналу!")
        return False
    return True


class RadioSelect(discord.ui.Select):
    def __init__(self, stations):
        options = [
            discord.SelectOption(label=station, description=station)
            for station in stations
        ]
        super().__init__(placeholder="Выберите радиостанцию...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        station = self.values[0]
        station_url = radio_stations.get(station)
        if station_url is None:
            await interaction.response.send_message("Эта радиостанция не найдена.")
            return

        if interaction.guild.voice_client is None:
            if interaction.user.voice is not None:
                await interaction.user.voice.channel.connect()
            else:
                await interaction.response.send_message("Пожалуйста, подключитесь к голосовому каналу!")
                return

        interaction.guild.voice_client.stop()
        ffmpeg_options = {
            'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        interaction.guild.voice_client.play(discord.FFmpegPCMAudio(station_url, **ffmpeg_options))

        # Сохраняем URL текущей радиостанции
        interaction.guild.voice_client.current_station_url = station_url

        await interaction.response.send_message(f"Начинаю жужать под {station}!")


class RadioMenu(discord.ui.View):
    def __init__(self, stations):
        super().__init__()
        self.add_item(RadioSelect(stations))


@bot.command(name='playradio')
@commands.has_permissions(administrator=True)
async def play_radio(ctx):
    if not await ensure_voice(ctx):
        return

    # Разбейте радиостанции на группы по 25
    station_groups = [list(radio_stations.keys())[i:i + 25] for i in range(0, len(radio_stations), 25)]
    for group in station_groups:
        view = RadioMenu(group)
        await ctx.send("Выберите радиостанцию из списка:", view=view)

@play_radio.error
async def play_radio_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет прав на использование этой команды.")

@bot.command(name='rob')
async def robert(ctx):
    if not await ensure_voice(ctx):
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

    # Создание аудиофайла с текстом "Роберт пидор"
    tts = gTTS(text=AUDIOROB, lang='ru')
    tts.save("robert.mp3")

    # Проигрывание аудиофайла
    ctx.voice_client.stop()
    ffmpeg_options = {
        'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio("robert.mp3", **ffmpeg_options), after=lambda e: print(f"Finished playing: {e}"))

    await ctx.send(TXTROB)

    # Удаление аудиофайла после проигрывания
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

    os.remove("robert.mp3")

@bot.command(name='vse')
async def vsjo(ctx):
    if not await ensure_voice(ctx):
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

        # Проигрывание аудиофайла
    ctx.voice_client.stop()
    ffmpeg_options = {
        'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio("vse.mp3", **ffmpeg_options))
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

@bot.command(name='ger')
async def german(ctx):
    if not await ensure_voice(ctx):
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

        # Проигрывание аудиофайла
    ctx.voice_client.stop()
    ffmpeg_options = {
        'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio("ger.mp3", **ffmpeg_options))
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

@bot.command(name='est')
async def estt(ctx):
    if not await ensure_voice(ctx):
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()

        # Проигрывание аудиофайла
    ctx.voice_client.stop()
    ffmpeg_options = {
        'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio("est.mp3", **ffmpeg_options))
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)


@bot.command(name='stopradio')
async def stop_radio(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Остановил радио и отключился от канала.")


@bot.command(name='погода')
async def weather(ctx, *, city: str):
    weather_info = get_weather(city)
    await ctx.send(weather_info)


@bot.event
async def on_voice_state_update(member, before, after):
    # Проверяем, если пользователь зашел в голосовой канал
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)

        # Получаем текстовый канал для отправки сообщения
        text_channel = discord.utils.get(member.guild.text_channels,
                                         name="general")  # Убедитесь, что текстовый канал существует

        # Если бот уже подключен к голосовому каналу
        if voice_client is not None:
            if voice_client.channel != voice_channel:
                await voice_client.move_to(voice_channel)  # Перемещаемся в другой канал
        else:
            # Если не подключен, подключаемся
            voice_client = await voice_channel.connect()

        # Сохраняем текущий поток, если радио уже играет
        current_station_url = getattr(voice_client, 'current_station_url', None)
        if voice_client.is_playing():
            voice_client.stop()  # Останавливаем текущее воспроизведение

        # Отправляем сообщение в чат
        if text_channel is not None:
            await text_channel.send(f"{member.display_name}, держи мандаринку!")

        await asyncio.sleep(1)

        # Воспроизводим MP3 файл
        ffmpeg_options = {
            'executable': r'C:\ffmpeg\bin\ffmpeg.exe',  # Укажите полный путь к ffmpeg.exe
        }
        voice_client.play(discord.FFmpegPCMAudio('est.mp3', **ffmpeg_options))

        # Ждем окончания воспроизведения
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Возобновляем радио, если ранее оно играло
        if current_station_url:
            voice_client.play(discord.FFmpegPCMAudio(current_station_url, **ffmpeg_options))


bot.run(TOKEN)
