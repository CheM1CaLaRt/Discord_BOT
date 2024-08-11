import discord
from discord.ext import commands
import youtube_dl

# Создаем объект бота
bot = commands.Bot(command_prefix='!')

# Устанавливаем параметры youtube-dl для извлечения аудио
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Полный список радиостанций Radio Record
stations = {
    'record': 'http://air2.radiorecord.ru:805/rr_320',
    'pirate_station': 'http://air2.radiorecord.ru:805/ps_320',
    'trance': 'http://air2.radiorecord.ru:805/trance_320',
    'deep': 'http://air2.radiorecord.ru:805/deep_320',
    'house': 'http://air2.radiorecord.ru:805/house_320',
    'chillout': 'http://air2.radiorecord.ru:805/chil_320',
    'vip_house': 'http://air2.radiorecord.ru:805/vip_320',
    'techno': 'http://air2.radiorecord.ru:805/tehno_320',
    'progressive': 'http://air2.radiorecord.ru:805/progr_320',
    'russian_mixes': 'http://air2.radiorecord.ru:805/rus_320',
    'trap': 'http://air2.radiorecord.ru:805/trap_320',
    'future_house': 'http://air2.radiorecord.ru:805/fut_320',
    'minimal': 'http://air2.radiorecord.ru:805/mini_320',
    'hardstyle': 'http://air2.radiorecord.ru:805/teo_320',
    'goa_psy': 'http://air2.radiorecord.ru:805/goa_320',
    'russian_gold': 'http://air2.radiorecord.ru:805/gold_320',
    'pump': 'http://air2.radiorecord.ru:805/pump_320',
    'breaks': 'http://air2.radiorecord.ru:805/brks_320',
    'big_room': 'http://air2.radiorecord.ru:805/dub_320',
    'symphonic': 'http://air2.radiorecord.ru:805/symh_320',
    'hard_bass': 'http://air2.radiorecord.ru:805/tmd_320',
    'classic': 'http://air2.radiorecord.ru:805/cla_320',
    'jackin_house': 'http://air2.radiorecord.ru:805/jack_320',
    'ukraine_hits': 'http://air2.radiorecord.ru:805/ukr_320',
    'techno_fm': 'http://air2.radiorecord.ru:805/tecno_320',
    'tropical': 'http://air2.radiorecord.ru:805/trop_320',
    'progressive_psy': 'http://air2.radiorecord.ru:805/prog_320',
    'nu_disco': 'http://air2.radiorecord.ru:805/nud_320',
    'retro': 'http://air2.radiorecord.ru:805/rrretro_320',
    'drum_n_bass': 'http://air2.radiorecord.ru:805/dnb_320',
    'russian_club': 'http://air2.radiorecord.ru:805/rclub_320',
    'liquid_funk': 'http://air2.radiorecord.ru:805/liquid_320',
    'gabber': 'http://air2.radiorecord.ru:805/gab_320',
    'pop': 'http://air2.radiorecord.ru:805/pop_320',
    'drum_n_bass_rewind': 'http://air2.radiorecord.ru:805/dnbr_320',
    'deep_classic': 'http://air2.radiorecord.ru:805/dcl_320',
    'dubstep': 'http://air2.radiorecord.ru:805/dub_320',
    'k-pop': 'http://air2.radiorecord.ru:805/kpop_320',
    'rap': 'http://air2.radiorecord.ru:805/rap_320',
    'future_bass': 'http://air2.radiorecord.ru:805/fbas_320',
    'chillout_mixtapes': 'http://air2.radiorecord.ru:805/chill2_320',
    'speedy_tek': 'http://air2.radiorecord.ru:805/speed_320',
}


# Класс для управления аудиопотоком
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

    @classmethod
    async def from_url(cls, url, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename), data=data)


# Команда для подключения к голосовому каналу
@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not in a voice channel.")
        return

    channel = ctx.message.author.voice.channel
    await channel.connect()


# Команда для игры радио
@bot.command(name='play')
async def play(ctx, station_name: str):
    if ctx.voice_client is None:
        await ctx.send("Bot is not connected to a voice channel.")
        return

    if station_name not in stations:
        await ctx.send(f"Station {station_name} is not available. Available stations: {', '.join(stations.keys())}")
        return

    station_url = stations[station_name]
    async with ctx.typing():
        player = await YTDLSource.from_url(station_url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {station_name}')


# Команда для отключения от голосового канала
@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


# Запуск бота с токеном (замените "YOUR_TOKEN" на ваш реальный токен)
bot.run('YOUR_TOKEN')
