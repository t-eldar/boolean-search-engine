from boolean_search_engine import (
    boolean_search,
    build_inverted_index,
    check_query_spell,
)
from wiki_crawler import download_wiki_texts


topic = "История_народов"
texts = download_wiki_texts(topic)

inverted_index = build_inverted_index(texts, topic)

query = "ссср"
corrected_query = check_query_spell(query, inverted_index)
print(f"Did you mean: {corrected_query}")

result = boolean_search(corrected_query, inverted_index)
print(f"Search results: {result}")
