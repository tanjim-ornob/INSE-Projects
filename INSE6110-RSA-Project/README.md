# RSA Encryption, Decryption, and Digital Signature Project

This project is an educational implementation of the RSA cryptosystem completed for an INSE 6110 university cryptography assignment.

The project demonstrates:

- RSA key parameter generation
- Prime number selection
- Public and private key calculation
- Modular exponentiation using square-and-multiply
- Message encryption
- Message decryption
- Digital signature generation
- Signature verification

## Disclaimer

This project is for academic learning purposes only.

It is not intended for real-world cryptographic use. The implementation uses small key sizes and simplified message handling to demonstrate the core RSA concepts.

The public GitHub version uses anonymized demo values. Student IDs, real names, partner names, and identifying values from the original academic submission have been removed.

## Project Requirements Covered

This project implements the following RSA steps:

1. Randomly select two prime numbers.
2. Compute `N = p * q`.
3. Compute `phi(N) = (p - 1) * (q - 1)`.
4. Select a public key `e` such that `gcd(e, phi(N)) = 1`.
5. Calculate the private key `d` such that `(e * d) mod phi(N) = 1`.
6. Encrypt and decrypt messages using square-and-multiply.
7. Sign and verify messages using RSA.

## Files

```text
.
├── README.md
├── data.txt
└── mdtanjimahmed_inse6110_rsa_project.py
