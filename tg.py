from hydrogram import *
import asyncio


proxy = {
     "scheme": "socks5",
     "hostname": "127.0.0.1",
     "port": 8086,
}
app = Client(
    'session',
    19862900,
    'b987591392258ccdd42eab073eccc7fe',
    proxy=proxy
)


