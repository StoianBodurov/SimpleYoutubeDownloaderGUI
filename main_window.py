from tkinter import *
from tkinter import ttk

from pytube import YouTube


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube Downloader')
        self.root.geometry('600x300')

        frame = ttk.Frame(self.root, padding='20 60', borderwidth=5, relief='solid')
        frame.grid(padx=30, pady=35)

        ttk.Label(frame, text="Add url:", padding='1').grid(column=0, row=0, sticky='w', padx=10)

        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label='Paste', command=self.entry_paste)

        self.url = StringVar()
        self.entry = ttk.Entry(frame, textvariable=self.url)
        self.entry.grid(column=0, row=1, padx=10, ipady=5, ipadx=120)
        self.entry.bind('<Button-3>', self.popup)

        ttk.Button(frame, text='Download', padding='5', command=self.download).grid(column=1, row=1, padx=10)

        self.file_format = StringVar(None, 'audio')
        ttk.Radiobutton(frame,
                        text='Audio',
                        variable=self.file_format,
                        value='audio').grid(column=0, row=2, sticky='W', padx=10)
        ttk.Radiobutton(frame,
                        text='Video',
                        variable=self.file_format,
                        value='video').grid(column=0, row=2, sticky='W', padx=70)

    def download(self):
        yt_url = self.url.get()
        try:
            yt = YouTube(yt_url)
            if self.file_format.get() == 'audio':
                self.download_mp3(yt)
            else:
                self.download_mp4(yt)
        except Exception as ex:
            messagebox.showwarning('showwarning', str(ex))
        finally:
            self.url.set('')

    @staticmethod
    def download_mp4(you_tube):
        you_tube.streams.get_highest_resolution().download()

    @staticmethod
    def download_mp3(you_tube):
        filename = you_tube.title
        you_tube.streams.get_audio_only().download(filename=f'{filename}.mp3')

    def entry_paste(self):
        clipboard = self.root.clipboard_get()
        self.entry.insert('end', clipboard)

    def popup(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

