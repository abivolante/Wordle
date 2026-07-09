# Wordle (Command Line Edition)

A Python recreation of Wordle that runs in the terminal, built as a hands-on project to strengthen my Python fundamentals, particularly working with dictionaries, string/list manipulation, and handling edge cases like duplicate letters.

## How it works  

The goal is to guess the secret five-letter word in six tries, after each guess, you'll see which letters are correct, present, or absent, plus a running keyboard showing every letter you've tried.

- `/` — letter is correct and in the right position
- `*` — letter is in the word but in the wrong position
- `x` — letter is not in the word at all

The game correctly handles duplicate letters (e.g. guessing a word with two `E`s when the answer only has one), which is the trickiest part of implementing Wordle's logic.

## Requirements

- Python 3.9+
- `sgb-words.txt` — a plain text file with one five-letter word per line, used as both the word list and the dictionary for validating guesses. Included in this repo.

## Running it

```bash
git clone https://github.com/abivolante/wordle.git
cd wordle/file
python3 main.py
```

Make sure `sgb-words.txt` is in the same directory as `main.py`.

## Example

```
Welcome to Wordle!
Please input your name: Abi
Would you like to start, Abi? [yes/no] yes
input five letter word CRANE

x  *  x  /  x
C  R  A  N  E
```
    
## Technical Highlight: Handling Duplicate Letters
**The problem**: The question "is this letter anywhere in the correct word?" breaks down with duplicate letters. If the answer is PEACH and you guess EERIE, a naive approach would mark both E's as "present" `(*)`, even though PEACH only contains one E. Wordle's rule is that each letter in the answer can only be "claimed" as many times as it actually appears.

**The fix**:  two-pass comparison with a running count:

1. First pass: Loop through all 5 positions and mark `/` wherever `guessLetters[j] == correctLetters[j]`. Each exact match increments `guessLetters_count[letter] `(a running tally of how many times this guess has already claimed that letter).
2.  Second pass: For any letter not already marked correct, check two conditions together:
  - Is the letter in the answer at all `(guessLetters[j] in correctLetters)`?
  - Has this guess not yet exceeded how many times that letter actually appears in the answer `(guessLetters_count[letter] <= correctLetter_counts[letter])`?

Only if both are true does it get marked `*`, and the running count increments again. Once the count catches up to the real number of occurrences, any further copies of that letter correctly fall through to `x`.

Running the count check after the exact-match pass is what prevents the double-E bug: any E's already "used up" by a correct-position match in step 1 reduce how many are left to be claimed as "present" in step 2.
The keyboard tracker (keyboard_checks) uses the same logic to avoid downgrading a letter's displayed status. If a letter was already shown as `/` from an earlier guess, a later `x` for that same letter in a different guess won't overwrite it back to unmarked.

## Key Python Techniques Used
 
* **Dictionaries:** Used to track per-letter guess counts and running keyboard status without needing parallel lists or repeated lookups.
* **`collections.Counter`:** Efficiently counted letter frequency in the correct word, forming the basis of the duplicate-letter comparison logic.
* **Two-pass comparison algorithm:** Solved the classic Wordle duplicate-letter edge case by resolving exact matches before evaluating "present" matches.
* 
## Possible improvements 

- GUI or web version
- Colour-coded terminal output instead of `/ * x` for user friendliness
- Hard mode (must reuse revealed hints)
- Stats tracking across games
