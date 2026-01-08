"""
Exemplo interativo: Chat com o Ollama
Execute este arquivo para ter uma conversa interativa com o modelo
"""

from src.servo import Servo
from src.tts import TTS
from src.stt import STT
from logperformance import LogPerformance
from typing import List, Dict


class Main:
    def __init__(self, use_wake_word: bool = True) -> None:
        """Inicializa classes de reconhecimento de voz, síntese de voz
        e processamento de linguagem natural.

        Args:
            use_wake_word: Se True, usa detecção de wake word.
                          Se False, escuta continuamente.
        """
        self.stt = STT()
        self.tts = TTS("pt-BR-ThalitaMultilingualNeural")
        self.servo = Servo("servo")
        self.log = LogPerformance()
        self.session_history: List[Dict[str, str]] = []
        self.use_wake_word = use_wake_word

    def response(self, text: str) -> None:
        """Processa a resposta do assistente com aprendizado contínuo."""
        response = self.servo.chat(text, session_history=self.session_history)
        self.session_history.append({"user": text, "assistant": response})

        if len(self.session_history) > 10:
            self.session_history = self.session_history[-10:]

        self.tts.play_audio(response)

    def run(self) -> None:
        """Executa o loop principal com ou sem detecção de wake word."""
        if self.use_wake_word:
            self.log.info("Assistente iniciado. Diga 'ok assistente' para ativar.")
        else:
            self.log.info("Assistente iniciado. Modo contínuo ativado.")

        while True:
            if self.use_wake_word:
                self.tts.play_beep()
                self.stt.wait_for_wake_word()
                self.tts.play_beep()
                text = self.stt.recognize_after_wake_word()
            else:
                self.tts.play_beep()
                text = self.stt.recognize_speech_from_mic()

            self.log.warning(f"Você: {text}")

            # Verifica comandos de saída
            if text.lower() in ["sair", "exit", "quit", "desligar"]:
                self.log.info("Saindo...")
                break

            # Processa o comando se foi entendido
            if text and text != "Não foi possível entender o áudio":
                self.response(text)


if __name__ == "__main__":
    main = Main()
    main.run()
