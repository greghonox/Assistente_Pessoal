from json import load
from json import dump, JSONDecodeError
from typing import Any, Dict


def get_memory() -> Dict[str, Any]:
    with open("src/memory.json", "r", encoding="utf-8") as file:
        try:
            return load(file)
        except JSONDecodeError:
            return {"respostas_aprendidas": []}


def save_memory(message: str, response: str) -> None:
    memory = get_memory()
    memory["respostas_aprendidas"].append({"pergunta": message, "resposta": response})  # noqa: E501
    with open("src/memory.json", "w", encoding="utf-8") as file:
        dump(memory, file, indent=4)
