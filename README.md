# Cryptography Algorithms in Python

This repository contains several cryptographic systems implemented in **Python**, covering different paradigms of cryptography: historical, symmetric, and public key.

## Contents
- **Historical Ciphers**  
  - Combination of Cardano Grille and Caesar cipher.  
- **Symmetric Cryptography**  
  - Stream cipher inspired by A5/1 (LFSRs).  
  - Hash function built on AES.  
- **Public Key Cryptography**  
  - Elliptic Curve Cryptography (ECC).  
  - Diffie-Hellman key exchange over elliptic curves.  

Each module includes:
- `solution.py` — Python implementation.  
- `test.py` — Unit tests.  
- Documentation in `docs/` folder.  

## Project Structure
```
cryptography-algorithms/
├─ historical-ciphers/
│  ├─ solution.py
│  ├─ test.py
│
├─ symmetric-crypto/
│  ├─ solution.py
│  ├─ test.py
│
├─ public-key-crypto/
│  ├─ solution.py
│  ├─ test.py
│
├─ docs/                     # Assignment PDFs
│  ├─ historical-ciphers.pdf
│  ├─ symmetric-crypto.pdf
│  └─ public-key-crypto.pdf
├─ README.md
└─ .gitignore
```

## How to Run
Requires **Python 3.9+**.  
Run unit tests for each module:

```bash
cd historical-ciphers
python -m unittest test.py

cd ../symmetric-crypto
python -m unittest test.py

cd ../public-key-crypto
python -m unittest test.py
```