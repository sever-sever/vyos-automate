#!/usr/bin/env python3

import os
import logging
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer


def file_server(server_directory, url_path='/', bind_address='0.0.0.0', bind_port=8000):
    """
    Start a simple file server.

    Args:
        server_directory (str): The directory containing files to be served.
        url_path (str): The part of the URL after the domain and before any query parameters.
        bind_address (str): The IP address to bind the server to. Defaults to '0.0.0.0'.
        bind_port (int): The port to bind the server to. Defaults to 8000.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.name = os.path.basename(__file__)

    logger.info(f'Serving files from: {server_directory}')
    logger.info(f'Binding to: {bind_address}:{bind_port}')
    logger.info(f'URL Path: {url_path}')

    handler_class = partial(SimpleHTTPRequestHandler, directory=server_directory)

    with HTTPServer((bind_address, bind_port), handler_class) as http_server:
        logger.info(
            f'Starting file server on http://{bind_address}:{bind_port}{url_path}'
        )
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            logger.info('File server terminated')


if __name__ == "__main__":
    url_path_to_serve = '/'
    files_directory = '/home/vyos/'
    file_server(files_directory, url_path_to_serve)
