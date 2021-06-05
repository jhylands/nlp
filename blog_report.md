# Grammar, If brute force doesn't work, you aren't using enough.

## Introduction to grammars
One of the core concepts in computational complexity theory is the chompsky hiericky.
It is one of the first theoretical computer science topics taught in undergrad CS. One point from my learning of the grammars was closer to chompskys initial intention for his hieracky which is is talking about natural languages, rather than artificial ones.


# Sentences as a context free grammar
The idea is that by using a context free grammar one can parse an english sentence.

Take the simple grammar:
```lark
sentence: np vp
np: det? adj* noun
vp: verb advb* np?
```

This can be used to understand simple sentences like "A plane flies" or even "The cat sat on the mat". The parsing for such looks a little like this:
```
(sentence (np (det a) (noun plane)) (vp (verb flies)))
(sentence (np (det The) (noun cat)) (vp (verb sat) (adverb on) (np (det the) (noun mat))))
```
These would be better shown as the parse trees.

You can expand the grammar more and more
It turns out you need to expand the grammar substantially to account for a reasonable range of sentences. I was surprised by how many of my sentences use prepositional phrases.

When I was at school I had no interest in learning about grammars. I think the main reason for this was the learning was focused more about recalling lists of types of words than the links between all the elements.

# Why doesn't this work
As explained in this article as part of the natural language tool kit (nltk) ...

# How big can you go before it breaks?

One of the issues I've had is in both composing the right grammar

- also need to talk through the issues

Issues:
 - The ambiguity of POS tagging
 - sbar and prepositional phrases, how they expand the ambiguity unnesserily
 - Finding meaning in the parse trees
 - Limiting the tree depth with terminals
