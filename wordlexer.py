from lark.lexer import Lexer, Token
from os import path


WORDTYPES = ["determiner", "noun", "linkingverb", "verb", "conjunction", "adjective", "adverb", "preposition"]
worddir = path.join(path.dirname(__file__), "wordlists")


def get_dictionary(word_type: str)->set:
    with open(path.join(worddir, word_type + ".txt"), "r") as f:
        return set([word.lower() for word in f.read().split("\n") if word!=""])


def set_dictionary(word_type: str, dictionary: set):
    with open(path.join(worddir, word_type + ".txt"), "w") as f:
        f.write("\n".join(sorted(dictionary)))


def get_word_types(dictionary={}):
    if dictionary == {}:
        for word_type in WORDTYPES:
            dictionary[word_type] = get_dictionary(word_type)
    return dictionary


class WordLexer(Lexer):
    def __init__(self, lexer_conf=None):
        self.expand_vocab = False
        self.dictionary = get_word_types()

    def save(self):
        if not self.expand_vocab:
            return
        for word_type in WORDTYPES:
            set_dictionary(word_type, self.dictionary[word_type])

    def lexword(self, word):
        word = word.lower()
        token = ""
        tokens = 0
        for word_type in WORDTYPES:
            if word in self.dictionary[word_type]:
                token += word_type.upper()
                tokens += 1
        if tokens > 4:
            token = "MANY"

        if token == "":
            if self.expand_vocab:
                print(", ".join(WORDTYPES))
                print("I don't know: ", word)
                word_type = input()
                self.dictionary[word_type].add(word)
            else:
                raise Exception("Unknown word: %s"%word)
        else:
            return Token("ambiguous_word__" + token, word)

    def lex(self, phrase):
        if phrase[-1] in ".!?":
            terminal = phrase[-1]
            phrase = phrase[:-1]
        else:
            terminal = "."
        if "`" in phrase:
            raise Exception("Unimplemented quote based noun phrases")


        sentence = phrase.split(" ")
        for word in sentence:
            yield self.lexword(word)
        if terminal == "?":
            yield Token("QUESTIONMARK", "?")
            
        self.save()
