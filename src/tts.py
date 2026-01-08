from edge_tts import Communicate
from asyncio import run
from pygame import mixer, time
from re import sub
from logperformance import LogPerformance


class TTS:
    def __init__(self, voice: str):
        self.voice = voice
        self.log = LogPerformance()

    async def generate_audio(self, text: str, file_output: str) -> None:
        if not text or not text.strip():
            raise ValueError("O texto não pode estar vazio")

        comm = Communicate(text=self.clean_text(text), voice=self.voice)
        await comm.save(file_output)

    def play_audio(self, text: str, file_output: str = "output.mp3") -> None:
        if not text or not text.strip():
            self.log.warning("Aviso: Texto vazio, nenhum áudio será gerado")
            return
        run(self.generate_audio(text, file_output))
        self.run_audio(file_output)

    def clean_text(self, text: str) -> str:
        return sub(r"[^a-zA-Z0-9\s]", "", text)

    def run_audio(self, file_output: str) -> None:
        mixer.init()
        mixer.music.load(file_output)
        mixer.music.play()
        while True:
            if not mixer.music.get_busy():
                break
            time.wait(10)
        mixer.quit()
