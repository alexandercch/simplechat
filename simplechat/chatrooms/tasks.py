from urllib import request

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .constants import (
    STOCK_COMMAND, STOCK_URL, STOCK_NAME_COL, STOCK_VALUE_COL
)


@shared_task
def retrieve_stock_value(chat_room, message):
    stock_code = message.replace(STOCK_COMMAND, '')
    stock_service = STOCK_URL.format(stock_code=stock_code)
    
    csv_response = request.urlopen(stock_service)
    csv_lines = [l.decode('utf-8') for l in csv_response.readlines()]
    stock_values = csv_lines[1].split(',')
    stock_message = "{} quote is ${} per share".format(
        stock_values[STOCK_NAME_COL], stock_values[STOCK_VALUE_COL]
    )

    channel_layer =  get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        chat_room, {'type': 'bot_message', 'message': stock_message}
    )
