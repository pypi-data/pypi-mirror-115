import subprocess
from ovos_plugin_manager.templates.tts import TTS, TTSValidator


class PicoTTS(TTS):
    def __init__(self, *args, **kwargs):
        if "lang" not in kwargs:
            kwargs["lang"] = "en-us"
        if "config" not in kwargs:
            kwargs["config"] = {}
        super().__init__(*args, **kwargs, audio_ext="wav",
                         validator=PicoTTSValidator(self))
        if not self.voice:
            if self.lang.startswith("de"):
                self.voice = "de-DE"
            elif self.lang.startswith("es"):
                self.voice = "es-ES"
            elif self.lang.startswith("fr"):
                self.voice = "fr-FR"
            elif self.lang.startswith("it"):
                self.voice = "it-IT"
            elif self.lang.startswith("en"):
                self.voice = "en-US"
                if "gb" in self.lang.lower() or "uk" in self.lang.lower():
                    self.voice = "en-GB"

    def get_tts(self, sentence, wav_file):
        subprocess.call(
            ['pico2wave', '-l', self.voice, "-w", wav_file, sentence])

        return wav_file, None


class PicoTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PicoTTSValidator, self).__init__(tts)

    def validate_lang(self):
        voices = ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT']
        lang = self.tts.lang.split("-")[0].lower().strip()
        supported = [v.split("-")[0].lower().strip() for v in voices]
        if lang not in supported:
            raise Exception('PicoTTS only supports ' + str(voices))

    def validate_connection(self):
        try:
            subprocess.call(['pico2wave', '--help'])
        except:
            raise Exception(
                'PicoTTS is not installed. Run: '
                '\nsudo apt-get install libttspico0\n'
                'sudo apt-get install  libttspico-utils')

    def get_tts_class(self):
        return PicoTTS


if __name__ == "__main__":
    e = PicoTTS()

    ssml = """Hello world"""
    e.get_tts(ssml, "pico.wav")
