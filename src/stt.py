import speech_recognition as sr
from logperformance import LogPerformance


class STT:
    def __init__(self) -> None:
        self.log = LogPerformance()
        self.recognizer = sr.Recognizer()

    def recognize_speech_from_mic(self) -> str:
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
