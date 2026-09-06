"""
Okapi BM25 Sparse Lexical Search Engine.
Zero external dependencies, standard library only.
"""

import math
import re
from typing import Dict, List, Any, Optional

class BM25LexicalIndexClient:
    """
    Implements Okapi BM25 ranking function for sparse keyword search:
    - Robertson-Spärck Jones Inverse Document Frequency (IDF)
    - Term frequency saturation parameter (k1)
    - Document length normalization parameter (b)
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_corpus = {} # doc_id -> list of tokens
        self.doc_lengths = {}
        self.avg_doc_length = 0.0
        self.df = {} # term -> doc count

    def tokenize(self, text: str) -> List[str]:
        """Simple alphanumeric tokenizer."""
        return [t.lower() for t in re.findall(r"\b[a-zA-Z0-9_]+\b", text)]

    def index_document(self, doc_id: str, content: str):
        """Indexes a text document."""
        tokens = self.tokenize(content)
        self.doc_corpus[doc_id] = tokens
        self.doc_lengths[doc_id] = len(tokens)

        unique_tokens = set(tokens)
        for t in unique_tokens:
            self.df[t] = self.df.get(t, 0) + 1

        self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)

    def _idf(self, term: str) -> float:
        n = len(self.doc_corpus)
        df = self.df.get(term, 0)
        # Standard RSJ IDF formula with smoothing
        return math.log(1.0 + (n - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Scores all documents against query terms using Okapi BM25."""
        query_terms = self.tokenize(query)
        scores = {}

        for doc_id, tokens in self.doc_corpus.items():
            doc_len = self.doc_lengths[doc_id]
            doc_score = 0.0

            # Count term frequencies
            tf_dict = {}
            for t in tokens:
                tf_dict[t] = tf_dict.get(t, 0) + 1

            for qt in query_terms:
                tf = tf_dict.get(qt, 0)
                if tf > 0:
                    idf = self._idf(qt)
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_length))
                    doc_score += idf * (tf * (self.k1 + 1.0)) / denom

            if doc_score > 0.0:
                scores[doc_id] = doc_score

        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{"id": d_id, "score": round(score, 4)} for d_id, score in sorted_docs[:top_k]]
