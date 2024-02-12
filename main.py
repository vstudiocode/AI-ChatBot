import pytgpt.gpt4free as provider
import nest_asyncio

import discord
from discord.ext import commands

nest_asyncio.apply()
ai = provider.GPT4FREE(provider="You")

def parse_dotenv():
    env = {}

    with open(".env", "r") as env_file:
        for line in env_file.readlines():
            line = line.strip()
            if not line or line[0] == "#":
                continue
            key, value = line.split("=", 1)
            env[key] = value
            
    return env

env = parse_dotenv()

intents = discord.Intents.default()
intents.members = True

bot_token = env["BOT_TOKEN"]

bot = commands.Bot(command_prefix='!', intents=intents)

async def process_message_with_ai(content):
    return ai.chat(content)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("@me with your prompt"))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message: commands.clean_content):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        message_to_edit = await message.reply("<a:loading:1204153312748769330> Processing...")
        content = message.content.replace("<@1204147459635417169> ", "")
        try:
            response = await process_message_with_ai(content)
            if len(response) > 2000:
                with open('response.txt', 'w') as f:
                    f.write(response)
                
                await message_to_edit.edit(content="<a:loading:1204153312748769330> Uploading...")
                await message_to_edit.reply(file=discord.File('response.txt'))

            else:
                await message_to_edit.edit(content=str(response))
        except Exception as e:
            await message_to_edit.edit(content=f"Error: {str(e)}")

    # await bot.process_commands(message)
    # This isn't needed as the bot doesn't have any commands

bot.run(bot_token)
