from openai import OpenAI
import faiss
import numpy as np
import json
from config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

class EmbeddingStore:
    def __init__(self, example_file="embedding_examples.json", fewshot_file="fewshot_examples.json"):
        self.examples = self.load_examples(example_file)
        self.fewshot_examples = self.load_examples(fewshot_file)
        self.texts = [ex["input"] for ex in self.examples]
        self.index = None
        self.embeddings = self.compute_embeddings()

    def load_examples(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def compute_embeddings(self):
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=self.texts
        )
        vectors = [d.embedding for d in response.data]
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        if not vectors:
            raise ValueError("No embeddings found.")
        self.index.add(np.array(vectors).astype("float32"))
        return vectors

    def get_fewshot_examples(self):
        return self.fewshot_examples

    def search_and_decide(self, query, direct_threshold=0.1):
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
        query_vector = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_vector, 1)  # top_k = 1 for direct match check

        closest_distance = distances[0][0]
        closest_index = indices[0][0]

        if closest_distance < direct_threshold:
            print("✅ 유사도 높음 → 예시 코드 직접 실행")
            return {
                "type": "direct",
                "code": self.examples[closest_index]["code"]
            }
        else:
            print("🤖 유사도 낮음 → GPT로 코드 생성 요청")
            examples = self.get_fewshot_examples()
            return {
                "type": "gpt",
                "examples": examples
            }
