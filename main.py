import discord
import os

# --- 設定エリア：ここを編集してワードを追加 ---
# 反応したい単語をこのリストに自由に追加してください
TARGET_KEYWORDS = [
    # 1. 基本（カタカナ・ひらがな・英語）
    "センス", "せんす", "sense",
    
    # 2. 「センス」を含む単語（一部の例）
    "ナンセンス", "エッセンス", "センスアップ",
    
    # 3. 「センス」と読める漢字の組み合わせ
    "扇子",   # 本来の「せんす」
    "潜水",   # せん・すい
    "洗剤",   # せん・ざい
    "先取",   # せん・しゅ
    "戦術",   # せん・じゅつ
    "千手",   # せん・じゅ
    "宣誓",   # せん・せい
    "選出",   # せん・しゅつ
    "泉州",   # せん・しゅう
]
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ 監視を開始しました（登録ワード数: {len(TARGET_KEYWORDS)}）')

@client.event
async def on_message(message):
    # Bot自身の発言には反応しない
    if message.author == client.user:
        return

    # メッセージを判定用に加工（小文字化）
    content = message.content.lower()

    # 判定実行
    # TARGET_KEYWORDSの中のどれか一つでもメッセージに含まれていればTrue
    is_detected = any(word in content for word in TARGET_KEYWORDS)

    if is_detected:
        await message.channel.send("今センスって言ったか？")

# 環境変数からトークンを読み込み
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    client.run(token)
else:
    print("Error: DISCORD_BOT_TOKEN が設定されていません。")
