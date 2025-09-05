#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

MODE_CIPHER = 0
MODE_DECIPHER = 1

pol19 = [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pol22 = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pol23 = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]

def_clocking_bits = [8, 10, 10]


# --------------------------------------------------------------------------


def uoc_lfsr_sequence(polynomial, initial_state, output_bits):
    """
    Returns the output sequence of output_bits bits of an LFSR with a given initial state and connection polynomial.

    :param polynomial: list of integers, with the coefficients of the connection polynomial that define the LFSR.
    :param initial_state: list of integers with the initial state of the LFSR
    :param output_bits: integer, number of bits of the output sequence
    :return: a list of output_bits bits
    """
    result = []

    state = initial_state[::-1]
    polynomial_reverse = polynomial[::-1]
    polynomial_list = []

    for i in range(len(polynomial_reverse)):
        if polynomial_reverse[i] == 1:
            polynomial_list.append(i)

    for i in range(output_bits):
        result.append(state[-1])
        plist = polynomial_list.copy()
        next_bit = state[polynomial_list[0]]

        for j in range(len(polynomial_list) - 1):
            next_bit = next_bit ^ state[plist[1]]
            plist = plist[1:]

        state.pop()
        state.insert(0, next_bit)
    # --------------------------------

    return result


def uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, clocking_bits, output_bits):
    """
    Implements extended A5's pseudorandom generator.
    :param params_pol_0: two-element list describing the first LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param params_pol_1: two-element list describing the second LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param params_pol_2: two-element list describing the third LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param clocking_bits: three-element list, with the clocking bits of each LFSR
    :param output_bits: integer, number of bits of the output sequence
    :return: list of output_bits elements with the pseudo random sequence
    """

    sequence = []

    lfsr1 = uoc_lfsr_sequence(params_pol_0[0], params_pol_0[1], len(params_pol_0[0]))
    lfsr2 = uoc_lfsr_sequence(params_pol_1[0], params_pol_1[1], len(params_pol_1[0]))
    lfsr3 = uoc_lfsr_sequence(params_pol_2[0], params_pol_2[1], len(params_pol_2[0]))

    lfsr1 = lfsr1[::-1]
    lfsr2 = lfsr2[::-1]
    lfsr3 = lfsr3[::-1]
    polreversed0 = params_pol_0[0][::-1]
    polreversed1 = params_pol_1[0][::-1]
    polreversed2 = params_pol_2[0][::-1]

    if clocking_bits[0] > (len(params_pol_0[1]) - 1) or clocking_bits[1] > (len(params_pol_1[1]) - 1) \
            or clocking_bits[2] > (len(params_pol_2[1]) - 1):
        raise ValueError("bad clocking bits!")

    pol0 = []
    pol1 = []
    pol2 = []

    for i in range(len(params_pol_0[0])):
        if polreversed0[i] == 1:
            pol0.append(i)

    for i in range(len(params_pol_1[0])):
        if polreversed1[i] == 1:
            pol1.append(i)

    for i in range(len(params_pol_2[0])):
        if polreversed2[i] == 1:
            pol2.append(i)

    for i in range(output_bits):
        new_bit1 = lfsr1[pol0[0]]
        new_bit2 = lfsr2[pol1[0]]
        new_bit3 = lfsr3[pol2[0]]

        pol0_copy = pol0.copy()
        pol1_copy = pol1.copy()
        pol2_copy = pol2.copy()

        next_bit = lfsr1[-1] ^ lfsr2[-1] ^ lfsr3[-1]
        sequence.append(next_bit)

        if lfsr1[clocking_bits[0]] == lfsr2[clocking_bits[1]] == lfsr3[clocking_bits[2]]:
            for j in range(len(pol0) - 1):
                new_bit1 = new_bit1 ^ lfsr1[pol0_copy[1]]
                pol0_copy = pol0_copy[1:]

            lfsr1.pop()
            lfsr1.insert(0, new_bit1)

            for j in range(len(pol1) - 1):
                new_bit2 = new_bit2 ^ lfsr2[pol1_copy[1]]
                pol1_copy = pol1_copy[1:]

            lfsr2.pop()
            lfsr2.insert(0, new_bit2)

            for j in range(len(pol2) - 1):
                new_bit3 = new_bit3 ^ lfsr3[pol2_copy[1]]
                pol2_copy = pol2_copy[1:]

            lfsr3.pop()
            lfsr3.insert(0, new_bit3)

        elif lfsr1[clocking_bits[0]] == lfsr2[clocking_bits[1]]:
            for j in range(len(pol0) - 1):
                new_bit1 = new_bit1 ^ lfsr1[pol0_copy[1]]
                pol0_copy = pol0_copy[1:]

            lfsr1.pop()
            lfsr1.insert(0, new_bit1)

            for j in range(len(pol1) - 1):
                new_bit2 = new_bit2 ^ lfsr2[pol1_copy[1]]
                pol1_copy = pol1_copy[1:]

            lfsr2.pop()
            lfsr2.insert(0, new_bit2)

        elif lfsr1[clocking_bits[0]] == lfsr3[clocking_bits[2]]:
            for j in range(len(pol0) - 1):
                new_bit1 = new_bit1 ^ lfsr1[pol0_copy[1]]
                pol0_copy = pol0_copy[1:]

            lfsr1.pop()
            lfsr1.insert(0, new_bit1)

            for j in range(len(pol2) - 1):
                new_bit3 = new_bit3 ^ lfsr3[pol2_copy[1]]
                pol2_copy = pol2_copy[1:]

            lfsr3.pop()
            lfsr3.insert(0, new_bit3)

        elif lfsr2[clocking_bits[1]] == lfsr3[clocking_bits[2]]:
            for j in range(len(pol1) - 1):
                new_bit2 = new_bit2 ^ lfsr2[pol1_copy[1]]
                pol1_copy = pol1_copy[1:]

            lfsr2.pop()
            lfsr2.insert(0, new_bit2)

            for j in range(len(pol2) - 1):
                new_bit3 = new_bit3 ^ lfsr3[pol2_copy[1]]
                pol2_copy = pol2_copy[1:]

            lfsr3.pop()
            lfsr3.insert(0, new_bit3)

    # --------------------------------

    return sequence


def uoc_a5_cipher(initial_state_0, initial_state_1, initial_state_2, message, mode):
    """
    Implements ciphering/deciphering with the A5 pseudo random generator.

    :param initial_state_0: list, initial state of the first LFSR
    :param initial_state_1: list, initial state of the second LFSR
    :param initial_state_2: list, initial state of the third LFSR
    :param message: string, plaintext to cipher (mode=MODE_CIPHER) or ciphertext to decipher (mode=MODE_DECIPHER)
    :param mode: MODE_CIPHER or MODE_DECIPHER, whether to cipher or decipher
    :return: string, ciphertext (mode=MODE_CIPHER) or plaintext (mode=MODE_DECIPHER)
    """

    output = ""

    params_pol_0 = [pol19, initial_state_0]
    params_pol_1 = [pol22, initial_state_1]
    params_pol_2 = [pol23, initial_state_2]

    if mode == MODE_CIPHER:
        binary_text = "".join([format(ord(char), '08b') for char in message])

        sequence = uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, def_clocking_bits,
                                                len(binary_text))

        binary_text = [int(char, 2) for char in binary_text]

        encrypted_bits = [m ^ p for m, p in zip(binary_text, sequence)]
        output = ''.join([str(bit) for bit in encrypted_bits])

    elif mode == MODE_DECIPHER:
        sequence = uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, def_clocking_bits,
                                                len(message))

        message = [int(char, 2) for char in message]

        decrypted_bits = [m ^ p for m, p in zip(message, sequence)]

        output = "".join(
            [chr(int("".join(map(str, decrypted_bits[i:i + 8])), 2)) for i in range(0, len(decrypted_bits), 8)])
    # --------------------------------
    return output


def uoc_aes(message, key):
    """
    Implements 1 block AES enciphering using a 256-bit key.

    :param message: string of 1 and 0s with the binary representation of the messsage, 128 char. long
    :param key: string of 1 and 0s with the binary representation of the key, 256 char. long
    :return: string of 1 and 0s with the binary representation of the ciphered message, 128 char. long
    """

    cipher_text = ""

    key_bytes = bytes(int(key[i:i + 8], 2) for i in range(0, len(key), 8))
    message_bytes = bytes(int(message[i:i + 8], 2) for i in range(0, len(message), 8))

    aes = AES.new(key_bytes, AES.MODE_ECB)

    encrypted_message = aes.encrypt(message_bytes)

    cipher_text = "".join([format(byte, '08b') for byte in encrypted_message])
    # --------------------------------

    return cipher_text


def uoc_g(message):
    """
    Implements the g function.

    :param message: string of 1 and 0s with the binary representation of the messsage, 128 char. long
    :return: string of 1 and 0s, 256 char. long
    """

    output = ""

    output = message + message
    # --------------------------------

    return output


def uoc_naive_padding(message, block_len):
    """
    Implements a naive padding scheme. As many 0 are appended at the end of the message
    until the desired block length is reached.

    :param message: string with the message
    :param block_len: integer, block length
    :return: string of 1 and 0s with the padded message
    """

    output = ""

    bin_str = "".join(format(ord(c), '08b') for c in message)

    remainder = len(bin_str) % block_len

    if remainder != 0:
        num_zeros = block_len - remainder
        bin_str += "0" * num_zeros

    output = bin_str
    # --------------------------------

    return output


def uoc_mmo_hash(message):
    """
    Implements the hash function.

    :param message: a char. string with the message
    :return: string of 1 and 0s with the hash of the message
    """

    h_i = ""

    h0 = "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    block_len = 128

    padded_msg = uoc_naive_padding(message, block_len)

    for i in range(0, len(padded_msg), block_len):
        key = uoc_g(h0)

        block = padded_msg[i:i + block_len]

        ciphered_block = uoc_aes(block, key)

        g_output = uoc_g(ciphered_block)
        h0 = "".join(str(int(a) ^ int(b)) for a, b in zip(h0, g_output))

    h_i = h0[-128:].zfill(128)
    # --------------------------------
    return h_i


def uoc_collision(prefix):
    """
    Generates collisions for uoc_mmo_hash, with messages having a given prefix.

    :param prefix: string, prefix for the messages
    :return: 2-element tuple, with the two strings that start with prefix and have the same hash.
    """

    collision = ("", "")

    return collision
