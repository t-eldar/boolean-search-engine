from collections import defaultdict

from pymystem3 import Mystem

from boolean_search_engine.search_utils import bigram_distance, is_russian_word
from file_utils import (
    is_lemmatized_text_exists,
    read_lemmatized_text,
    save_lemmatized_text,
)


class Lemmatizer:
    mystem = Mystem()

    def lemmatize_text(self, text, category=None, text_number=None):
        def lemmatize(text):
            lowered = text.lower()
            return list(filter(is_russian_word, self.mystem.lemmatize(lowered)))

        if not text_number or not category:
            return lemmatize(text)

        if is_lemmatized_text_exists(category, text_number):
            lemmas = read_lemmatized_text(category, text_number).split()
        else:
            lemmas = lemmatize(text)
            save_lemmatized_text(" ".join(lemmas), text_number, category)

        return lemmas


lemmatizer = Lemmatizer()


def check_query_spell(query, inverted_index):
    words = lemmatizer.lemmatize_text(query)
    corrected_query = []

    print(words)

    for word in words:
        if word not in inverted_index:
            closest_word = min(
                inverted_index.keys(), key=lambda x: bigram_distance(word, x)
            )
            corrected_query.append(closest_word)
        else:
            corrected_query.append(word)

    return " ".join(corrected_query)


def extract_words(text, category, text_number):
    lemmatized = list(
        filter(is_russian_word, lemmatizer.lemmatize_text(text, category, text_number))
    )

    return lemmatized


def build_inverted_index(texts, category):
    inverted_index = defaultdict(set)
    for _, text in enumerate(texts):
        content, num = text
        words = extract_words(content, category, num)

        for word in words:
            inverted_index[word].add(f"{num}.txt")

    return inverted_index


def boolean_search(query, inverted_index):
    query_words = lemmatizer.lemmatize_text(query)

    operators = {"AND", "OR", "NOT"}
    result = None

    for word in query_words:
        if word not in operators:
            if result is None:
                result = inverted_index.get(word, set())
            else:
                result = result.intersection(inverted_index.get(word, set()))

    return result if result else set()
