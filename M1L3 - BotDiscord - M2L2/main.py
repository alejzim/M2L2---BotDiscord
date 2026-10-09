import discord
from discord.ext import commands
from discord import app_commands
import random
from pathlib import Path
import asyncio
import aiohttp

# =========================
# VARIABLES
# =========================

TOKEN = "TOKEN_DEL_BOT"  # Reemplazar por el token de tu bot
GUILD_ID = 1316540420536143883  # Reemplazar por el ID de tu servidor

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="$",
    intents=intents
)

# Carpeta donde están guardadas las imágenes
CARPETA = Path(__file__).parent / "Imagenes"


# =========================
# INICIO DEL BOT
# =========================

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        print(f"{bot.user} inició sesión y está listo.")
        print(f"✅ {len(synced)} comandos sincronizados.")

        for comando in synced:
            print(f" - /{comando.name}")

    except Exception as error:
        print(f"❌ Error sincronizando comandos: {error}")


# =========================
# /SALUDO
# =========================

@bot.tree.command(
    name="saludo",
    description="El bot te saluda."
)
async def saludo(interaction: discord.Interaction):

    await interaction.response.send_message(
        "¡Hola! ¿Cómo estás?"
    )


# =========================
# /SUMAR
# =========================

@bot.tree.command(
    name="sumar",
    description="Suma dos números."
)
@app_commands.describe(
    num1="Primer número",
    num2="Segundo número"
)
async def sumar(
    interaction: discord.Interaction,
    num1: float,
    num2: float
):

    resultado = num1 + num2

    await interaction.response.send_message(
        f"El resultado de {num1} + {num2} es **{resultado}**"
    )


# =========================
# /NUMERO_ALEATORIO
# =========================

@bot.tree.command(
    name="numero_aleatorio",
    description="Genera un número aleatorio."
)
@app_commands.describe(
    num1="Número mínimo",
    num2="Número máximo"
)
async def numero_aleatorio(
    interaction: discord.Interaction,
    num1: int = 1,
    num2: int = 100
):

    if num1 > num2:
        await interaction.response.send_message(
            "❌ El número mínimo no puede ser mayor que el máximo.",
            ephemeral=True
        )
        return

    # =========================
    # EASTER EGG 67
    # =========================

    if num1 == 67 and num2 == 67:

        await interaction.response.send_message(
            "# ¡Six Seven!"
        )

        imagen = CARPETA / "67.jpg"

        if imagen.exists():

            await interaction.followup.send(
                file=discord.File(imagen)
            )

        else:

            await interaction.followup.send(
                f"❌ No encontré el archivo `67.jpg`.\n"
                f"📁 Busqué en: `{imagen}`"
            )

        return

    # =========================
    # GENERAR NÚMERO
    # =========================

    numero = random.randint(num1, num2)

    await interaction.response.send_message(
        f"🎲 Tu número aleatorio entre **{num1}** y **{num2}** "
        f"está siendo generado..."
    )

    await asyncio.sleep(2)

    mensaje2 = await interaction.followup.send(
        "✅ Tu número aleatorio se ha generado correctamente...",
        wait=True
    )

    await asyncio.sleep(1)

    await interaction.followup.send(
        f"🎯 Tu número aleatorio entre **{num1}** y **{num2}** es: **{numero}**"
    )

    await mensaje2.delete()

    # =========================
    # DADO ALEATORIO
    # =========================

    dado_numero = random.randint(1, 6)

    archivo_dado = CARPETA / f"dado{dado_numero}.jpg"

    if archivo_dado.exists():

        await interaction.followup.send(
            content=f"🎲 Dado: **{dado_numero}**",
            file=discord.File(archivo_dado)
        )

    else:

        await interaction.followup.send(
            f"🎲 Dado: **{dado_numero}**\n"
            f"⚠️ No encontré `dado{dado_numero}.jpg`.\n"
            f"📁 Busqué en: `{archivo_dado}`"
        )


# =========================
# /BORRAR_MENSAJES
# =========================

@bot.tree.command(
    name="borrar_mensajes",
    description="Borra mensajes del canal."
)
@app_commands.describe(
    cantidad="Cantidad de mensajes que querés borrar"
)
@app_commands.checks.has_permissions(manage_messages=True)
async def borrar_mensajes(
    interaction: discord.Interaction,
    cantidad: int = 1
):

    if cantidad < 1:

        await interaction.response.send_message(
            "❌ La cantidad debe ser al menos 1.",
            ephemeral=True
        )

        return

    if cantidad > 100:

        await interaction.response.send_message(
            "❌ Solo podés borrar hasta 100 mensajes de una vez.",
            ephemeral=True
        )

        return

    await interaction.response.defer(
        ephemeral=True
    )

    deleted = await interaction.channel.purge(
        limit=cantidad
    )

    await interaction.followup.send(
        f"🗑️ Se borraron **{len(deleted)} mensajes**.",
        ephemeral=True
    )


# =========================
# ERROR DE /BORRAR_MENSAJES
# =========================

@borrar_mensajes.error
async def borrar_mensajes_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    if isinstance(error, app_commands.MissingPermissions):

        await interaction.response.send_message(
            "❌ No tenés permisos para borrar mensajes.",
            ephemeral=True
        )

    else:

        print(f"Error en /borrar_mensajes: {error}")

        if not interaction.response.is_done():

            await interaction.response.send_message(
                "❌ Ocurrió un error intentando borrar los mensajes.",
                ephemeral=True
            )


# =========================
# /SPAM
# =========================

@bot.tree.command(
    name="spam",
    description="Envía varias veces un mensaje."
)
@app_commands.describe(
    cantidad="Cantidad de mensajes (máximo 67)",
    mensaje="Mensaje que querés enviar"
)
async def spam(
    interaction: discord.Interaction,
    cantidad: int,
    mensaje: str
):

    # Validar cantidad
    if cantidad < 1 or cantidad > 67:

        await interaction.response.send_message(
            "⚠️ La cantidad debe estar entre **1 y 67**.",
            ephemeral=True
        )

        return

    # Validar mensaje vacío
    if not mensaje.strip():

        await interaction.response.send_message(
            "❌ El mensaje no puede estar vacío.",
            ephemeral=True
        )

        return

    # Validar largo
    if len(mensaje) > 2000:

        await interaction.response.send_message(
            "❌ El mensaje no puede tener más de **2000 caracteres**.",
            ephemeral=True
        )

        return

    # Confirmación privada
    await interaction.response.send_message(
        f"✅ Enviando **{cantidad} mensajes**...",
        ephemeral=True
    )

    try:

        for _ in range(cantidad):

            await interaction.channel.send(mensaje)

            await asyncio.sleep(0.8)

    except discord.Forbidden:

        await interaction.followup.send(
            "❌ No tengo permisos para enviar mensajes en este canal.",
            ephemeral=True
        )

    except discord.HTTPException as error:

        await interaction.followup.send(
            "❌ Discord produjo un error mientras intentaba enviar los mensajes.",
            ephemeral=True
        )

        print(f"Error HTTP en /spam: {error}")

    except Exception as error:

        await interaction.followup.send(
            "❌ Ocurrió un error inesperado en `/spam`.",
            ephemeral=True
        )

        print(f"Error inesperado en /spam: {error}")

# =========================
# Memes
# =========================

BASE_DIR = Path(__file__).resolve().parent
CARPETA_IMAGENES = BASE_DIR / "Imagenes"

MEME_API = "https://meme-api.com/gimme"


# =========================
# Funciones
# =========================

def lectura_meme(numero_meme: int):
    ruta = CARPETA_IMAGENES / f"meme{numero_meme}.png"

    if not ruta.exists():
        return None

    return discord.File(str(ruta))


async def obtener_meme_api():
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout) as session:

        # Intentamos varias veces por si sale NSFW o spoiler
        for _ in range(5):
            try:
                async with session.get(MEME_API) as response:

                    if response.status != 200:
                        continue

                    datos = await response.json()

                    # Evitar contenido NSFW
                    if datos.get("nsfw", False):
                        continue

                    # Evitar spoilers
                    if datos.get("spoiler", False):
                        continue

                    # Verificar que tenga imagen
                    if not datos.get("url"):
                        continue

                    return datos

            except (aiohttp.ClientError, TimeoutError):
                continue

    return None


# =========================
# /meme
# =========================

@bot.tree.command(
    name="meme",
    description="Envía un meme local."
)
@app_commands.describe(
    numero_meme="Número del meme (1-12). Poné 0 o dejalo vacío para uno aleatorio."
)
async def meme(
    interaction: discord.Interaction,
    numero_meme: app_commands.Range[int, 0, 67] = 0
):
    # Si pone 0 o no pone nada:
    # meme local aleatorio del 1 al 12
    if numero_meme == 0:
        numero_meme = random.randint(1, 12)

    # =========================
    # Six Seven
    # =========================

    if numero_meme == 67:
        await interaction.response.send_message(
            "¡Six Seven!"
        )

        imagen = CARPETA_IMAGENES / "67.jpg"

        if imagen.exists():
            await interaction.followup.send(
                file=discord.File(str(imagen))
            )
        else:
            await interaction.followup.send(
                f"❌ No encontré el archivo `67.jpg`.\n"
                f"📁 Busqué en: `{imagen}`"
            )

        return

    # =========================
    # Validación
    # =========================

    if numero_meme < 1 or numero_meme > 12:
        await interaction.response.send_message(
            "❌ Número de meme inválido.\n"
            "Usá del **1 al 12**, `0` para uno aleatorio "
            "o `67` para **Six Seven**."
        )
        return

    # =========================
    # Enviar meme local
    # =========================

    imagen = lectura_meme(numero_meme)

    if imagen is None:
        ruta = CARPETA_IMAGENES / f"meme{numero_meme}.png"

        await interaction.response.send_message(
            f"❌ No encontré `meme{numero_meme}.png`.\n"
            f"📁 Busqué en: `{ruta}`"
        )
        return

    await interaction.response.send_message(
        file=imagen
    )


# =========================
# /memeapi
# =========================

@bot.tree.command(
    name="memeapi",
    description="Envía un meme aleatorio de Internet."
)
async def memeapi(
    interaction: discord.Interaction
):
    # Avisamos a Discord que la respuesta puede tardar
    await interaction.response.defer()

    datos = await obtener_meme_api()

    if datos is None:
        await interaction.followup.send(
            "❌ No pude obtener un meme de la API."
        )
        return

    # =========================
    # Datos del meme
    # =========================

    titulo = datos.get("title", "Meme")
    imagen_url = datos.get("url")

    subreddit = datos.get("subreddit", "desconocido")
    autor = datos.get("author", "desconocido")
    ups = datos.get("ups", 0)
    post_link = datos.get("postLink")

    # =========================
    # Embed
    # =========================

    embed = discord.Embed(
        title=titulo,
        color=discord.Color.random()
    )

    embed.set_image(
        url=imagen_url
    )

    embed.set_footer(
        text=(
            f"r/{subreddit} • "
            f"👍 {ups} • "
            f"u/{autor}"
        )
    )

    # Link al post original
    if post_link:
        embed.url = post_link

    await interaction.followup.send(
        embed=embed
    )

# =========================
#         Juegos
# =========================
@bot.tree.command(
    name="8ball",
    description="Haz una pregunta al 8-ball."
)
async def eight_ball(
    interaction: discord.Interaction,
    pregunta: str
):
    respuestas = [
        "Sí.",
        "No.",
        "Tal vez.",
        "Definitivamente.",
        "No cuentes con ello.",
        "Pregunta de nuevo más tarde.",
        "Es cierto.",
        "No es cierto."
    ]

    respuesta = random.choice(respuestas)

    await interaction.response.send_message(
        f"🎱 Pregunta: {pregunta}\n"
        f"Respuesta: **{respuesta}**"
    )
# -------------------------
#  Piedra, Papel o tijera
# ------------------------
@bot.tree.command(
    name="ppt",
    description="Juega Piedra, Papel o Tijera."
)
@app_commands.choices(
    mensaje=[
        app_commands.Choice(name="Piedra", value=1),
        app_commands.Choice(name="Papel", value=2),
        app_commands.Choice(name="Tijera", value=3)
    ]
)
async def ppt(
    interaction: discord.Interaction,
    mensaje: app_commands.Choice[int]
):
    imagen = CARPETA_IMAGENES / "ppt.png"

    await interaction.response.send_message(
        "¡Vamos a jugar Piedra, Papel o Tijera!",
        file=discord.File(imagen)
    )

    mensaje_ppt = await interaction.followup.send("Pensando...")

    ppt_numero = random.randint(1, 3)

    opciones = {
        1: "Piedra",
        2: "Papel",
        3: "Tijera"
    }

    await interaction.followup.send(
        f"Elegiste: **{opciones[mensaje.value]}**\n"
        f"Elegí: **{opciones[ppt_numero]}**"
    )

    await asyncio.sleep(1)
    await mensaje_ppt.delete()

    mensaje_resultado_ppt = await interaction.followup.send(
        "Generando resultado..."
    )

    await asyncio.sleep(1)

    if mensaje.value == ppt_numero:
        await interaction.followup.send("¡Empate!")
    elif (
        (mensaje.value == 1 and ppt_numero == 3) or
        (mensaje.value == 2 and ppt_numero == 1) or
        (mensaje.value == 3 and ppt_numero == 2)
    ):
        await interaction.followup.send("¡Ganaste! 🎉")
    else:
        await interaction.followup.send("¡Perdiste! 😢")

    await mensaje_resultado_ppt.delete()
    
# =========================
# ERROR GLOBAL
# =========================

@bot.tree.error
async def error_global(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    print(f"Error de comando: {error}")

    # Evita responder dos veces si el comando ya manejó el error
    if interaction.response.is_done():
        return

    await interaction.response.send_message(
        "❌ Ocurrió un error ejecutando el comando.",
        ephemeral=True
    )


# =========================
# EJECUCIÓN
# =========================

print("Bot is starting...")

bot.run(TOKEN)