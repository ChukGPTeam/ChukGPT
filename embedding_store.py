import json
import os
import re
import difflib

class EmbeddingStore:
    def __init__(self, path="embedding_examples.json"):
        # JSON 파일에서 명령어 예제 불러오기
        with open(path, "r", encoding="utf-8") as f:
            self.examples = json.load(f)

    def normalize(self, text):
        """
        숫자를 {num}으로 치환하여 비교를 위한 정규화 수행
        예: "화면 밝기 80" -> "화면 밝기 {num}"
        """
        return re.sub(r"\d+", "{num}", text)

    def search_and_decide(self, user_input):
        normalized_input = self.normalize(user_input)

        inputs = [ex["input"] for ex in self.examples]
        normalized_inputs = [self.normalize(inp) for inp in inputs]

        # 가장 비슷한 정규화된 명령어 찾기
        matches = difflib.get_close_matches(normalized_input, normalized_inputs, n=1, cutoff=0.6)

        if not matches:
            # GPT로 위임
            return {
                "type": "gpt",
                "examples": self.examples
            }

        match = matches[0]
        matched_index = normalized_inputs.index(match)
        example = self.examples[matched_index]

        if match == normalized_input:
            # 완전 일치
            return {
                "type": "direct",
                "matched_input": inputs[matched_index],
                "description": example.get("description", ""),
                "code": example["code"]
            }

        # 유사하지만 확인 필요
        return {
            "type": "confirm",
            "matched_input": inputs[matched_index],
            "similarity": difflib.SequenceMatcher(None, normalized_input, match).ratio(),
            "description": example.get("description", ""),
            "code": example["code"]
        }
