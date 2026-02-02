#!/usr/bin/env python3
"""
Teacher tool: build encoded feed files from *-sol.txt files.

Usage:
  python scripts/build_feeds.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


FEEDS_DIR = Path("static/feeds")


@dataclass(frozen=True)
class Level:
    source: str
    target: str
    method: str
    shift: int = 0
    key: str = ""


LEVELS: tuple[Level, ...] = (
    # Very easy intro, guided in class.
    Level(source="start-sol.txt", target="start.txt", method="caesar", shift=-1),
    # Slightly harder: same method, different shift (+7).
    Level(source="vlieg-sol.txt", target="vlieg.txt", method="caesar", shift=7),
    # New method, still approachable.
    Level(source="7maart-sol.txt", target="7maart.txt", method="atbash"),
    # Hardest level here: Vigenere with keyword from previous level (JEREMY).
    Level(source="JEREMY-sol.txt", target="JEREMY.txt", method="vigenere", key="JEREMY"),
)


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


def encode_text(text: str, level: Level) -> str:
    if level.method == "caesar":
        return caesar(text, level.shift)
    if level.method == "atbash":
        return atbash(text)
    if level.method == "vigenere":
        return vigenere(text, level.key)
    raise ValueError(f"Unknown method: {level.method}")


def main() -> None:
    FEEDS_DIR.mkdir(parents=True, exist_ok=True)
    for level in LEVELS:
        src = FEEDS_DIR / level.source
        dst = FEEDS_DIR / level.target
        if not src.exists():
            print(f"[SKIP] Missing source: {src}")
            continue

        plaintext = src.read_text(encoding="utf-8")
        ciphertext = encode_text(plaintext, level)
        dst.write_text(ciphertext, encoding="utf-8")
        print(f"[OK] {src.name} -> {dst.name} ({level.method})")


if __name__ == "__main__":
    main()
