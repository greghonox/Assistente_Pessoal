from json import load
from json import dump, JSONDecodeError
from typing import Any, Dict, List
from datetime import datetime
from os.path import join
import re


def get_memory() -> Dict[str, Any]:
    with open(join("src", "memory.json"), "r", encoding="utf-8") as file:
        try:
            return load(file)
        except JSONDecodeError:
            return {"respostas_aprendidas": [], "historico_conversas": [], "informacoes_usuario": {}}


def save_memory(message: str, response: str) -> None:
    """Salva uma interação na memória (mantido para compatibilidade)."""
    memory = get_memory()
    memory["respostas_aprendidas"].append(
        {"pergunta": message, "resposta": response, "timestamp": datetime.now().isoformat()}
    )  # noqa: E501
    with open("src/memory.json", "w", encoding="utf-8") as file:
        dump(memory, file, indent=4, ensure_ascii=False)


def save_conversation(message: str, response: str) -> None:
    """Salva uma conversa no histórico para aprendizado contínuo."""
    memory = get_memory()

    # Inicializa histórico se não existir
    if "historico_conversas" not in memory:
        memory["historico_conversas"] = []

    # Adiciona a conversa com timestamp
    conversation = {"pergunta": message, "resposta": response, "timestamp": datetime.now().isoformat()}
    memory["historico_conversas"].append(conversation)

    # Mantém apenas as últimas 100 conversas para não sobrecarregar
    if len(memory["historico_conversas"]) > 100:
        memory["historico_conversas"] = memory["historico_conversas"][-100:]

    with open("src/memory.json", "w", encoding="utf-8") as file:
        dump(memory, file, indent=4, ensure_ascii=False)


def get_recent_conversations(limit: int = 10) -> List[Dict[str, str]]:
    """Retorna as conversas recentes para usar como contexto."""
    memory = get_memory()
    historico = memory.get("historico_conversas", [])
    return historico[-limit:] if historico else []


def get_conversation_context(limit: int = 10) -> str:
    """Retorna o contexto das conversas recentes formatado para o modelo."""
    conversations = get_recent_conversations(limit)
    if not conversations:
        return ""

    context = "Contexto de conversas anteriores:\n"
    for conv in conversations:
        context += f"Usuário: {conv['pergunta']}\n"
        context += f"Assistente: {conv['resposta']}\n\n"

    return context


def extract_user_info(message: str, response: str) -> None:
    """Extrai e salva informações sobre o usuário da conversa."""
    memory = get_memory()

    if "informacoes_usuario" not in memory:
        memory["informacoes_usuario"] = {}

    message_lower = message.lower()

    # Extrai nome do usuário
    if "meu nome é" in message_lower or "eu sou" in message_lower or "me chamo" in message_lower:
        # Tenta extrair o nome
        patterns = [r"meu nome é (\w+)", r"eu sou (\w+)", r"me chamo (\w+)", r"nome é (\w+)"]
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                memory["informacoes_usuario"]["nome"] = match.group(1).capitalize()
                break

    # Extrai outras informações comuns
    if "eu tenho" in message_lower or "minha idade é" in message_lower:
        idade_match = re.search(r"(\d+)\s*anos?", message_lower)
        if idade_match:
            memory["informacoes_usuario"]["idade"] = idade_match.group(1)

    if "moro em" in message_lower or "sou de" in message_lower:
        # Tenta extrair cidade (simplificado)
        cidade_match = re.search(r"(?:moro em|sou de)\s+([A-Za-záàâãéèêíïóôõöúçñ]+)", message)
        if cidade_match:
            memory["informacoes_usuario"]["cidade"] = cidade_match.group(1)

    with open("src/memory.json", "w", encoding="utf-8") as file:
        dump(memory, file, indent=4, ensure_ascii=False)
