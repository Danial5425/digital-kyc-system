import re
from dataclasses import dataclass
from typing import Tuple, Optional, List


# ---------- Aadhaar (Verhoeff-based) ----------

# Verhoeff tables
_VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

_VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

_VERHOEFF_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def _verhoeff_check_digit(num_str: str) -> str:
    c = 0
    for i, item in enumerate(reversed(num_str)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[(i + 1) % 8][int(item)]]
    return str(_VERHOEFF_INV[c])


def validate_aadhaar(aadhaar: str) -> Tuple[bool, str]:
    aadhaar = aadhaar.strip()
    if len(aadhaar) != 12 or not aadhaar.isdigit():
        return False, "Aadhaar must be exactly 12 digits."

    if not (2 <= int(aadhaar[0]) <= 9):
        return False, "Aadhaar must start with a digit between 2 and 9."

    base = aadhaar[:-1]
    check_digit = aadhaar[-1]
    expected = _verhoeff_check_digit(base)

    if check_digit != expected:
        return False, "Aadhaar checksum validation failed."

    return True, "Aadhaar is valid."


# ---------- PAN (custom checksum) ----------

_PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")


def _char_to_num(c: str) -> int:
    if c.isdigit():
        return int(c)
    return 10 + (ord(c.upper()) - ord("A"))


def _num_to_char(n: int) -> str:
    return chr(ord("A") + (n % 26))


def validate_pan(pan: str) -> Tuple[bool, str]:
    pan = pan.strip().upper()
    if not _PAN_REGEX.match(pan):
        return False, "PAN format must be 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)."

    body = pan[:9]
    check_char = pan[9]

    total = sum(_char_to_num(c) for c in body)
    expected = _num_to_char(total % 26)

    if check_char != expected:
        return False, "PAN checksum validation failed."

    return True, "PAN is valid."


# ---------- Passport (MRZ-style check digit) ----------

def _doc_char_value(c: str) -> int:
    if c.isdigit():
        return int(c)
    return 10 + (ord(c.upper()) - ord("A"))


def _passport_check_digit(body7: str) -> str:
    weights = [7, 3, 1, 7, 3, 1, 7]
    total = 0
    for i, ch in enumerate(body7):
        total += _doc_char_value(ch) * weights[i % len(weights)]
    return str(total % 10)


def validate_passport(passport: str) -> Tuple[bool, str]:
    passport = passport.strip().upper()

    if len(passport) != 8:
        return False, "Passport must be 8 characters (1 letter + 6 digits + 1 check digit)."

    body = passport[:7]
    check = passport[7]

    if not (body[0].isalpha() and body[1:].isdigit() and check.isdigit()):
        return False, "Passport format must be: 1 letter, 6 digits, 1 digit check."

    expected = _passport_check_digit(body)
    if check != expected:
        return False, "Passport checksum validation failed."

    return True, "Passport is valid."


# ---------- High-level KYC aggregation ----------

@dataclass
class DocumentValidationResult:
    document_type: str
    value: str
    is_valid: bool
    reason: Optional[str] = None


def validate_all_documents(
    aadhaar: Optional[str] = None,
    pan: Optional[str] = None,
    passport: Optional[str] = None,
) -> Tuple[bool, List[DocumentValidationResult]]:
    """
    Run all document validations and return overall status + per-document details.
    """
    results: List[DocumentValidationResult] = []

    if aadhaar:
        ok, msg = validate_aadhaar(aadhaar)
        results.append(DocumentValidationResult("aadhaar", aadhaar, ok, msg))

    if pan:
        ok, msg = validate_pan(pan)
        results.append(DocumentValidationResult("pan", pan, ok, msg))

    if passport:
        ok, msg = validate_passport(passport)
        results.append(DocumentValidationResult("passport", passport, ok, msg))

    if not results:
        # No documents provided
        return False, [
            DocumentValidationResult(
                "none",
                "",
                False,
                "No documents provided for validation.",
            )
        ]

    overall_ok = all(r.is_valid for r in results)
    return overall_ok, results

# ---------- Helper functions to generate valid sample IDs ----------

import random


def generate_valid_aadhaar() -> str:
    """
    Generate a 12-digit Aadhaar-like number that passes Verhoeff checksum.
    First digit is between 2 and 9, next 10 digits random, last digit is check.
    """
    first = str(random.randint(2, 9))
    middle = "".join(str(random.randint(0, 9)) for _ in range(10))
    base = first + middle  # 11 digits
    check = _verhoeff_check_digit(base)
    return base + check


def generate_valid_pan(prefix5: str | None = None, digits4: str | None = None) -> str:
    """
    Generate a PAN-like number with a valid custom checksum.
    prefix5: 5 letters (optional, random if not provided)
    digits4: 4 digits (optional, random if not provided)
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if prefix5 is None:
        prefix5 = "".join(random.choice(letters) for _ in range(5))
    if digits4 is None:
        digits4 = "".join(str(random.randint(0, 9)) for _ in range(4))

    base = prefix5.upper() + digits4
    total = sum(_char_to_num(c) for c in base)
    check_char = _num_to_char(total % 26)
    return base + check_char


def generate_valid_passport(
    first_letter: str | None = None,
    digits6: str | None = None,
) -> str:
    """
    Generate an 8-character passport-like number:
    1 letter + 6 digits + 1 check digit using MRZ-style checksum.
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if first_letter is None:
        first_letter = random.choice(letters)
    if digits6 is None:
        digits6 = "".join(str(random.randint(0, 9)) for _ in range(6))

    body = first_letter.upper() + digits6
    check = _passport_check_digit(body)
    return body + check
