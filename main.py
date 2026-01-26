import discord
import os
from flask import Flask
from threading import Thread

# 1. Flaskの設定（これがないとRenderに消される）
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderのポート指定に合わせる
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Discord Botの設定
TARGET_KEYWORDS = [
    # 1. 基本（カタカナ・ひらがな・英語）
    "センス", "せんす", "sense",
    
    # 2. 「センス」を含む単語（一部の例）
    "ナンセンス", "エッセンス", "センスアップ",
    
    # 3. 「センス」と読める漢字の組み合わせ
    "扇子",   # 本来の「せんす」
    "潜水",   # せん・すい
    "泉水",   # よくわからん単語のせんす1
    "仙水",   # よくわからん単語のせんす2
    "sensu",   # ローマ字センス
    "宣す",   # よくわからんセンス3
    "撰す",   # よくわからんセンス4
    "僭す",   # よくわからんセンス5
    "遷す",   # よくわからんセンス6
    "浅水",   # "せんす"い
    "先水",   # "せんす"い
    "千水",   # "せんす"い
]
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('--- ログイン完了 ---')
    print(f'Bot名: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if any(keyword in message.content for keyword in TARGET_KEYWORDS):
        await message.channel.send('今センスって言ったか？')

# 3. 実行（順番が大事です！）
if __name__ == "__main__":
    # まずWebサーバーを裏側で動かす
    print("Starting Web Server...")
    keep_alive()
    
    # 次にDiscord Botをメインで動かす
    print("Starting Discord Bot...")
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if token:
        try:
            client.run(token)
        except Exception as e:
            print(f"Error starting bot: {e}")
    else:
        print("Error: DISCORD_BOT_TOKEN is not set.")
