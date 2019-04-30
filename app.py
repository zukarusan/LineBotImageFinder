# mybot/app.py
import os
from decouple import config
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
from google_images_search import GoogleImagesSearch

app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)
import random

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def search_g(query):
    gis = GoogleImagesSearch('AIzaSyBjMfb1TfPfhDRKbzyK9E6cDypYXHEbhQw', '000266786199815297998:e1orac7unwo')
    num = random.randint(1, 4)
    gis.search({'q':query, 'num':num})
    result = ""
    for image in gis.results():
        if (image.url.lower().find("https") == 0):
            result = image.url
    return result


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    query = event.message.text
    temp = query.lower()
    if (temp.find("pic ") == 0):
        query = query[4::]
        result = search_g(query)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=result, preview_image_url=result)
        )




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)