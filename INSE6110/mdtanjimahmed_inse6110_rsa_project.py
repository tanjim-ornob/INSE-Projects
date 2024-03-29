# -*- coding: utf-8 -*-
"""MDTanjimAhmed_INSE6110_RSA_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13qumRxNevbGXRJSU8I9LcT5Z96Wmbc-I
"""

import random
import re

def is_prime(input):
  if input == 2 or input == 3:
    return True
  elif input < 2:
    return False
  elif input % 2 == 0:
    return False
  for i in range(2, int(input*0.5) + 1):
        if input % i == 0:
            return False
  return True


def generate_prime(bits):
    while True:
        value = random.randint(2 ** (bits - 1), 2 ** bits - 1)
        if value % 2 == 0:
            value += 1
        if is_prime(value):
            return value

def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


def generate_key(bits):
  p, q = generate_prime(bits), generate_prime(bits)
  N, phi_n = p * q, (p - 1) * (q - 1)

  while True:
    e = random.randrange(2 ** (bits -1), 2 ** bits - 1)
    d = gcd(e, phi_n)
    if d == 1:
        break

  return (p, q, N, phi_n, e, d)


def get_keys(bits):
    p, q, N, phi_n, e, d = generate_key(bits)
    print(f"p: {p}", f"q: {q}", f"N: {N}", f"phiN: {phi_n}", f"e: {e}", f"d: {d}")
    return (p, q, N, phi_n, e, d)

def find_d(phi_n, e, d, current_y, temp_phi_n):
  while e > 0:
      quotient = temp_phi_n // e
      remainder = temp_phi_n - (quotient * e)
      temp_phi_n = e
      e = remainder

      y = d - quotient * current_y
      d = current_y
      current_y = y

      if e == 1:
          break

  return current_y


def get_d(phi_n, e):
  d = 0
  current_y = 1
  temp_phi_n = phi_n
  output = find_d(phi_n, e, d, current_y, temp_phi_n)
  return output

def encrypt(N, e, message):
    pattern = '...?'
    matches = re.findall(pattern, message)
    hex_values = " ".join([i.encode('utf-8').hex() for i in matches]).split()
    integers = [int(j, 16) for j in hex_values]
    return integers, N, e


def square_and_multiply(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result


def get_encrpytion(N, e, message):
  integer, N, e = encrypt(N, e, message)
  cipher = [int(square_and_multiply(c, e, N)) for c in integer]
  return cipher


def get_decryption(N, d, cipher):
  integer = [int(square_and_multiply(int(part), d, N)) for part in cipher]
  hex_values = [hex(j)[2:] for j in integer]
  message = ''.join([bytes.fromhex(k).decode('ascii') for k in hex_values])
  return message


def get_signing(N, d, message):
  integer, N, d = encrypt(N, d, message)
  cipher = [int(square_and_multiply(c, d, N)) for c in integer]
  return cipher

def get_verification(N, e, cipher):
  integer = [int(square_and_multiply(int(part), e, N)) for part in cipher]
  hex_values = [hex(j)[2:] for j in integer]
  signature = ''.join(bytes.fromhex((k)).decode("ascii") for k in hex_values)
  return signature


def main():
  p, q, N, phi_n, e, d = get_keys(16)

  N = 1912407547; e = 40487; phi_n = 1912318696
  my_message = "Hello Nadia"; my_signature = "MD Tanjim Ahmed"
  partner_cipher_text = [1588254726, 1458329806, 1600891517, 171252503]
  partner_signature = [2054132782, 2419001626, 3663435429, 3143443959, 3011647020, 3055987228]
  partner_N = 3957207679; partner_e = 1447159027

  print(f"actual N: {N}", f"e: {e}", f"phi_n: {phi_n}")
  private_key = get_d(phi_n, e)
  print(f"private_key: {private_key}")
  encrypted_message = get_encrpytion(partner_N, partner_e, my_message)
  print(f"encrypted_message_sent_to_partner: {encrypted_message}")
  decrpyted_message = get_decryption(N, private_key, partner_cipher_text)
  print(f"decrpyted_message_received_from_partner: {decrpyted_message}")
  encrypted_signature = get_signing(N, private_key, my_signature)
  print(f"my_encrpyted_signature: {encrypted_signature}")
  decrypted_signature = get_verification(partner_N, partner_e, partner_signature)
  print(f"partner_decrypted_signature: {decrypted_signature}")


if __name__ == "__main__":
    main()

