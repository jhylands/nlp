from lark.lexer import Lexer, Token
from os import path


WORDTYPES = ["determiner", "noun", "verb", "pronoun", "conjunction", "adjective", "adverb", "preposition"]
worddir = path.join(path.dirname(__file__), "wordlists")


def get_word_types(dictionary={}):
    if dictionary == {}:
        for word_type in WORDTYPES:
            with open(path.join(worddir, word_type + ".txt"), "r") as f:
                dictionary[word_type] = set([word.lower() for word in f.read().split("\n") if word!=""])
    return dictionary


class WordLexer(Lexer):
    def __init__(self, lexer_conf=None):
        self.expand_vocab = True
        self.dictionary = get_word_types()

    def save(self):
        if not self.expand_vocab:
            return
        for word_type in WORDTYPES:
            with open(path.join(worddir, word_type + ".txt"), "w") as f:
                f.write("\n".join(self.dictionary[word_type]))

    def lex(self, phrase):
        if phrase[-1] in ".!?":
            terminal = phrase[-1]
            phrase = phrase[:-1]
        else:
            terminal = "."
        sentence = phrase.split(" ")
        for word in sentence:
            word = word.lower()
            token = ""
            for word_type in WORDTYPES:
                if word in self.dictionary[word_type]:
                    token += word_type.upper()

            if token == "":
                if self.expand_vocab:
                    print(", ".join(WORDTYPES))
                    print("I don't know: ", word)
                    word_type = input()
                    self.dictionary[word_type].add(word)
                else:
                    raise Exception("Unknown word: %s"%word)
            else:
                yield Token("ambiguous_word__" + token, word)
        if terminal == "?":
            yield Token("QUESTIONMARK", "?")
            
        self.save()

