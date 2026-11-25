# CFG Sentence Generator

A small command-line tool that reads a context-free grammar from a text file (or stdin) and prints random sentences generated from it.

Made for the class Python for Linguists 2.

```
$ python grammar.py -f example_grammar.txt -n 5
a tall kid loves the dog
the dog runs
the dog runs every day
a dog runs every day
a dog loves the tall dog
```

## Usage

Requires Python 3.9 or later. There are no dependencies.

```
python grammar.py -f GRAMMAR_FILE [-n COUNT]
python grammar.py [-n COUNT] < GRAMMAR_FILE
```

| Option | Meaning |
|---|---|
| `-f`, `--file` | Text file containing the grammar. If omitted, the grammar is read from standard input. |
| `-n` | Number of sentences to generate (default: 1). |

Because it reads from stdin, it works in a pipeline:

```
$ printf 's -> greeting name\ngreeting -> "hello"\ngreeting -> "hi"\nname -> "world"\nname -> "Leiden"\n' | python grammar.py -n 3
hello Leiden
hi world
hello Leiden
```

## Grammar format

One rule per line, written `LEFT -> RIGHT` (with spaces around the arrow):

```
s -> dp vp
s -> dp vp adv
dp -> det np
np -> n
np -> adj n
vp -> iv
vp -> tv dp
det -> "the"
det -> "a"
adj -> "tall"
n -> "kid"
n -> "dog"
iv -> "runs"
tv -> "loves"
adv -> "every day"
```

- **Start symbol:** the left-hand side of the first rule (`s` above).
- **Nonterminals** are the symbols that appear on the left of a rule. They are separated by spaces and expanded until none are left.
- **Terminals** are written in double quotes. A quoted terminal can contain spaces (`"every day"`), and the quotes are removed from the output.
- **Several rules for one symbol** are alternatives, and one is chosen uniformly at random each time the symbol is expanded.
- **Blank lines** are ignored.

## How it works

Generation starts from the start symbol and repeatedly replaces the leftmost nonterminal with the right-hand side of a randomly chosen rule for it, until only terminals remain. Recursive rules (such as `np -> "dog" pp` with `pp -> "near" np`) are supported.

## Limitations

- A word that is not defined as a nonterminal is printed as it is, so a typo in a symbol name does not raise an error. Quote your terminals to keep them distinct from symbols.
- Rules are chosen uniformly. There are no rule weights.
- A grammar that can never finish (for example `s -> s s` as the only rule for `s`) will run forever.
- Malformed rules, such as a line with no ` -> `, are not reported with a helpful message yet.

## Ideas for later

- Weighted rules.
- Output as bracketed trees, for example `[s [dp [det the] [np kid]] [vp runs]]`.
- A recogniser (CKY) that parses sentences with the same grammar.
- Tests.
