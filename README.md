# Support Calendar

Aplicação Discord responsável por captar as mensagens de novas reuniões enviadas por meio de webhook e estilizar-las, além de auxiliar a equipe de suporte com lembretes ao se aproximar da hora da reunião.

## Rodando o projeto

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

Crie um arquivo `.env` seguindo o modelo abaixo e substitua os valores.

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


## Autores

- [@joaofbcastro](https://www.github.com/joaofbcastro)

