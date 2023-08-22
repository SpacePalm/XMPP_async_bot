import asyncio
import json
import ssl
from slixmpp import ClientXMPP

class MyBot(ClientXMPP):
    def __init__(self, jid, password, server_url, server_port, ssl_cert_file):
        super().__init__(jid, password)

        # Настройка параметров подключения
        self.server_url = server_url
        self.server_port = server_port
        self.ssl_cert_file = ssl_cert_file

        # Добавьте обработчики событий и другую логику здесь

        # Настройка SSL-соединения
        context = ssl.create_default_context()
        context.load_cert_chain(self.ssl_cert_file)
        self.ssl_context = context

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sender = msg['from']
            message = msg['body']
            print(f"Received message from {sender}: {message}")

if __name__ == '__main__':

    with open("data.json", "r") as json_file:
        login_data = json.load(json_file)
        jid = login_data["jid"]
        password = login_data["password"]
        port = login_data["port"]
        server_url = login_data["server_url"] 
        ssl_cert_file = login_data["ssl_cert_file"]

    bot = MyBot(jid, password, server_url, port, ssl_cert_file)
    asyncio.run(bot.connect(address=(server_url, port), use_ssl=True, ssl_context=bot.ssl_context))
    asyncio.run(bot.process(forever=True))

