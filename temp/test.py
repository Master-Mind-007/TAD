from telethon.sync import TelegramClient
from telethon.crypto import AuthKey
import asyncio
authorization_key = "8a1f06fc8bed951d70187b838f908dd41de41e9f7221925a794ffde4ad5f7f14a02e1ca41f0ac5245f22663693afe53b4a79a0c086ba68326894bb6d1495caa1e99d3ed1815d9d1560990eadbcff70b3138a3fcc81e3abe23e3cfefd7fc93cdadb517a6667f73737551bbd61a7c49c41d7f5ba05cef8248c975afd565ea706be8a847ee3c7f3d792f49efe05ed2dd280fa8b71e9ee4c584f024ab89b4cfea139075019fe4a3d8c2766a9221929873105efd9dbea974a9e9367e1b5de21d257b0b49439d77e9f06fd8ce4a468f924aec800ebae19400d7bfb9e7a9499a646bd99962876798c9be0e9c7fec647a03582874dc8b07e796d11adb45b8ca5bd1f3581"


async def start():
    # Initialize your client
    client = TelegramClient('session_name', 12220268, "8555236aba57fb960d73b6ca980226ae")

    print(client.session.auth_key.key.hex())
    #client.session.set_dc(2,'149.154.167.51',443)
    client.session.auth_key= AuthKey(data=bytearray.fromhex(authorization_key))
    print(client.session.auth_key.key.hex())
    print(await client.start())
    
    # Connect to the client
    #await client.connect()
    print(await client.get_me())

asyncio.run(start())