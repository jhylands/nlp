from wordlexer import WordLexer, WORDTYPES, get_dictionary, set_dictionary
import argparse



def main():
    parser = argparse.ArgumentParser(description='Quick script for editing the dictionaries')
    subparsers = parser.add_subparsers(dest="program")
    lex = subparsers.add_parser("lex")
    lex.add_argument('value')
    subparsers.add_parser("types")

    subparsers.add_parser("types")
    add = subparsers.add_parser("add")
    add.add_argument('word', help="The word to add")
    add.add_argument('dictionary', choices=WORDTYPES, help="The dictionary from which to add it")
    rm = subparsers.add_parser("remove", aliases=["rm"])
    rm.add_argument('word', help="The word to remove")
    rm.add_argument('dictionary', choices=WORDTYPES, help="The dictionary from which to remove it")


    #parser.add_argument('function', choices=["dictionary", "add", "lex", "types"])
    namespace = parser.parse_args()
    if namespace.program=="lex":
        print(namespace.value)
        print(WordLexer().lexword(namespace.value).__repr__())
    elif namespace.program=="types":
        print(WORDTYPES)
    elif namespace.program=="add":
        dictionary = get_dictionary(namespace.dictionary)
        dictionary.add(namespace.word)
        set_dictionary(namespace.dictionary, dictionary)
    elif namespace.program=="rm":
        dictionary = get_dictionary(namespace.dictionary)
        dictionary.discard(namespace.word)
        set_dictionary(namespace.dictionary, dictionary)
        


if __name__=="__main__":
    main()
