#!/usr/bin/env python3
"""
Student script: fetch encrypted feed lines and decode them.

They can tweak only a few lines (LEVEL and DECODE config) each round.
"""

from __future__ import annotations

import argparse
import time
import urllib.request


# --- Tweak these in class ---
BASE_URL = "http://localhost:5173/feeds"
LEVEL = "start"  # start -> vlieg -> 7maart -> JEREMY
MODE = "caesar"  # caesar | atbash | vigenere
SHIFT = -1  # used by caesar
KEY = "JEREMY"  # used by vigenere
BRUTE_FORCE = False  # set True for caesar levels when shift is unknown
# ----------------------------


def shift_char(ch: str, shift: int) -> str:
    if "a" <= ch <= "z":
        base = ord("a")
        return chr(base + ((ord(ch) - base + shift) % 26))
    if "A" <= ch <= "Z":
        base = ord("A")
        return chr(base + ((ord(ch) - base + shift) % 26))
    return ch


def caesar(text: str, shift: int) -> str:
    return "".join(shift_char(ch, shift) for ch in text)


def atbash(text: str) -> str:
    out: list[str] = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr(ord("z") - (ord(ch) - ord("a"))))
        elif "A" <= ch <= "Z":
            out.append(chr(ord("Z") - (ord(ch) - ord("A"))))
        else:
            out.append(ch)
    return "".join(out)


def vigenere(text: str, key: str, decode: bool = False) -> str:
    key_shifts = [ord(ch.upper()) - ord("A") for ch in key if ch.isalpha()]
    if not key_shifts:
        raise ValueError("Vigenere key must contain letters.")

    out: list[str] = []
    idx = 0
    for ch in text:
        if ch.isalpha():
            shift = key_shifts[idx % len(key_shifts)]
            if decode:
                shift *= -1
            out.append(shift_char(ch, shift))
            idx += 1
        else:
            out.append(ch)
    return "".join(out)


def decode_line(line: str) -> str:
    if MODE == "caesar":
        return caesar(line, -SHIFT)
    if MODE == "atbash":
        return atbash(line)
    if MODE == "vigenere":
        return vigenere(line, KEY, decode=True)
    raise ValueError(f"Unknown MODE: {MODE}")


def brute_force_caesar(line: str) -> list[str]:
    return [f"shift={s:2d}: {caesar(line, -s)}" for s in range(26)]


def fetch_lines(level: str) -> list[str]:
    url = f"{BASE_URL}/{level}.txt"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
    return data.splitlines()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=1.1, help="seconds between lines")
    args = parser.parse_args()

    lines = fetch_lines(LEVEL)
    print(f"Receiving encrypted stream: {LEVEL}.txt")
    print("-" * 48)

    for line in lines:
        print(f"[cipher] {line}")
        if BRUTE_FORCE and MODE == "caesar":
            for candidate in brute_force_caesar(line):
                print(f"  {candidate}")
        else:
            print(f"[plain ] {decode_line(line)}")
        print()
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
