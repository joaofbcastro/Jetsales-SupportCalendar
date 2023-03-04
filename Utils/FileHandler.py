import os
import json
import discord
from datetime import datetime, timezone, timedelta


file_path = "./Data/EventsList.json"


def __read_file(file_path: str) -> None:
    """
    Retorna o arquivo, se não existir, será criado.

    Parameters
    ----------
    file_path: `str`
        O caminho para o arquivo.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except:
        path_split = file_path.split('/')
        path_split.pop(-1)
        dir_path = '/'.join(path_split)
        os.makedirs(dir_path)
        with open(file_path, "w") as file:
            file.write("[]")
        return __read_file(file_path)


def __write_file(file_path: str, file) -> None:
    """
    Escreve dados dentro do arquivo escolhido.

    Parameters
    ----------
    file_path: `str`
        O caminho para o arquivo.
    file:
        Os dados a serem escritos no arquivo.
    """
    with open(file_path, "w") as f:
        json.dump(file, f, indent=2)


def __message_to_dict(message: discord.Message) -> dict:
    """
    Transforma a mensagem enviada pelo Webhook em um dicionario Python.

    Parameters
    ----------
    message: `discord.Message`
        A mensagem que servirá de base para o dicionário.
    """
    keys = [
        "Nome do Cliente",
        "Link da Call",
        "Hora da Call",
        "Zap do Cliente",
        "Empresa do CLiente",
        "Objetivo da Call",
        "Responsável pelo agendamento"
    ]

    message_dict = {"Event ID": message.id}
    for i, line in enumerate(message.content.splitlines()):
        key = keys[i]
        value = line

        if key == "Hora da Call":
            call_datetime = datetime.strptime(value, "%d.%m.%Y %H:%M")
            value = round(datetime.timestamp(call_datetime)) + 7200

        message_dict[key] = value

    message_dict["Interessados"] = {
        "Lembrar30": [],
        "Lembrar15": [],
        "Lembrar10": [],
        "Lembrar5": []
    }
    return message_dict


def get_reminder_category(time: float) -> str:
    """
    Verifica em que categoria o intervalo de tempo se encaixa.

    Parameters
    ----------
    time: `float`
        O tempo em segundos a ser usado de referência.
    """
    reminder_category = ' '
    if time <= 300:
        reminder_category = 'Lembrar5'
    elif time <= 600:
        reminder_category = 'Lembrar10'
    elif time <= 900:
        reminder_category = 'Lembrar15'
    else:
        reminder_category = 'Lembrar30'
    print(time, reminder_category)
    return reminder_category


def get_all_events() -> list:
    """
    Retorna uma lista com todos os eventos armazenados no arquivo.
    """
    return __read_file(file_path)


def get_all_interested(event_id: int) -> list:
    """
    Retorna uma lista com todos os interessados no evento.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    """
    event = get_event(event_id)
    interested = []
    for reminder_list in event['Interessados'].values():
        for i in reminder_list:
            interested.append(i)
    return interested


def get_event(event_id: int) -> dict | None:
    """
    Busca o evento na lista de eventos.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    """
    file = __read_file(file_path)

    for event in file:
        if event['Event ID'] == event_id:
            return event
    return None


def get_event_embed(event_id: int) -> discord.Embed:
    """
    Busca o evento e retorna um `discord.Embed` com os dados do evento.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    """
    event = get_event(event_id)
    message_url = f"https://discord.com/channels/{os.environ.get('GUILD_ID')}/{os.environ.get('SUPPORT_CHANNEL')}/{event_id}"
    embed = discord.Embed(
        title=event['Nome do Cliente'].title(),
        color=0x58FF0F,
        url=message_url
    )
    embed.set_thumbnail(url="https://i.imgur.com/tlnAUP0.jpg")
    embed.add_field(
        name="Objetivo",
        value=f"> {event['Objetivo da Call']}",
        inline=False
    )
    embed.add_field(
        name="Informações do cliente",
        value=f"**Cliente**: {event['Nome do Cliente'].title()}\n**Empresa**: {event['Empresa do CLiente']}",
        inline=False
    )
    embed.add_field(
        name="Data da reunião",
        value=f"<t:{event['Hora da Call']}:F>",
        inline=False
    )
    embed.set_footer(
        text=f"Agendado por {event['Responsável pelo agendamento'].title()}")
    return embed


def insert_event(message: discord.Message) -> bool:
    """
    Adiciona um evento na lista de eventos.

    Parameters
    ----------
    message: `discord.Message`
        Mensagem a qual servirá de base para criar o evento.

    Returns
    -------
    `True`: Caso o evento seja criado.
    `False`: Caso o evento seja encontrado na lista de eventos.
    """
    if get_event(message):
        return False
    else:
        file = __read_file(file_path)
        event = __message_to_dict(message)
        file.append(event)
        __write_file(file_path, file)
        return True


def update_event(new_event: dict) -> None:
    """
    Atualiza um evento dentro da lista de eventos.

    Parameters
    ----------
    new_event: `dict`
        Um dicionário Python com os dados do evento.
    """
    events = get_all_events()
    for event in events:
        if event['Event ID'] == new_event['Event ID']:
            event_index = events.index(event)
            events[event_index] = new_event
    __write_file(file_path, events)


def remove_event(event_id: int) -> None:
    """
    Remove um evento da lista de eventos.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    """
    events = get_all_events()
    for event in events:
        if event['Event ID'] == event_id:
            events.remove(event)
    __write_file(file_path, events)


async def remind_users(self, event: dict, reminder: str) -> None:
    """
    Notifica os usuários interessados no evento.

    Parameters
    ----------
    event: `dict`
        Um dicionário Python com os dados do evento.
    reminder: `str`
        A categoria em de lembrete em que o evento se encontra.
    """
    for user_id in event['Interessados'][reminder]:
        user: discord.User = self.bot.get_user(user_id)
        message_url = f"https://discord.com/channels/{os.environ.get('GUILD_ID')}/{os.environ.get('SUPPORT_CHANNEL')}/{event['Event ID']}"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Detalhes", url=message_url))
        view.add_item(discord.ui.Button(label="Acessar reunião", url=event['Link da Call']))
        embed = get_event_embed(event['Event ID'])
        embed.clear_fields()
        embed.remove_footer()
        embed.set_thumbnail(url="https://i.imgur.com/92JXVus.png")
        embed.description = f"Esse é um lembrete da reunião que acontecerá <t:{event['Hora da Call']}:R> com o cliente **{event['Nome do Cliente']}**.\n\nSe não puder estar presente nessa reunião, favor comunicar ao seu gestor."
        try:
            await user.send(embed=embed, view=view)
        except:
            pass
        switch_to_next_reminder(event['Event ID'], user.id)


def insert_interested(event_id: int, interested_id: int) -> bool:
    """
    Insere um usuário interessado a ser lembrado do evento.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    interested_id: `int`
        O id do usuário que deseja ser lembrado do evento.

    Returns
    -------
    `True`: Caso o interessado seja adicionado a lista.
    `False`: Caso o interessado já esteja em uma das listas.
    """
    event = get_event(event_id)
    now = datetime.timestamp(datetime.utcnow())
    seconds_until = event['Hora da Call'] - now

    for reminder_list in event['Interessados'].values():
        if interested_id in reminder_list:
            return False

    reminder_category = get_reminder_category(seconds_until)
    event['Interessados'][reminder_category].append(interested_id)
    update_event(event)
    return True


def switch_to_next_reminder(event_id: int, interested_id: int) -> None:
    """
    Verifica em que posição dos lembretes o usuário se encontra e o passa para o proximo.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    interested_id: `int`
        O id do usuário que deseja ser lembrado do evento.
    """
    event = get_event(event_id)
    reminders: dict = event['Interessados']

    insert_in_next = False
    for reminder, interested in reminders.items():
        if insert_in_next:
            reminders[reminder].append(interested_id)
            break
        elif interested_id in interested:
            reminders[reminder].remove(interested_id)
            insert_in_next = True
    update_event(event)


def remove_interested(event_id: int, interested_id: int) -> None:
    """
    Remove um usuário das listas de interessados.

    Parameters
    ----------
    event_id: `int`
        O identificador do evento, ou id da mensagem.
    interested_id: `int`
        O id do usuário que deseja ser lembrado do evento.
    """
    event = get_event(event_id)

    for reminder, list in event['Interessados'].items():
        if interested_id in list:
            event['Interessados'][reminder].remove(interested_id)

    update_event(event)
