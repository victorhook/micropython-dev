import uasyncio as asyncio
import os

speed = 10

""" returns html headers as a dict, key-pairs """
def _parse_headers(lines):

    headers = {}
    for line in lines[1:]:
        line = line.strip().split(':', 1)
        header = line[0]
        if header:
            headers[header] = line[1]

    return headers

""" returns the binary data from the requested file """
def _get_data(_file):

    if _file == '/':
        # default file
        with open('index.html', 'rb') as f:
            return f.read()

    if _file[0] == '/':
        _file = _file[1:]

    if _file in os.listdir():
        with open(_file, 'rb') as f:
            return f.read()
            
    return None

""" handles an http request """
async def handle_request(reader, writer):
    
    req = await reader.read(-1)

    if req:

        if b'GET' == req[:3]:
            lines = req.decode('utf-8').split('\n')
            _file = lines[0].split()[1]
            headers = _parse_headers(lines[1:])

            print(_file)
            global speed
            speed += 1

        data = _get_data(_file)

        if data:
            msg = b'HTTP/1.1 200 OK\r\n' + \
            b'Server: ESP8266\r\n' + \
            b'content-type: text/html\r\n' + \
            b'content-length: ' + \
            '{}'.format(len(data)).encode() + \
            b'\r\n\r\n' + \
            data + \
            b'\r\n\r\n'

            await writer.awrite(msg)

        else:
            msg = b'HTTP/1.1 404 Not Found\r\n' + \
            b'Server: ESP8266\r\n' + \
            b'content-type: text/html\r\n' + \
            b'content-length: ' + \
            b'\r\n\r\n'

            await writer.awrite(msg)

    await writer.aclose()


async def start():
    print('Server stared')
    server = await asyncio.start_server(handle_request, '192.168.0.13', 9999)

loop = asyncio.get_event_loop()
loop.run_until_complete(start())

async def idle():
    global speed
    while 1:
        print(speed)
        await asyncio.sleep(2)