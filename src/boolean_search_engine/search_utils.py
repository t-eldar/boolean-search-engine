import re


def bigram_distance(first, second):
    bigrams_s1 = set(zip(first[:-1], first[1:]))
    bigrams_s2 = set(zip(second[:-1], second[1:]))

    intersection = len(bigrams_s1 & bigrams_s2)
    union = len(bigrams_s1 | bigrams_s2)

    return 1 - intersection / union if union != 0 else 0


def is_russian_word(word):
    return bool(re.search("[а-яА-Я]", word))
