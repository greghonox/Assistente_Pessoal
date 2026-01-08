import speech_recognition as sr
from logperformance import LogPerformance
from typing import Optional, List


class STT:
    def __init__(self, wake_words: Optional[List[str]] = None) -> None:
        self.log = LogPerformance()
        self.recognizer = sr.Recognizer()
        self.wake_words = wake_words or ["ok assistente", "assistente", "ok servo"]

    def recognize_speech_from_mic(self) -> str:
        """Reconhece fala do microfone."""
        with sr.Microphone() as source:
            self.log.info("Escutando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        self.log.warning("Reconhecendo...")
        try:
            return self.recognizer.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio"
        except sr.RequestError:
            return "Erro ao solicitar o serviço de reconhecimento de fala"

    def listen_for_wake_word(self, timeout: int = 1, phrase_time_limit: int = 3) -> bool:
        """Escuta continuamente até detectar uma wake word.

        Args:
            timeout: Tempo máximo para escutar antes de verificar novamente
            phrase_time_limit: Tempo máximo de uma frase

        Returns:
            True se wake word foi detectada, False caso contrário
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                # Escuta por um período curto
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio, language="pt-BR").lower()

                # Verifica se alguma wake word foi detectada
                for wake_word in self.wake_words:
                    if wake_word.lower() in text:
                        self.log.info(f"Wake word detectada: '{wake_word}'")
                        return True
                return False
            except sr.WaitTimeoutError:
                # Timeout é normal quando não há fala
                return False
            except sr.UnknownValueError:
                # Áudio não reconhecível
                return False
            except sr.RequestError as e:
                self.log.warning(f"Erro ao acessar serviço de reconhecimento: {e}")
                return False

    def wait_for_wake_word(self) -> None:
        """Fica em loop esperando pela wake word."""
        self.log.info("Aguardando wake word... (diga 'ok assistente')")
        while True:
            if self.listen_for_wake_word():
                self.log.info("Wake word detectada! Escutando comando...")
                break

    def recognize_after_wake_word(self) -> str:
        """Reconhece o comando após a wake word ser detectada."""
        with sr.Microphone() as source:
            self.log.info("Escutando comando...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            # Escuta por mais tempo para capturar o comando completo
            audio = self.recognizer.listen(source, phrase_time_limit=5)

        self.log.warning("Reconhecendo comando...")
        try:
            text = self.recognizer.recognize_google(audio, language="pt-BR")
            # Remove a wake word do texto se estiver presente
            for wake_word in self.wake_words:
                text = text.replace(wake_word, "").strip()
            return text
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio"
        except sr.RequestError:
            return "Erro ao solicitar o serviço de reconhecimento de fala"
