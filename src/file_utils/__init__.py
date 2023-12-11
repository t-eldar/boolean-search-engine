import os
import os.path


DEFAULT_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "out"
)


def is_file_exists(path):
    return os.path.exists(path)


def is_lemmatized_text_exists(category, text_number):
    path = os.path.join(DEFAULT_BASE_PATH, "lemmatized", category, f"{text_number}.txt")
    return is_file_exists(path)


def read_lemmatized_text(category, text_number):
    path = os.path.join(DEFAULT_BASE_PATH, "lemmatized", category, f"{text_number}.txt")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return "\n".join(lines)


def read_text_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        return "\n".join(lines)


def save_lemmatized_text(text, text_number, category):
    path = DEFAULT_BASE_PATH
    os.chdir(path)
    if not os.path.exists("lemmatized"):
        os.mkdir("lemmatized")
    os.chdir(f"{path}/lemmatized")
    if not os.path.exists(category):
        os.mkdir(category)
    os.chdir(f"{path}/lemmatized/{category}")

    filename = f"{text_number}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def save_text(text, text_number, category):
    path = DEFAULT_BASE_PATH
    os.chdir(path)
    if not os.path.exists("texts"):
        os.mkdir("texts")
    os.chdir(f"{path}/texts")
    if not os.path.exists(category):
        os.mkdir(category)
    os.chdir(f"{path}/texts/{category}")

    filename = f"{text_number}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
