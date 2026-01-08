import ollama
from typing import Union, Dict, Any, Tuple, List
from src.memory import get_memory, save_memory, save_conversation, get_conversation_context, extract_user_info
from logperformance import LogPerformance


class Servo:
    wrapes_is_learning = ["aprenda", "escute", "leia", "veja", "treine"]

    def __init__(self, model: str):
        self.model = model
        self.memory = Union[Dict[str, Any], None]
        self.response: Union[ollama.ChatResponse, None] = None
        self.log = LogPerformance()

    def chat(self, message: str, session_history: List[Dict[str, str]] = None) -> str:
        """Processa a mensagem com aprendizado contínuo baseado no histórico."""
        self.memory = get_memory()
        system_message = self.memory.get("personalidade", "")

        # Adiciona informações do usuário ao contexto do sistema
        user_info = self.memory.get("informacoes_usuario", {})
        if user_info:
            info_text = "Informações sobre o usuário: "
            if "nome" in user_info:
                info_text += f"O nome do usuário é {user_info['nome']}. "
            if "idade" in user_info:
                info_text += f"O usuário tem {user_info['idade']} anos. "
            if "cidade" in user_info:
                info_text += f"O usuário mora em {user_info['cidade']}. "
            system_message = f"{system_message}\n\n{info_text}"

        is_exists, resposta = self.check_exists_response(message)
        if is_exists:
            save_conversation(message, resposta)
            return resposta

        messages = [{"role": "system", "content": system_message}]

        context = get_conversation_context(limit=50)
        if context:
            messages.append(
                {"role": "system", "content": f"{context}\nUse este contexto para manter consistência nas respostas."}
            )

        if session_history:
            for hist in session_history[-3:]:
                messages.append({"role": "user", "content": hist.get("user", "")})
                messages.append({"role": "assistant", "content": hist.get("assistant", "")})

        messages.append({"role": "user", "content": message})

        self.response = ollama.chat(
            model=self.model,
            messages=messages,
        )

        response_text = self.response.message.content or ""
        self.log.info(f"Resposta: {response_text}")

        save_conversation(message, response_text)
        extract_user_info(message, response_text)

        if self.check_is_learning(message):
            save_memory(message, response_text)

        return response_text

    def check_exists_response(self, message: str) -> Tuple[bool, Union[str, None]]:
        """Verifica se já existe uma resposta aprendida para a mensagem."""
        respostas = self.memory.get("respostas_aprendidas", [])
        for question in respostas:
            if question["pergunta"] == message:
                return True, question["resposta"]
        return False, None

    @classmethod
    def check_is_learning(cls, message: str) -> bool:
        """Verifica se a mensagem contém palavras-chave de aprendizado explícito."""
        return bool(set(message.lower().split(" ")) & set(cls.wrapes_is_learning))
