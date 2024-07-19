'''
Name: dicto.py
Author: moiSentineL and Claude.ai
Repo: https://github.com/moiSentineL/dicto
Version: 1.0
'''

from gtts import gTTS
import pygame
import io
import time
import re
import os
import sys
import argparse

class TextToSpeechDictator:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.punctuation_mapping = {
            '.': 'full stop',
            ',': 'comma',
            '?': 'question mark',
            '!': 'exclamation mark',
            ';': 'semicolon',
            ':': 'colon',
        }

    def configure(self, lang, tld, stop_after_fullstop, word_group, base_pause, extra_pause_frequency, extra_pause_duration, length_multiplier):
        self.lang = lang
        self.tld = tld
        self.stop_after_fullstop = stop_after_fullstop
        self.word_group = word_group
        self.base_pause = base_pause
        self.extra_pause_frequency = extra_pause_frequency
        self.extra_pause_duration = extra_pause_duration
        self.length_multiplier = length_multiplier

    def speak_group(self, group, is_last_group):
        tts = gTTS(text=group, lang=self.lang, tld=self.tld, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        if not is_last_group:
            # Calculate pause duration based on word length
            total_length = sum(len(word) for word in group.split())
            pause_duration = self.base_pause + (total_length * self.length_multiplier)
            time.sleep(pause_duration)

    def display_paragraph(self, paragraph, current_group):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
        words = paragraph.split()
        highlighted = []
        current_group_words = current_group.split()
        i = 0
        while i < len(words):
            if i + len(current_group_words) <= len(words) and words[i:i+len(current_group_words)] == current_group_words:
                highlighted.append(f"\033[91m{' '.join(words[i:i+len(current_group_words)])}\033[0m")
                i += len(current_group_words)
            else:
                highlighted.append(words[i])
                i += 1
        print(" ".join(highlighted))

    def dictate(self, text):
        paragraphs = text.split('\n')

        for paragraph in paragraphs:
            words = paragraph.split()
            i = 0
            while i < len(words):
                group = []
                display_group = []
                for _ in range(self.word_group):
                    if i < len(words):
                        word = words[i]
                        display_group.append(word)
                        # Check if the word ends with a punctuation
                        if word[-1] in self.punctuation_mapping:
                            group.append(word[:-1])
                            group.append(self.punctuation_mapping[word[-1]])
                        else:
                            group.append(word)
                        i += 1
                        if word[-1] in self.punctuation_mapping:
                            break

                is_last_group = i >= len(words)
                
                # Display paragraph with current word group highlighted
                self.display_paragraph(paragraph, ' '.join(display_group))
                
                # Speak the group
                self.speak_group(' '.join(group), is_last_group)

                if not is_last_group:
                    if (i // self.word_group) % self.extra_pause_frequency == 0:
                        time.sleep(self.extra_pause_duration)
                
                # If the last word ended with a period, pause
                if group[-1] == 'full stop':
                    time.sleep(self.stop_after_fullstop)

def get_user_input():
    # file = os.path.abspath(str(sys.argv[0]))
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="echo the string you use here")
    args = parser.parse_args()

    file = os.path.abspath(args.file)

    t = open(args.file, "r")
    text = t.read()
    lang = "en"
    tld = "com.ng"
    stop_after_fullstop = 1
    word_group = 2
    base_pause = 0.5
    extra_pause_frequency = 2
    extra_pause_duration = 1
    length_multiplier = 0.1
    return text, lang, tld, stop_after_fullstop, word_group, base_pause, extra_pause_frequency, extra_pause_duration, length_multiplier

if __name__ == "__main__":
    dictator = TextToSpeechDictator()

    try:
        text, lang, tld, stop_after_fullstop, word_group, base_pause, extra_pause_frequency, extra_pause_duration, length_multiplier = get_user_input()
        dictator.configure(lang, tld, stop_after_fullstop, word_group, base_pause, extra_pause_frequency, extra_pause_duration, length_multiplier)
        dictator.dictate(text)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()