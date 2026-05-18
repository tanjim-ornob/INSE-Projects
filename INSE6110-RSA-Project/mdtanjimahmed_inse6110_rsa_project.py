# -*- coding: utf-8 -*-
import random
import re

"""
Educational RSA implementation for one of my Master's degree courses: Foundation of Cryptography (INSE 6110)

This project manually implements simple RSA key generation,
encryption/decryption and signature/verification using modular
exponentiation by square-and-multiply.

This is for academic learning only and is not suitable for production cryptography.
"""

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
        e = random.randrange(2, phi_n)
        if gcd(e, phi_n) == 1:
            break

    d = get_d(phi_n, e)

    if d < 0:
        d += phi_n

    return p, q, N, phi_n, e, d


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

    if output < 0:
        output += phi_n

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


def get_encryption(N, e, message):
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
    # My RSA values from the anonymized public data file
    N = 1912407547
    e = 40487
    phi_n = 1912318696
    private_key = get_d(phi_n, e)

    # Anonymized demo message and signature
    my_message = "Hello You"
    my_signature = "Student Demo"

    # Anonymized demo partner values
    partner_N = 3586779127
    partner_e = 65537

    # Anonymized demo ciphertext/signature values
    partner_cipher_text = [1588254726, 1458329806, 97701714]
    partner_signature = [114934866, 1592326434, 1690739743, 199310275]

    print("My RSA Parameters")
    print(f"N: {N}")
    print(f"e: {e}")
    print(f"phi_n: {phi_n}")
    print(f"d/private_key: {private_key}")

    encrypted_message = get_encryption(partner_N, partner_e, my_message)
    print(f"encrypted_message_sent_to_partner: {encrypted_message}")

    decrypted_message = get_decryption(N, private_key, partner_cipher_text)
    print(f"decrypted_message_received_from_partner: {decrypted_message}")

    encrypted_signature = get_signing(N, private_key, my_signature)
    print(f"my_encrypted_signature: {encrypted_signature}")

    verified_signature = get_verification(partner_N, partner_e, partner_signature)
    print(f"partner_verified_signature: {verified_signature}")

if __name__ == "__main__":
    main()

