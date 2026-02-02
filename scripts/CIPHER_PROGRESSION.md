Suggested progression (HAVO/VWO 4):

1) `start.txt` (Caesar -1)
- Keep `MODE = "caesar"`, `SHIFT = -1`.
- Goal: understand basic letter shifting.

2) `vlieg.txt` (Caesar +7)
- Same code, only change `SHIFT = 7`.
- Goal: show same method with another setting.

3) `7maart.txt` (Atbash)
- Change `MODE = "atbash"`.
- Goal: introduce a second classical cipher.

4) `JEREMY.txt` (Vigenere with key `JEREMY`)
- Change `MODE = "vigenere"` and `KEY = "JEREMY"`.
- Goal: understand keyword-based shifts.

Optional challenge (between 2 and 3):
- Set `BRUTE_FORCE = True` in a Caesar level.
- Let students inspect all 26 options and pick readable Dutch text.

Teacher workflow:
1. Edit `static/feeds/*-sol.txt`.
2. Run `python scripts/build_feeds.py`.
3. The encrypted files `static/feeds/*.txt` are regenerated.
