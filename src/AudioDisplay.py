import tkinter as tk
import wave, pyaudio
import os
from tkinter import messagebox


class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0,
                            state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = []

    # Function to add buttons for music files
    def add_music_buttons(self, i):
        bg = "pale green"
        box = tk.Button(text='mu' + str(i + 1), bd=1, relief="sunken", highlightbackground=bg,
                        width=14, height=7, command=lambda i=i: self.music_callBack(i))
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")

    # Callback function for music file
    def music_callBack(self, i):
        path = '../audio_data/music/mu' + str(i + 1) + '.wav'
        print('path is ' + path)
        wf = wave.open(
            path, 'rb')
        p = pyaudio.PyAudio()
        chunk = 1024
        stream = p.open(format=
                        p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()

    # Function to add buttons for speech files
    def add_speech_buttons(self, i):
        bg = "plum1"
        box = tk.Button(text='sp' + str(i + 1), bd=1, relief="sunken", highlightbackground=bg,
                        width=14, height=7, command=lambda i=i: self.speech_callBack(i))
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")

    # Callback function for speech file
    def speech_callBack(self, i):
        path = '../audio_data/speech/sp' + str(i + 1) + '.wav'
        print('path is ' + path)
        wf = wave.open(
            path, 'rb')
        p = pyaudio.PyAudio()
        chunk = 1024
        stream = p.open(format=
                        p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()


class Display(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1400x800')

        self.dg = DynamicGrid(self.root, width=500, height=200)
        w = tk.Label(self.root, text="Click on any of the below audio files to play! Pale Green - Music ,Plum - Speech",
                     width=15, height=4, font='Helvetica 18 bold')
        w.pack(side="top", fill="both")

        for i in range(20):
            self.dg.add_music_buttons(i)
        self.dg.pack(side="top", fill="both", expand=True)

        for i in range(20):
            self.dg.add_speech_buttons(i)
        self.dg.pack(side="top", fill="both", expand=True)

        b = tk.Button(text='Classify', width=20, height=5, highlightbackground='cornflower blue', command=self.classify)
        b.pack(side="bottom", expand=True)

    def classify(self):
        print('Test message')
        os.system('python3 AudioRead.py')
        messagebox.showinfo(title='Classification Report',
                            message='For 3 Features: \n Confusion Matrix : \n545 514 \n481 576 \n Accuracy : 0.5297 \n Precision:0.53 \n Recall is 0.54 \n\n For 34 features: \n Confusion matrix : \n709 350 \n240 817 \n Accuracy :0.7211 \n Precision : 0.72 \n Recall:0.77')

    def start(self):
        self.root.mainloop()


Display().start()
