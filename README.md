# Argos Bot

Bot do Telegram para baixar vídeos do YouTube, Instagram, TikTok e Facebook.

## Requisitos

- Python 3.11+
- ffmpeg

## Instalação

```bash
pip install -r requirements.txt
cp .env.example .env
# Edite .env e adicione seu BOT_TOKEN
```

## Uso

```bash
python main.py
```

Envie um link de vídeo no chat do bot e ele retornará o vídeo baixado.

> **Limite:** O Telegram aceita arquivos de até 50 MB via bot.
