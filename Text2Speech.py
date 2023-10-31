from playsound import playsound
import os

class speech_dictionary:

    def __init__(self, filename):
        reader = open(filename, "r")

        self.dictionary = {}
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.audio_path = os.path.join(self.local_path, "samples - 1.5x")
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

    def play_phonemes(self, phonemes):
            for phoneme in phonemes:
                    filename = self.get_audio_filename(phoneme)
                    filename = str(filename)
                    filename.replace("//", "\\")
                    playsound(filename)

sd = speech_dictionary("cmudict-0.7b.txt")
while True:
    sentence = input("Enter a sentence: ")

    if sentence == "exit":
        break

    phonemes = sd.sentence_to_phonemes(sentence)
    sd.play_phonemes(phonemes)