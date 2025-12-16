from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import uuid
from chunking import chunk
from read_pdf import clean_text, reader

import os

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)
DIR_PROJECT = os.path.dirname(DIR_PATH)


class CVEmbeddingStore:

    """
    Docstring for CVEmbeddingStore
    Class dengan method
    1. ubah chunk to embedding
    2. search hasil embedding
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim)

        # metadata disimpan paralel
        self.metadatas = []
        self.texts = []

    def add_chunks(self, chunk_result: list, candidate_id: str):
        texts = []
        metadatas = []

        for chunk in chunk_result:
            texts.append(chunk["text"])
            metadatas.append({
                "id": str(uuid.uuid4()),
                "section": chunk["section"],
                "candidate_id": candidate_id,
                "source": "cv_upload"
            })

        embeddings = self.model.encode(texts,
                                       convert_to_numpy=True,
                                       normalize_embeddings=True)

        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query: str, top_k=3):
        if self.index.ntotal == 0:
            return []
        
        query_embedding = self.model.encode([query],
                                            convert_to_numpy=True,
                                            normalize_embeddings=True)
        distances, indices = self.index.search(
            np.array(query_embedding).astype("float32"), top_k
        )

        results = []
        for dist, idx in zip(distances[0],indices[0]):
            idx = int(idx)
            if idx < 0 or idx >= len(self.texts):
                continue
            results.append({
                "text": self.texts[idx],
                "metadata": self.metadatas[idx],
                "distance": float(dist)
            })

        return results


if __name__ == "__main__":
    pdf_path = os.path.join(DIR_PROJECT, "source",
                            "CV_Muhammad Arif Budiman.pdf")
    if not pdf_path.endswith(".pdf"):
        raise ValueError("Please input PDF file")

    read_pdf = reader(pdf_path=pdf_path)
    result_chunking = chunk(text=read_pdf)
    embedding = CVEmbeddingStore()
    embedding.add_chunks(
        chunk_result=result_chunking,
        candidate_id="arif_001"
    )

    results = embedding.search(
        "what kind of skills that user to apply as AI Engineer and minimun of his years experience")
    print("Pure result", results)
    print("============================")
    for r in results:
        print(r["metadata"]["section"])
        print(r["text"][:200])
