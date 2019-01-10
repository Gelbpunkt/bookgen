import nltk
import random

from collections import defaultdict

"""Some rules to fix spacing in results."""
ONLY_SPACE_AFTER = [".", "!", "?", ";", ",", ":", ")", "]", "}"]
ONLY_SPACE_BEFORE = ["(", "[", "{"]
SENTENCE_TERMINATORS = [".", "?", "!"]

"""We capitalize sentence beginnings after the terminators and these words (lowercase here)"""
NEEDS_CAPS = ["i"]


class BookGen:
    """A class representing a Book generator."""

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def download(self):
        """Downloads nltk packages needed."""
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("universal_tagset")

    @staticmethod
    def get_text(source):
        """
    	Gets the text from a source.
	This may be a file or URL.
	"""
        if source.startswith("http"):
            import requests

            return requests.get(source).text
        with open(source, "r") as file:
            return file.read()

    @staticmethod
    def prepare(text):
        """Tokenizes and parses the text."""
        tokenized = nltk.word_tokenize(text)
        return nltk.pos_tag(tokenized, tagset="universal")

    def run(self):
        """Generates the book."""
        source = self.prepare(self.get_text(self.source))
        target = self.prepare(self.get_text(self.target))
        words = defaultdict(list)
        for word, cls in source:
            words[cls].append(word)
        result = []
        for i, (orig, pos) in enumerate(target):
            if pos != ".":
                word = random.choice(words[pos])
                if (
                    i == 0
                    or result[i - 1][0] in SENTENCE_TERMINATORS
                    or word.lower() in NEEDS_CAPS
                ):
                    word = word.title()
                else:
                    word = word.lower()
                result.append((f" {word} ", pos))
            else:
                result.append((orig, pos))
        text = "".join(r[0] for r in result).replace("  ", " ")
        for rule in ONLY_SPACE_AFTER:
            text = text.replace(f" {rule} ", f"{rule} ")
        for rule in ONLY_SPACE_BEFORE:
            text = text.replace(f" {rule} ", f"{rule} ")
        if text.endswith(tuple(SENTENCE_TERMINATORS)):
            text = f"{text[:-2]}{text[-1]}"
        return text[1:]


"""
book = BookGen("wordbase.txt", "sentence_base.txt")
print(book.run())
"""

"""
Good examples are

Bible words:
https://raw.githubusercontent.com/mxw/grmr/master/src/finaltests/bible.txt

Harry Potter structure:
http://www.glozman.com/TextPages/Harry%20Potter%201%20-%20Sorcerer's%20Stone.txt
"""
