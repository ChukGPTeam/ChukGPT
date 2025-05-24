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
        if not self.texts:
            raise ValueError("No example texts to embed.")
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=self.texts
        )
        vectors = [d.embedding for d in response.data]
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors).astype("float32"))
        return vectors

    def get_fewshot_examples(self):
        return self.fewshot_examples

    def search_and_decide(self, query, direct_threshold=0.1, similarity_threshold=0.5):
        # Get query embedding
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query
        )
        query_vector = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

        distances, indices = self.index.search(query_vector, 1)
        closest_distance = distances[0][0]
        closest_index = indices[0][0]

        similarity = 1 - closest_distance  # 대략적으로 거리를 유사도로 변환 (IndexFlatL2는 거리임)

        matched_example = self.examples[closest_index]

        if closest_distance < direct_threshold:
            # 아주 가까운 매칭
            return {
                "type": "direct",
                "code": matched_example["code"],
                "description": matched_example.get("description", "정확한 명령어입니다."),
            }
        elif similarity >= similarity_threshold:
            # 유사도 적당히 높은 경우, 사용자에게 확인 후 실행
            return {
                "type": "confirm",
                "code": matched_example["code"],
                "description": matched_example.get("description", "유사한 명령어입니다."),
                "matched_input": matched_example["input"],
                "similarity": similarity,
            }
        else:
            # 유사도 낮음 → GPT 코드 생성 요청
            return {
                "type": "gpt",
                "examples": self.get_fewshot_examples()
            }
