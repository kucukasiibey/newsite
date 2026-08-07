import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from PyCharacterAI import get_client

app = Flask(__name__)
CORS(app)

token = os.environ.get("CAI_TOKEN")
character_id = "hBH_mAY7JFcX8nBIdabIs5ixJ2uW6rTdMRMfs1wAi-E"

client = None
chat_id = None

async def init_client():
    global client, chat_id
    client = await get_client(token=token)
    chat, greeting = await client.chat.create_chat(character_id)
    chat_id = chat.chat_id

@app.route("/mesaj", methods=["POST"])
def mesaj():
    user_message = request.json.get("message")

    async def get_reply():
        answer = await client.chat.send_message(character_id, chat_id, user_message)
        return answer.get_primary_candidate().text

    reply = asyncio.run(get_reply())
    return jsonify({"reply": reply})

if __name__ == "__main__":
    asyncio.run(init_client())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))