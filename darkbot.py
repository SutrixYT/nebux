from discord.ext import commands

client = commands.Bot(command_prefix="-")
player_dict = dict()


@client.event
async def on_ready():
    print("Bot ist bereit")


@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice = client.voice_client_in(server)
    player = await voice.create_ytdl_player(url)
    player_dict[server.id] = player
    await client.send_message(ctx.message.channel, "Hoffe es funktoniert! Jetzt läuft `%s` " % player.title)
    player.start()


@client.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.stop()
    del player_dict[server.id]


@client.command(pass_context=True)
async def pause (ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.pause()


@client.command(pass_context=True)
async def resume (ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.resume()


@client.command(pass_context=True)
async def loop (ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    await client.send_message(ctx.message.channel, "Loop aktiviert für `%s` " % player.title)
    player.play()

client.run(os.getenv('Token'))
