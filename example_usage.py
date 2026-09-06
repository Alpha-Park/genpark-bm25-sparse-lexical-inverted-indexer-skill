"""
Demonstration of genpark-bm25-sparse-lexical-inverted-indexer-skill
"""

from client import BM25LexicalIndexClient

def main():
    indexer = BM25LexicalIndexClient()

    docs = {
        "doc1": "Python is a popular programming language for AI and machine learning applications.",
        "doc2": "Machine learning models require clean training datasets and high quality features.",
        "doc3": "Delicious recipes for baking bread with sourdough starter."
    }

    for d_id, text in docs.items():
        indexer.index_document(d_id, text)

    results = indexer.search("machine learning models", top_k=2)
    print("=== OKAPI BM25 SEARCH RESULTS ===")
    for r in results:
        print(f"[{r['id']}] BM25 Score: {r['score']}")

if __name__ == "__main__":
    main()
