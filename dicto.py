from gtts import gTTS
import pygame
import io
import time
import re
import os
import sys
import base64
import json
import streamlit as st

pygame.init()  # outside class?
pygame.mixer.init()


class dicto:
    def __init__(self):
        with open("punctuation.json", "r") as punc:
            self.punctuation_mapping = json.load(punc)

        with st.sidebar:
            st.header("Configuration")
            self.lang = st.selectbox("Select language", ("en", "fr", "hi"), key="lang")
            self.tld = st.selectbox("Accent", ("co.uk", "com.ng", "com.au"), key="tld")
            self.stop_after_fullstop = st.slider(
                "Pause after fullstop (s)", 0.0, 5.0, 1.5
            )
            self.word_group = st.slider("How many words at once?", 0, 5, 2)
            self.base_pause = st.slider("Minimum pause (s)", 0.0, 3.0, 0.5)
            # self.extra_pause_frequency = 2
            # self.extra_pause_duration = 1.2
            self.length_multiplier = st.slider("Length Multiplier", 0.0, 1.0, 0.135)

    def speak_group(self, group, is_last_group):
        fp = io.BytesIO()
        tts = gTTS(text=group, lang=self.lang, tld=self.tld, slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)

        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if not is_last_group:
            time.sleep(
                self.base_pause
                + ((sum(len(word) for word in group.split())) * self.length_multiplier)
            )

    def display_paragraph(self, paragraph, current_group):

        highlighted = []
        current_group_words = current_group.split()

        i = 0
        while i < len(words := paragraph.split()):
            if (
                to_be_h := words[i : i + len(current_group_words)]
            ) == current_group_words:  # i + len(current_group_words) <= len(words) and
                highlighted.append(f":red[{' '.join(to_be_h)}]")
                i += len(current_group_words)
            else:
                highlighted.append(words[i])
                i += 1
        return " ".join(highlighted)

    def dictate(self, text):
        for paragraph in (paragraphs := text.split("\n")):
            i = 0
            while i < len(words := paragraph.split()):
                group = []
                display_group = []

                for _ in range(self.word_group):
                    if i < len(words):
                        display_group.append(word := words[i])

                        # Check if the word ends with a punctuation
                        if word[0] in self.punctuation_mapping:
                            group.append(self.punctuation_mapping[word[0]])
                            group.append(word)
                        else:
                            group.append(word)
                        i += 1

                        if word[0] in self.punctuation_mapping:
                            break

                        if word[-1] in self.punctuation_mapping:
                            group.append(self.punctuation_mapping[word[-1]])
                            break

                highlighted_text = self.display_paragraph(
                    paragraph, " ".join(display_group)
                )
                bruh = st.empty()
                bruh.subheader(highlighted_text)

                # Speak the group
                self.speak_group(" ".join(group), (is_last_group := i >= len(words)))

                # if not is_last_group:
                #     if (i // self.word_group) % self.extra_pause_frequency == 0:
                #         time.sleep(self.extra_pause_duration)

                if group[-1] == "full stop":
                    time.sleep(self.stop_after_fullstop)

                bruh.empty()


if __name__ == "__main__":
    st.title("dicto")
    with st.expander("Instructions", expanded=True):
        st.write(open("INSTRUCTIONS.md", "r").read())

    area = st.text_area(
        "Text to dictate",
        "It was the best of times, it was the worst of times, it was the age of "
        "wisdom, it was the age of foolishness, it was the epoch of belief, it "
        "was the epoch of incredulity, it was the season of Light, it was the "
        "season of Darkness, it was the spring of hope, it was the winter of "
        "despair.",
        key="textarea",
    )
    with st.expander("Your File", expanded=True):
        uploaded = st.empty().file_uploader(
            "Upload a file lol", type="txt", label_visibility="collapsed", key="upload"
        )

    try:
        dictator = dicto()
        text = (
            io.StringIO(uploaded.getvalue().decode("utf-8")).read()
            if uploaded is not None
            else area
        )

        with st.container():
            dictator.dictate(text) if st.button("Dictate!") else st.write("")
    except Exception as e:
        st.divider()
        st.exception(e)
    finally:
        pygame.quit()
