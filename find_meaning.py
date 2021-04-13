from lark import Tree
import sys
from wordlexer import WordLexer
from parser import plot, p


collision_grammar = '''
start: sentence
sentence: declarative_sentence | interrogative_sentence | imperative_sentence
declarative_sentence: np vp
pp: preposition+ np
sbar: sentence | conjunction sentence
np: determiner? adjp? noun | np pp | np sbar
vp: vp np | vp pp | advp? vp advp?| verb+
adjp: adjective+
advp: adverb+
imperative_sentence: vp np
interrogative_sentence: qvp? np QUESTIONMARK
qvp: advp? verb? adjp| verb vp
QUESTIONMARK: "?"
%ignore " "
%import .ambiguous_word (determiner, noun, verb, pronoun, conjunction, adjective, adverb, preposition)
'''
def find_meaning(t: Tree):
    if t.data=="start":
        return find_meaning(t.children[0])
    if t.data=="_ambig":
        return "\n\n".join([find_meaning(child) or "" for child in t.children])
    if t.data=="declarative_sentence":
        np1, vp = t.children
        if len(vp.children)>1 and vp.children[1].data=="np":
            v, np2 = vp.children
            return "{}(\n{},\n{})".format(plot(v), plot(np1), plot(np2))
        elif len(vp.children)>1 and vp.children[1].data=="pp":
            v, pp = vp.children
            pp, np2 = pp.children
            return "{}{}(\n{},\n{})".format(plot(v.children[0]), plot(pp), plot(np1), plot(np2))
        elif len(vp.children)>1 and vp.children[1].data=="vp":
            v, vp1 = vp.children
            vp2, np2 = vp1.children
            return "{}_{}(\n{},\n{})".format(plot(v.children[0]), plot(vp2.children[0]), plot(np1), plot(np2))

def main(phrase):
    try:
        parsed_phrase = p.parse(phrase)
    except Exception as e:
        print(e)
        print(list(WordLexer().lex(phrase)))
        return
    try:
        meaning = find_meaning(parsed_phrase)
    except Exception:
        meaning = False
    if meaning:
        print(meaning)
    print("plot: ")
    print(plot(parsed_phrase))

if __name__=="__main__":
    phrase = sys.argv[1]
    main(phrase)
