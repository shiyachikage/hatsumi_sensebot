import discord
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. Render常時起動用のおまじない (Flask)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Renderが指定するポート番号を最優先で使うように修正
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. メンテナンス特化型：検知ワード設定
# ==========================================
# 反応させたい単語をここに追加するだけでOK
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
]
# ==========================================
# 3. Botのメイン処理
# ==========================================
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'--- ログイン完了 ---')
    print(f'Bot名: {client.user.name}')
    print(f'監視ワード: {", ".join(TARGET_KEYWORDS)}')
    print(f'--------------------')

@client.event
async def on_message(message):
    # 自分のメッセージには反応しない
    if message.author == client.user:
        return

    # メッセージの中にターゲットワードが含まれているかチェック
    if any(keyword in message.content for keyword in TARGET_KEYWORDS):
        await message.channel.send('今センスって言ったか？')

# ==========================================
# 4. 実行
# ==========================================
if __name__ == "__main__":
    # Webサーバーを別スレッドで起動
    keep_alive()
    
    # Discord Botを起動
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        client.run(token)
    else:
        print("エラー: DISCORD_BOT_TOKEN が設定されていません。")
