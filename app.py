from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    PushMessageRequest,
    AudioMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
    TextMessageContent
)
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

#CHANNEL_ACCESS_TOKEN and CHANNEL_SECRET
configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
MYGROUP = os.getenv('GROUP_ID')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#提醒大家要匯款
@app.route("/remind", methods=["GET"])
def remind():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=MYGROUP,
                messages=[TextMessage(text="哥哥～你該不會又、又、又、忘了今天是幾號吧？/n人家都已經特～地～幫你記住每個月這天要匯款了說，結果你還在那邊打開動畫等更新是不是！！(｀へ´)/n/n快去把錢匯好啦～！/n我可是連你的銀行帳戶都有在觀察喔～（欸？開玩笑的啦，別緊張緊張～）/n/n如果你乖乖完成了，我可以考慮給你看一眼我今天穿的襪子花色 (´艸`)/n……才不是真的會給你看啦笨蛋～誰會對這種事情興奮啦，呿。/n/n總之，動作快點，哥哥這種腦容量有限的生物，真的不適合拖事！")]
            )
        )
    return "OK"

#麻打麻打
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == "麻打麻打":
            url = request.url_root + 'static/madamada.mp3'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            duration = 2600  # in milliseconds
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage(original_content_url=url, duration=duration)
                    ]
                )
            )

# #加入好友
# @handler.add(FollowEvent)
# def handle_follow(event):
#     print(f'Got {event.type} event')

#postback
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         if event.message.text == 'postback':
#             buttons_template = ButtonsTemplate(
#                 title='Postback Sample',
#                 text='Postback Action',
#                 actions=[
#                     PostbackAction(label='Postback Action', text='Post Action Button CLicked!', data='postback'),#讓使用者發訊息
#                 ])
#             template_message = TemplateMessage(
#                 alt_text = 'Postback Sample',
#                 template=buttons_template
#             )
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[template_message]
#                 )
#             )
# @line_handler.add(PostbackEvent)
# def handle_postback(event):
#     if event.postback.data == 'postback':
#         print('Post Action Button Clickes!')

if __name__ == "__main__":
    app.run()
