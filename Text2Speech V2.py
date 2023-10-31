import pyaudio
import wave
import os

class speech_dictionary:

        def __init__(self, filename):
                reader = open(filename, "r")

                self.dictionary = {}
                self.local_path = os.path.dirname(os.path.realpath(__file__))
                self.audio_path = os.path.join(self.local_path, "samples")
                self.output_file = os.path.join(self.local_path, "output.wav")
                for line in reader:
                        line = line.strip()
                        line = line.split()
                        self.dictionary[line[0]] = line[1:]

                print(">> Dictionary loaded", len(self.dictionary), "entires")
                print(">> Local path:", self.local_path)
                print(">> Audio path:", self.audio_path)

        def get_phonemes(self, word):
                if word in self.dictionary:
                        return self.dictionary[word]
                else:
                        print(word, "not found in dictionary")
                        return None

        def remove_stress(self, phoneme):
                if phoneme[-1].isdigit():
                        return phoneme[:-1]
                else:
                        return phoneme

        def sentence_to_phonemes(self, sentence, stress = False):
                sentence = sentence.split()
                phonemes = []
                for word in sentence:
                        word_phonemes = self.get_phonemes(word.upper())
                        if word_phonemes:
                                phonemes += word_phonemes
                return phonemes

        def get_audio_filename(self, phoneme):
                phoneme = self.remove_stress(phoneme)
                return os.path.join(self.audio_path, phoneme + ".wav")

        def save_phonemes_to_wav(self, phonemes):    
                infiles = [self.get_audio_filename(phoneme) for phoneme in phonemes]
                outfile = self.output_file

                data= []
                for infile in infiles:
                        w = wave.open(infile, 'rb')
                        data.append( [w.getparams(), w.readframes(w.getnframes())] )
                        w.close()
                
                output = wave.open(outfile, 'wb')
                output.setparams(data[0][0])
                for i in range(len(data)):
                        output.writeframes(data[i][1])
                output.close()
                
        
        def save_and_play_phonemes(self, phonemes): 
                self.save_phonemes_to_wav(phonemes)
                # Open the WAV file
                wave_file = wave.open(self.output_file, 'rb')

                # Create a PyAudio object
                audio = pyaudio.PyAudio()

                # Open a stream
                stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                                channels=wave_file.getnchannels(),
                                rate=wave_file.getframerate(),
                                output=True)

                # Read and play audio
                chunk = 1024
                data = wave_file.readframes(chunk)
                while data:
                        stream.write(data)
                        data = wave_file.readframes(chunk)

                # Cleanup
                wave_file.close()
                stream.stop_stream()
                stream.close()
                audio.terminate()

sd = speech_dictionary("cmudict-0.7b.txt")
while True:
    sentence = input("Enter a sentence: ")

    if sentence == "exit":
        break

    phonemes = sd.sentence_to_phonemes(sentence)
    sd.save_and_play_phonemes(phonemes)