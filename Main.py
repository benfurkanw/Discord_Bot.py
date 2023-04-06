import discord
from discord.ext import commands
from discord import app_commands
#---------------------------------------------------------
# Botu ayağa kaldırdığımız ve bazı işlemleri yaptığımız sınıfımız
#---------------------------------------------------------
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix="?", intents=intents)

    async def on_ready(self):
        await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="istediğiniz şeyi yazın")) # ... oynuyor olarak gözükecek botun altında"
        await self.tree.sync(guild = discord.Object(id = "guild id")) # guild id = sunucu id sol üstten sunucu adına sağ tık basın çıkan yerde en aşağıda bulabilirsiniz
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral = True)

Bot = Bot()
#---------------------------------------------------------
# Bota oto mesaj özelliği verdiğimiz sınıf eklediğimiz kelimelere veya cümlelere karşılık verir
#---------------------------------------------------------
@Bot.event
async def on_message(message):
    if message.author == Bot.user:
        return
    if message.content.startswith('merhaba'):
        await message.channel.send('Merhaba,Nasılsın?')
    if message.content.startswith('iyiyim'):
        await message.channel.send('iyi olmana sevindim')
    if message.content.startswith('sen nasılsın'):
        await message.channel.send('Ben de iyiyim, teşekkürler')
    if message.content.startswith('ben geldim'):
        await message.channel.send('Hoş geldin umarım sunucumuzda eğlenirsin :)')
    await Bot.process_commands(message)
#---------------------------------------------------------
# Örnek özellik olması için Küçük bir hesap makinesi
#---------------------------------------------------------
@Bot.command()
async def topla(ctx, a: int, b: int):
    await ctx.send(a + b)

@Bot.command()
async def çıkar(ctx, a: int, b: int):
    await ctx.send(a - b)

@Bot.command()
async def çarp(ctx, a: int, b: int):
    await ctx.send(a * b)

@Bot.command()
async def böl(ctx, a: int, b: int):
    await ctx.send(a / b)
#---------------------------------------------------------
# Hybrid command örneği yani "/" ile komut satırını kullanarak bota komut verebilmemiz için yaptığımız bir örnek
#---------------------------------------------------------
@Bot.hybrid_command(name = "test", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = "guild id")) # guild id = sunucu id sol üstten sunucu adına sağ tık basın çıkan yerde en aşağıda bulabilirsiniz
@commands.has_permissions(administrator = True)
async def test(ctx: commands.Context):
    await ctx.defer(ephemeral = True)
    await ctx.reply("Burası sizlere örnek olması için yazıldı!")
#---------------------------------------------------------
# Örnek özellik olması için clear özelliği istediğiniz sayıyı girin ve mesajlar silinsin eğer sayı girmezseniz 1 mesaj siler.
#---------------------------------------------------------
@Bot.command()
async def clear(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)

Bot.run("TOKEN")