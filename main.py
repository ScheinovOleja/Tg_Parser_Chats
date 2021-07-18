import asyncio
import configparser
import csv
import re

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest


async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 200  # максимальное число записей, передаваемых за один раз
    while True:
        try:
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            all_messages = [message.to_dict() for message in history.messages]
            for message in all_messages:
                nums = re.findall(r'\d+', message['message'])
                nums = [int(i) for i in nums if 3000000 <= int(i) <= 35000000]
                if not nums:
                    continue
                user = await client.get_entity(message['from_id']['user_id'])
                with open(f'{channel.username}.csv', 'a+', encoding='utf-8') as file:
                    for vendor in nums:
                        data = [message['date'].strftime('%d-%m-%Y'), vendor, user.id,
                                f'@{user.username}' if user.username else user.first_name,
                                user.phone if user.phone else '--']
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(data)
        except Exception as exc:
            continue


async def main():
    # for chat in ['@wbofficialchat', '@wbofficialSKLAD']:
    #     channel = await client.get_entity(chat)
    await asyncio.gather(dump_all_messages(await client.get_entity('@wbofficialchat')),
                         dump_all_messages(await client.get_entity('@wbofficialSKLAD')))
    # await dump_all_messages(channel)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = int(config['Telegram']['api_id'])
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    with client:
        client.loop.run_until_complete(main())
