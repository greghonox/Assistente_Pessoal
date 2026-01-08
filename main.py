"""
Exemplo interativo: Chat com o Ollama
Execute este arquivo para ter uma conversa interativa com o modelo
"""

from src.servo import Servo
from src.tts import TTS
from src.stt import STT
from logperformance import LogPerformance


class Main:
    def __init__(self) -> None:
        """Inicializa as classes de reconhecimento de voz, síntese de voz e processamento de linguagem natural."""
        self.stt = STT()
        self.tts = TTS("pt-BR-ThalitaMultilingualNeural")
        self.servo = Servo("servo")
        self.log = LogPerformance()

    def response(self, text: str) -> None:
        """Processa a resposta do assistente."""
        response = self.servo.chat(text)
        self.tts.play_audio(response)

    def run(self) -> None:
        while True:
            text = self.stt.recognize_speech_from_mic()
            self.log.info(f"Você: {text}")
            if text.lower() in ["sair", "exit", "quit"]:
                self.log.info("Saindo...")
                break
            if text != "Não foi possível entender o áudio":
                self.response(text)


if __name__ == "__main__":
    main = Main()
    main.run()
