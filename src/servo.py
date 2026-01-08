import ollama
from typing import Union, Dict, Any, Tuple
from src.memory import get_memory, save_memory
from logperformance import LogPerformance


class Servo:
    wrapes_is_learning = ["aprenda", "escute", "leia", "veja", "treine"]

    def __init__(self, model: str):
        self.model = model
        self.memory = Union[Dict[str, Any], None]
        self.response: Union[ollama.ChatResponse, None] = None
        self.log = LogPerformance()

    def chat(self, message: str) -> str:
        self.memory = get_memory()
        system_message = self.memory["personalidade"]
        is_exists, resposta = self.check_exists_response(message)
        if is_exists:
            return resposta

        self.response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message},
            ],
        )
        self.log.info(f"Resposta: {self.response.message.content}")
        if self.check_is_learning(message):
            save_memory(message, self.response.message.content or "")
        return self.response.message.content

    def check_exists_response(self, message: str) -> Tuple[bool, Union[str, None]]:
        for question in self.memory["respostas_aprendidas"]:
            if question["pergunta"] == message:
                return True, question["resposta"]
        return False, None

    @classmethod
    def check_is_learning(cls, message: str) -> bool:
        return bool(set(message.lower().split(" ")) & set(cls.wrapes_is_learning))
