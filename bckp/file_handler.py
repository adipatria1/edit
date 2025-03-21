from tkinter import filedialog

class FileHandler:
    def __init__(self):
        pass
        
    def browse_video(self):
        return filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mkv")]
        )
        
    def browse_audio(self):
        return filedialog.askopenfilename(
            filetypes=[("Audio files", "*.mp3 *.wav")]
        )
