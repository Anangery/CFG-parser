from argparse import ArgumentParser, Namespace
from sys import stdin
from random import choice


def parse_arguments() -> tuple[str, int]:
    """Parses the arguments passed into the function from an optional file, otherwise from standard in.
    
    arguments:
        None
    output:
        replacement_grammar: str; string containing the contents of the input replacement grammar from either stdin or an optional file
        number: int; number of generated sentences, default is 1
    """

    parser = ArgumentParser(
                        prog='Text replacement grammar',
                        description='Takes a grammar input from stdin or an optional file and outputs sentences')

    parser.add_argument("-f", "--file", help="text file containing a grammar")
    parser.add_argument("-n", help="Number of generated sentences", type=int, default=1)
    args: Namespace = parser.parse_args()

    replacement_grammar: str = ""

    if args.file:
        replacement_grammar = open(args.file).read()
    else:
        replacement_grammar = stdin.read()

    number: int = args.n

    return (replacement_grammar, number)


def parse_grammar(grammar_text: str) -> dict[str, list[str]]:
    """Parses a given string of replacement grammar into a dictionary with rules
    
    arguments:
        grammar_text: str; string of replacement grammar rules
    output:
        grammar_rules: dict[str, list[str]]; dictionary mapping replacement rules
    """

    grammar_rules: dict[str, list[str]] = {}

    grammar_list: list[str] = grammar_text.split("\n")
    for rule in grammar_list:
        if not rule.strip():
            continue
        rules: list[str] = rule.split(" -> ")
        if rules[0] in grammar_rules:
            grammar_rules[rules[0]].append(rules[1])
        else:
            grammar_rules[rules[0]] = [rules[1]]

    return grammar_rules

def generate_sentence(grammar_rules: dict[str, list[str]], max_steps: int = 10_000) -> str:
    """Generates a random sentence based on given replacement grammar rules

    arguments:
        grammar_rules: dict[str, list[str]]; dictionary mapping replacement rules
        max_steps: int; maximum amount of iterations before halting to prevent infinite recursion
    output:
        random_sentence: str; randomly generated sentence based on the replacement rules
    """

    random_sentence: str = list(grammar_rules.keys())[0]
    sentence_array: list = random_sentence.split()

    i = 0
    steps = 0
    while i < len(sentence_array):
        if steps >= max_steps:
            raise RecursionError("grammar did not terminate!")
        word = sentence_array[i]
        if word in grammar_rules:
            sentence_array[i:i+1] = choice(grammar_rules[word]).split()
        else:
            i += 1
        steps += 1

    random_sentence = " ".join(sentence_array).replace('"', '')

    return random_sentence



if __name__ == "__main__":

    # Parse the arguments passed into the file
    arguments: tuple[str, int] = parse_arguments()
    replacement_grammar: str = arguments[0]
    number: int = arguments[1]


    # Generates the grammar rules and n random sentences
    grammar_rules: dict[str, list[str]] = parse_grammar(replacement_grammar)
    for i in range(number):
        sentence: str = generate_sentence(grammar_rules)
        print(sentence)
