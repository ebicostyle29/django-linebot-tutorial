from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import pya3rt


line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)
# talk_api = settings.TALK_API

class CallbackView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):

        signature = request.META['HTTP_X_LINE_SIGNATURE']

        body = request.body.decode('utf-8')

        try:
            # 署名を検証して、問題なければhandleに定義されている関数を呼び出す
            handler.handle(body, signature)
        except InvalidSignatureError:

            return HttpResponseBadRequest()
        except Exception as e:

            print(e)
            return HttpResponseServerError()


        return HttpResponse('OK')



    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CallbackView, self).dispatch(*args, **kwargs)



    @staticmethod
    @handler.add(MessageEvent, message=TextMessage)
    def message_event(event):
        # オウム返しする
        reply = event.message.text

        # 雑談Bot
        # client = pya3rt.TalkClient(talk_api)
        # response = client.talk(event.message.text)
        # reply = response['results'][0]['reply']

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
