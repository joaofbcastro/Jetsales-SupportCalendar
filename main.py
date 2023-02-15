import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.remove_command("help")

    async def on_ready(self):
        print(f"[App] App started with {self.user.name}!")

        print("[App] Loading cogs...")
        for root, dirs, files in os.walk("./Cogs"):
            for directory in dirs:
                if directory == "__pycache__":
                    continue
                dir_path = f"{root}/{directory}"
                await self.LoadCog(dir_path)
        print(f"[App] All cogs loaded")

        activity = discord.Game(name="em manutenção.")
        await self.change_presence(status=discord.Status.dnd, activity=activity)

    async def LoadCog(self, root) -> None:
        files = os.listdir(root)
        for fileName in files:
            cogPath = f"{root[2:]}.{fileName[:-3]}".replace("/", ".")
            if fileName.endswith(".py"):
                await self.load_extension(cogPath)
                print(f"[App] {cogPath}, loaded!")


bot = Client()
print("[App] Starting app...")
bot.run(os.environ.get("BOT_TOKEN"))
