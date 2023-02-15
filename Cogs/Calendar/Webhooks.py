import os
import discord
from asyncio import sleep
from datetime import datetime
from discord.ext import commands, tasks
import Utils.FileHandler as fHandler


class NotificationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def insert_interested(self, inter: discord.Interaction) -> None:
        channel = await inter.client.fetch_channel(os.environ.get("SUPPORT_CHANNEL"))
        channel_webhooks = await channel.webhooks()
        bot_webhooks = [wh for wh in channel_webhooks if wh.user == inter.client.user]
        if not bot_webhooks:
            return
        webhook = bot_webhooks[0]
        webhook_msg = await webhook.fetch_message(inter.message.id)

        embed = webhook_msg.embeds[0]
        for field in embed.fields:
            if field.name == "Interessados" and field.value.find(str(inter.user.id)) > -1:
                return
            if field.name == "Interessados":
                field_index = embed.fields.index(field)
                field.value += f", <@{inter.user.id}>"

                embed.set_field_at(field_index, name=field.name, value=field.value)
                return await webhook_msg.edit(embed=embed)

        embed.add_field(name="Interessados", value=f"<@{inter.user.id}>")
        return await webhook_msg.edit(embed=embed)

    @discord.ui.button(label="Quero que me lembre!", custom_id="btn_lembrar", style=discord.ButtonStyle.green)
    async def btn_lembrar(self, inter: discord.Interaction, button: discord.Button):
        await inter.response.defer(thinking=True, ephemeral=True)
        interested_inserted = fHandler.insert_interested(inter.message.id, inter.user.id)
        if interested_inserted:
            await self.insert_interested(inter)
            message = f"Te adicionei aos interessados 👍!!"
            try:
                await inter.user.send("Quando estiver próximo à reunião, te lembrarei por aqui.")
            except:
                message += f"\nVocê deve habilitar o recebimento de mensagens diretas para ser lembrado(a).\nhttps://i.imgur.com/O1qAe1F.gif"
        else:
            message = f"Você já está na lista de interessados!!"

        await inter.edit_original_response(content=message)


class Webhooks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.event_reminder.start()

    def cog_load(self) -> None:
        self.bot.add_view(NotificationButtons())

    def cog_unload(self) -> None:
        self.event_reminder.cancel()

    async def disable_event_button(self, message_id: int) -> None:
        channel = await self.bot.fetch_channel(os.environ.get("SUPPORT_CHANNEL"))
        channel_webhooks = await channel.webhooks()
        bot_webhooks = [wh for wh in channel_webhooks if wh.user == self.bot.user]
        if not bot_webhooks:
            return

        webhook = bot_webhooks[0]
        webhook_msg = await webhook.fetch_message(message_id)
        await webhook_msg.edit(view=None)

    async def get_webhook(self) -> discord.Webhook | None:
        channel = await self.bot.fetch_channel(os.environ.get("SUPPORT_CHANNEL"))
        channel_webhooks = await channel.webhooks()
        bot_webhooks = [wh for wh in channel_webhooks if wh.user == self.bot.user]
        if not bot_webhooks:
            return None
        return bot_webhooks[0]
        
    async def mention_support_role(self, event: dict):
        webhook = await self.get_webhook()
        webhook_msg = await webhook.fetch_message(event['Event ID'])

        embed = webhook_msg.embeds[0]
        for field in embed.fields:
            if field.name == "Interessados":
                return

        embed.add_field(name="Interessados", value=f"<@&{os.environ.get('SUPPORT_ROLE')}>")
        await webhook_msg.edit(embed=embed)
        await webhook_msg.reply(f"**<@&{os.environ.get('SUPPORT_ROLE')}>. Essa reunião começara em breve e ninguém clicou para ser lembrado.**")
        return

    @tasks.loop(seconds=60)
    async def event_reminder(self) -> None:
        print('Looping...')
        now = datetime.timestamp(datetime.now())
        events = fHandler.get_all_events()
        for event in events:
            seconds_until = event['Horário da Call'] - now
            interested = fHandler.get_all_interested(event['Event ID'])
            if seconds_until > 1800:
                continue
            elif seconds_until <= 0:
                fHandler.remove_event(event['Event ID'])
                await self.disable_event_button(event['Event ID'])
                continue
            elif seconds_until <= 1800 and not interested:
                await self.mention_support_role(event)

            reminder_category = fHandler.get_reminder_category(seconds_until)
            await fHandler.remind_users(self, event, reminder_category)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user or not message.webhook_id:
            return

        webhook = await self.bot.fetch_webhook(message.webhook_id)
        if webhook.user != self.bot.user:
            return

        fHandler.insert_event(message)
        event = fHandler.get_event(message.id)

        webhook_msg = await webhook.fetch_message(message.id)

        await sleep(3)
        view = NotificationButtons()
        embed = fHandler.get_event_embed(event['Event ID'])
        embed.description = f"Para acessar a reunião basta [clicar aqui]({event['Link da Call']}). Vale lembrar que a reunião acontecerá acontecerá <t:{event['Horário da Call']}:R>."
        await webhook_msg.edit(content=None, embed=embed, view=view)

    @discord.app_commands.command(name="criar_webhook")
    async def criar_webhook(self, inter: discord.Interaction) -> None:
        """
        Cria um webhook com o próprio bot.
        """
        channel_webhooks = await inter.channel.webhooks()
        bot_webhooks = [wh for wh in channel_webhooks if wh.user == self.bot.user]
        if not bot_webhooks:
            new_webhook = await inter.channel.create_webhook(name="Calendar")
            bot_webhooks.append(new_webhook)

        content = f"Essa aplicação tem `{len(bot_webhooks)}` webhook(s) ativo(s) nesse canal."
        for wh in bot_webhooks:
            content = content + f"\n> ID: `{wh.id}` URL:{wh.url}\n"

        await inter.response.send_message(content=content, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Webhooks(bot), guild=discord.Object(os.environ.get("GUILD_ID")))
