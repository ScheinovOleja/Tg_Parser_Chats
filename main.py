import asyncio
import configparser
import csv
import re
from telethon.sync import TelegramClient


async def dump_all_messages(channel):
    async for message in client.iter_messages(channel):
        try:
            nums = re.findall(r'\d+', message.message)
            nums = [int(i) for i in nums if 3000000 <= int(i) <= 35000000]
            if not nums:
                continue
            user = await client.get_entity(message.from_id.user_id)
            with open(f'{channel.username}.csv', 'a+', encoding='utf-8') as file:
                for vendor in nums:
                    data = [message.date.strftime('%d-%m-%Y'), vendor, user.id,
                            f'@{user.username}' if user.username else "--",
                            f'{user.first_name}' if user.first_name else '--',
                            user.phone if user.phone else '--']
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(data)
        except Exception as exc:
            print(exc)


async def main():
    for chat in ['@wbofficialchat']:
        channel = await client.get_entity(chat)
        await dump_all_messages(channel)


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
        user = client.get_entity('@grekov')
        client.send_file(user, open('wbofficialchat.csv', 'rb'),
                         caption='Это сообщение создано автоматически!\nПолучен файл!')
