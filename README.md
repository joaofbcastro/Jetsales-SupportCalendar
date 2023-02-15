# Support Calendar

Aplicação Discord responsável por captar as mensagens de novas reuniões enviadas por meio de Webhook e estilizar-las, além de auxiliar a equipe de suporte com lembretes ao se aproximar da hora da reunião.

## Iniciando o projeto

Subentendendo que você já tem o [Python](https://www.python.org/downloads/) instalado e está dentro de um [ambiente virtual](https://docs.python.org/pt-br/3/tutorial/venv.html), siga os passos abaixo para rodar o projeto.

Clone o repositório do projeto

```bash
git clone https://github.com/joaofbcastro/Jetsales-SupportCalendar.git
```

Entre na pasta do projeto

```bash
cd Jetsales-SupportCalendar
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` seguindo o modelo substituindo os valores.

```.env
BOT_TOKEN = XXXXXXXXXXXXXXXXX
GUILD_ID = XXXXXXXXXXXXXXXXX
SUPPORT_CHANNEL = XXXXXXXXXXXXXXXXX
SUPPORT_ROLE = XXXXXXXXXXXXXXXXX
```

Inicie a aplicação

```bash
python main.py
```

## Sincronizando os comandos

Com o bot online e dentro de um servidor, use o comando `sync`, conforme o gif abaixo:

![Sincronizando comandos do bot](https://i.imgur.com/xoT4NNM.gif)

## Criando um Webhook com o bot

Será necessário obter um Webhook criado pelo próprio bot, caso o Webhook utilizado para enviar as mensagens tenha sido criado por outro usuário, o bot não conseguirá editar a mensagem.

 - Caso o bot já tenha um Webhook existente no canal, este será retornado e um novo não será criado. Isso evita inúmeros Webhooks inativos.

![Como criar Webhook com o bot](https://i.imgur.com/lMS9PgB.gif)

## Efetuando um disparo de teste

Para verificar se está tudo dentro dos conformes você pode enviar um disparo com o Webhook. Você pode utilizar o site [Discohook](https://discohook.org/) para isso.

O modelo de mensagem a ser disparada no webhook é a abaixo:
 
 - Caso seja necessário mudar esse modelo de mensagem, o código precisará ser alterado.
  
```txt
Nome do Cliente: XXXXX XXXX
Nome da Empresa: XXX XXX XXXX
Url do Cliente: Objetivo da reunião.
Horário da Call: 03:00pm - Wednesday, February 10, 2025
Link da Call: https://calendly.com/events/XXX
Responsável pelo agendamento: XXXXX XXXX
```

![Realizando um envio de teste](https://i.imgur.com/s43esQE.gif)

## Autores

- [@joaofbcastro](https://www.github.com/joaofbcastro)

