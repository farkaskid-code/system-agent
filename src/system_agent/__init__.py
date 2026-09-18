import sys

from .core.llm_client import LLMClient


def main() -> None:
    url = "http://192.168.137.1:11434/v1/chat/completions"
    model_name = "qwen2.5-coder:14b"

    print(LLMClient(url, model_name).call_model(sys.argv[1]))
