from itertools import combinations
from wordlexer import WORDTYPES


def getall():
    d = dict([(t, []) for t in WORDTYPES])
    for i in range(1, 5):
        print(i)
        for option in combinations(WORDTYPES, i):
            for t in WORDTYPES:
                if t in option:
                    d[t].append("".join([c.upper() for c in option]))
    return d


def make():
    d = getall()
    acc = ""
    full_token_list = ["MANY"]
    for key, value in d.items():
        also = ["MANY"]
        # Some sets should be super sets of others
        if key=="verb":
            also.append("linkingverb")
        acc += key + ": " + " | ".join(value + also) + "\n"
        full_token_list += value
    acc += "%declare " + " ".join(set(full_token_list))
    with open("ambiguous_word.lark", "w") as f:
        f.write(acc)


if __name__=="__main__":
    make()
