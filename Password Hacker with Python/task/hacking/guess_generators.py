import string
import itertools

def lower_case_elements():
    alphabet = list(string.ascii_lowercase)
    numbers = list(string.digits)
    alphabet.extend(numbers)
    return alphabet

def all_elements():
    alphabet = list(string.ascii_letters + string.digits)
    return alphabet

def brute_force_generator(base_str: str = ""):
    extend = lower_case_elements()
    base = [base_str]
    while True:
        new_base = []
        for first, second in itertools.product(base, extend):
            combination = first + second
            new_base.append(combination)
            yield combination
        base = new_base

def constant_length_generator(base: str = ""):
    extend = all_elements()
    for element in extend:
        yield base + element


def generate_from_dict(file_name: str):
    with open(file_name, 'r') as file:
        common_pw = file.readlines()
    for pw in common_pw:
        upper_lower_combinations = map(lambda x: "".join(x),
                                       itertools.product(
                                           *([letter.lower(), letter.upper()]
                                             for letter in pw.strip())))
        for combination in upper_lower_combinations:
            yield combination
