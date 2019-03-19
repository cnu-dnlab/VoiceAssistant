import speech_recognition as sr

class TestChecker():
    def __init__(self, language, audio_file=""):
        self.record = sr.Recognizer()
        self.language = language # "en-US" or "ko-KR"
        self.audio_file = audio_file
        self.have_wav_file = False
        if len(audio_file) > 0: 
            self.have_wav_file = True
    
    def _audio_from_MIC(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.record.listen(source)
            return audio
    
    def _mic_to_text(self):
        audio = self._audio_from_MIC()
        result = ""
        while True:
            try:
                result += self.record.recognize_google(audio, language=self.language)
            except sr.UnkownValueError:
                break
            except sr.RequestError as e:
                break
        return result
    
    def _wav_to_text(self):
        wav_file = sr.AudioFile(self.audio_file)
        gap = 5
        result = ""
        with wav_file as source:
            for _ in range(0, 60, gap):
                audio = self.record.record(source, duration=gap)
                try: result += self.record.recognize_google(audio, language=self.language)+" "
                except sr.UnknownValueError: break
                except sr.RequestError: break
        return result
    
    def get_result(self):
        result = ""
        if self.have_wav_file:
            result = self._wav_to_text()
            text_file_name = self.audio_file.split('.')[0]+'.txt'
        else:
            result = self._mic_to_text()
            text_file_name = "./mic_result.txt"
        print(result)
        with open(text_file_name, "w") as result_file:
            result_file.write(result)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--language',
                        help='audio language',
                        type=str,
                        required=True)

    parser.add_argument('-p', '--file-path',
                        help='wav file location',
                        type=str,
                        default='')

    ARGS = parser.parse_args()

    test_checker = TestChecker(ARGS.language, ARGS.file_path)
    test_checker.get_result()
    
