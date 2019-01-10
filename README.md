# bookgen

A python library using nltk to analyse two books and generate a new one.

## Installation

`pip install bookgen`

## Usage

```py
from bookgen import BookGen

book = BookGen("word_base_book.txt", "sentence_base_book.txt")
# book.download() will download the nltk extras required, only needed once

print(book.run())
```

## Explanation

BookGen will parse word classes from the first specified book, looking like this:

`{"NOUN": ["Mountain", "Valley"], "VERB": ["take", "went"]}`

These are sorted by the nltk universal tagset.

The second book serves as sentence base. It will be parsed into a list of word types that represent the whole book.

`["NOUN", "VERB", "PREP", "NOUN", "CONJ", "VERB", "."]`

Then, it generates a list of words from the words of the first book based on the second book.

`["Nathan", "went", "to", "Valley", "and", "peed", "."]`

This is joined with some capitalization fixes and returned.
