#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:?"


def uoc_rotative_encrypt(message, shift):
    """
    Simple substitution cipher
    :message: message to cipher (plaintext)
    :shift: offset or displacement
    :return: ciphered text
    """

    ciphertext = ""

    message = message.upper()

    for char in message:
        if char in ABC:
            char_index = ABC.index(char)
            encrypted_index = (char_index + shift) % len(ABC)
            encrypted_char = ABC[encrypted_index]
            ciphertext += encrypted_char
        else:
            ciphertext += char

    # --------------------------------

    return ciphertext


def uoc_rotative_decrypt(message, shift):
    """
    Simple substitution decipher
    :message: message to cipher (plaintext)
    :shift: offset or displacement
    :return: ciphered text
    """

    plaintext = ""

    message = message.upper()

    for char in message:
        if char in ABC:
            char_index = ABC.index(char)
            decrypted_index = (char_index - shift) % len(ABC)
            decrypted_char = ABC[decrypted_index]
            plaintext += decrypted_char
        else:
            plaintext += char

    # --------------------------------

    return plaintext


def uoc_grille_genkey(grille_len, num_holes):
    """
    Key generation
    :gruille_len: total grille length in symbols
    :num_holes: Number of holes in the grille
    :return: key as list of 0 and 1
    """

    key = []

    key = [0] * grille_len
    indexes = random.sample(range(grille_len), num_holes)
    for i in indexes:
        key[i] = 1
    # --------------------------------

    return key


def uoc_grille_encrypt(key, plaintext):
    """
    Encrypt a text using the key
    :message: message to grille_encrypt
    :shift: offset or displacement
    :return: ciphered text
    """

    ciphertext = ""

    j = 0
    finished = False

    while j < len(plaintext) or not finished:
        for i in range(len(key)):
            if not finished:
                if key[i] == 0:
                    ciphertext += random.choice(ABC)
                else:
                    if j == len(plaintext):
                        finished = True
                    else:
                        char = plaintext[j]
                        ciphertext += char
                        j += 1
    # --------------------------------
    return ciphertext


def uoc_grille_decrypt(key, ciphertext):
    """
    Decrypt a text using the key
    :message: message to grille_decrypt
    :subs_alphabet: substitution alphabet
    :return: ciphered text
    """

    plaintext = ""

    j = 0
    finished = False

    while j < len(ciphertext) or not finished:
        for i in range(len(key)):
            if not finished:
                if key[i] == 1:
                    if j >= len(ciphertext):
                        finished = True
                    else:
                        char = ciphertext[j]
                        plaintext += char
                j += 1

    # --------------------------------

    return plaintext


def uoc_encrypt(key, plaintext):
    """
    omplete cryptosystem (encrypt)
    :key: grille key
    :plaintext: message to encrypt
    :return: encrypted text
    """

    ciphertext = ""
    num_holes = 0

    for i in range(len(key)):
        if key[i] == 1:
            num_holes += 1

    rotativetext = uoc_rotative_encrypt(plaintext, num_holes)
    ciphertext = uoc_grille_encrypt(key, rotativetext)

    # --------------------------------

    return ciphertext


def uoc_decrypt(key, ciphertext):
    """
    Complete cryptosystem (decrypt)
    :key: grille key
    :ciphertext: message to decrypt
    :return: plaintext
    """

    plaintext = ""
    grilletext = uoc_grille_decrypt(key, ciphertext)
    num_holes = 0

    for i in range(len(key)):
        if key[i] == 1:
            num_holes += 1

    plaintext = uoc_rotative_decrypt(grilletext, num_holes)
    # --------------------------------

    return plaintext
