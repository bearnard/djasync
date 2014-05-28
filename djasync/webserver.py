import asyncio
import io
import importlib
import logging

from .http_parser import create_parser

logger = logging.getLogger(__name__)

WSGI_APP = None


class HTTPServer(asyncio.Protocol):

    def connection_made(self, transport):
        logger.debug('connection made')
        self.transport = transport
        self.request_buffer = io.BytesIO()
        self.parser = create_parser()
        self.header_chunk = 0

    def data_received(self, data):
        logger.debug('data received {}'.format(data))
        self.request_buffer.write(data)
        header_idx = self.parser.send(data)
        while header_idx is not None:
            if self.header_chunk == 0:
                self.handle_request(method='GET', uri='/')
            try:
                header_idx = next(self.parser)
            except StopIteration:
                break
            self.header_chunk += 1

    def start_response(self, status, response_headers, exc_info=None):
        logger.debug('start response')
        self.transport.write(b' '.join((b'HTTP/1.1', status.encode(), b'\r\n')))
        self.transport.write(b'\r\n')

    def handle_request(self, method, uri, headers=None):
        logger.debug('handle request')
        resp = WSGI_APP(
            {
                'REQUEST_METHOD': method,
                'PATH_INFO': uri,
                'wsgi.input': None,
                'SERVER_NAME': 'localhost',
                'SERVER_PORT': '8000'
            },
            self.start_response)
        # TODO: handle async response here
        for chunk in resp:
            self.transport.write(chunk)
        self.transport.close()


def run(host, port, wsgi_app):
    global WSGI_APP
    split = wsgi_app.rfind('.')
    if split < 0:
        raise ValueError('bad wsgi app')
    module = importlib.import_module(wsgi_app[:split])
    if split < len(wsgi_app):
        WSGI_APP = getattr(module, wsgi_app[split + 1:])
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(HTTPServer, host, port)
    server = loop.run_until_complete(coroutine)
    loop.run_forever()


def main():
    import argparse
    parser = argparse.ArgumentParser('asyncio web server')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default='8000')
    parser.add_argument('wsgi_app')
    args = parser.parse_args()
    run(args.host, args.port, args.wsgi_app)


if __name__ == '__main__':
    main()
