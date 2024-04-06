import os
from PyPDF2 import PdfReader, PdfWriter

def remove_encryption_from_pdf(input_path, output_path):
    with open(input_path, "rb") as file:
        reader = PdfReader(file)
        if reader.is_encrypted:
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

if __name__ == "__main__":
    directory_path = os.getcwd()  # get current directory path
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(directory_path, "decrypted_" + filename)
            print(f"Processing {filename}")  # print the file name
            try:
                remove_encryption_from_pdf(input_path, output_path)
                print(f"Encryption removed from {filename}")
            except Exception as e:
                print(f"Failed to remove encryption from {filename}. Error: {e}")
from typing import *
from itertools import product
import time, pikepdf, math, numpy as np
from pikepdf import PasswordError

ALPHABET_UPPERCASE: Sequence[str] = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ALPHABET_LOWERCASE: Sequence[str] = tuple('abcdefghijklmnopqrstuvwxyz')
NUMBER: Sequence[str] = tuple('0123456789')

def as_list(l):
    if isinstance(l, (list, tuple, set, np.ndarray)):
        l = list(l)
    else:
        l = [l]
    return l

def human_readable_numbers(n, decimals: int = 0):
    n = round(n)
    if n < 1000:
        return str(n)
    names = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion']
    n = float(n)
    idx = max(0,min(len(names)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return f'{n/10**(3*idx):.{decimals}f} {names[idx]}'

def check_password(pdf_file_path: str, password: str) -> bool:
    ## You can modify this function to use something other than pike pdf. 
    ## This function should throw return True on success, and False on password-failure.
    try:
        pikepdf.open(pdf_file_path, password=password)
        return True
    except PasswordError:
        return False


def check_passwords(pdf_file_path, combination, log_freq: int = int(1e4)):
    combination = [tuple(as_list(c)) for c in combination]
    print(f'Trying all combinations:')
    for i, c in enumerate(combination):
        print(f"{i}) {c}")
    num_passwords: int = np.product([len(x) for x in combination])
    passwords = product(*combination)
    success: bool | str = False
    count: int = 0
    start: float = time.perf_counter()
    for password in passwords:
        password = ''.join(password)
        if check_password(pdf_file_path, password=password):
            success = password
            print(f'SUCCESS with password "{password}"')
            break
        count += 1
        if count % int(log_freq) == 0:
            now = time.perf_counter()
            print(f'Tried {human_readable_numbers(count)} ({100*count/num_passwords:.1f}%) of {human_readable_numbers(num_passwords)} passwords in {(now-start):.3f} seconds ({human_readable_numbers(count/(now-start))} passwords/sec). Latest password tried: "{password}"')
    end: float = time.perf_counter()
    msg: str = f'Tried {count} passwords in {1000*(end-start):.3f}ms ({count/(end-start):.3f} passwords/sec). '
    msg += f"Correct password: {success}" if success is not False else f"All {num_passwords} passwords failed."
    print(msg)
    
check_passwords(
    pdf_file_path='sd.pdf',
    combination=[
        ALPHABET_UPPERCASE,
        ALPHABET_UPPERCASE,
        ALPHABET_UPPERCASE,
        ALPHABET_UPPERCASE,
        NUMBER,
        NUMBER,
        NUMBER,
        NUMBER,
    ]
)
