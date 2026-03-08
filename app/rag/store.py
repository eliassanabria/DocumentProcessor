from dataclasses import dataclass
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class ChunkRecord:
    chunk_id: str
    text: str


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.records: List[ChunkRecord] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = None

    def add_records(self, records: List[ChunkRecord]) -> None:
        self.records.extend(records)
        corpus = [record.text for record in self.records]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def search(self, query: str, top_k: int = 4) -> List[ChunkRecord]:
        if not self.records or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = (self.matrix @ query_vector.T).toarray().ravel()

        ranked_indices = scores.argsort()[::-1][:top_k]
        return [self.records[index] for index in ranked_indices if scores[index] > 0]