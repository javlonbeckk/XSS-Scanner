#!/usr/bin/python3

#global imports
import requests
import random

def fuzz(url, payload):
    response = requests.post(url, data=payload)
    return response


def basic_fuzzing(url):
    print("\nFUZZING")
    for i in range(100, 501, 100):
        payload = ''.join(chr(random.randint(32,126)) for j in range(i))
        response = fuzz(url, payload)

        if response.status_code == 200:
            print(f'{i//100}/5 The website responded successfully.')
        else:
            print(f'{i//100}/5 The website responded with an error.')


def custom_fuzzing(url, wordlist):
    print("\nFUZZING")
    file = open(wordlist, "r")
    lines = open(wordlist, "r").readlines()
    l = len(lines)
    i = 1
    for payload in file.readlines():
        response = fuzz(url, payload[:-1])

        if response.status_code == 200:
            print(f'{i}/{l} The website responded successfully.')
        else:
            print(f'{i}/{l} The website responded with an error.')
        i += 1

