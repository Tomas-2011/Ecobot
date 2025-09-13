import discord
import requests

# Intents de Discord
intents = discord.Intents.default()
intents.message_content = True  # NECESARIO para leer mensajes
client = discord.Client(intents=intents)

# Tokens
DISCORD_TOKEN = "MTQwODg4NDE5Mzc2MDY0MTIzNg.Gn-XbD.6dbUchHM7I2tm_eBuvk_MQ2AjQNMZf2IeyOtig"   # 🔥 Usa el token regenerado
METEOBLUE_API_KEY = "y5Nw4rmdPbMVu3vL"

# Función para obtener clima
def get_weather(lat, lon):
    url = (
        f"https://my.meteoblue.com/packages/basic-1h?"
        f"lat={lat}&lon={lon}&apikey={METEOBLUE_API_KEY}"
    )
    resp = requests.get(url).json()
    if "data_1h" not in resp:
        return "⚠️ No se pudo obtener el clima."
    temp = resp["data_1h"]["temperature"][0]
    return f"🌤️ Clima: {temp}°C (dato de la última hora)"

# Función para obtener calidad del aire
def get_air_quality(lat, lon):
    url = (
        f"https://my.meteoblue.com/packages/basic-1h?"
        f"lat={lat}&lon={lon}&apikey={METEOBLUE_API_KEY}"
    )
    resp = requests.get(url).json()
    if "data_1h" in resp and "pm2_5" in resp["data_1h"]:
        pm25 = resp["data_1h"]["pm2_5"][0]
        if pm25 <= 12:
            nivel = "Muy bueno ✅"
        elif pm25 <= 35.4:
            nivel = "Bueno 🙂"
        elif pm25 <= 55.4:
            nivel = "Moderado 😐"
        else:
            nivel = "Malo 😷"
        return f"🌍 Calidad del aire (PM2.5): {pm25} µg/m³ → {nivel}"
    else:
        return "ℹ️ Calidad del aire no disponible con este paquete."

@client.event
async def on_ready():
    print(f"✅ Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith("!clima"):
        try:
            _, lat, lon = msg.split()
            lat, lon = float(lat), float(lon)
            await message.channel.send(get_weather(lat, lon))
        except:
            await message.channel.send("📍 Usa: `!clima [lat] [lon]`")

    elif msg.startswith("!aire"):
        try:
            _, lat, lon = msg.split()
            lat, lon = float(lat), float(lon)
            await message.channel.send(get_air_quality(lat, lon))
        except:
            await message.channel.send("📍 Usa: `!aire [lat] [lon]`")

client.run("MTQwODg4NDE5Mzc2MDY0MTIzNg.Gn-XbD.6dbUchHM7I2tm_eBuvk_MQ2AjQNMZf2IeyOtig")
