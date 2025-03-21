import os
from pyvirtualdisplay import Display
import tkinter as tk
from tkinter import ttk, messagebox
import random
from video_processor import VideoProcessor
from file_handler import FileHandler
from ui_components import UIComponents

# Jika tidak ada DISPLAY, jalankan virtual display
if "DISPLAY" not in os.environ:
    display = Display(visible=0, size=(1024, 768))
    display.start()

class MovieRecapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recap Editor")
        self.root.geometry("800x600")
        
        # Variabel
        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.resolution = tk.StringVar(value="720")
        self.interval = tk.StringVar(value="30")  # default interval 30 detik
        self.overlap = tk.StringVar(value="5")      # default scene duration 5 detik
        self.random_enabled = tk.BooleanVar(value=False)         # tidak digunakan untuk interval pada contoh ini
        self.random_overlap_enabled = tk.BooleanVar(value=True)    # aktifkan random scene
        
        # Inisialisasi komponen
        self.file_handler = FileHandler()
        self.video_processor = VideoProcessor()
        
        # Buat UI
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.ui = UIComponents(main_frame)
        
        self.ui.create_file_selection(0, "Select Video:", self.video_path, self.browse_video)
        self.ui.create_file_selection(1, "Select Audio:", self.audio_path, self.browse_audio)
        self.ui.create_resolution_selection(2, self.resolution)
        self.ui.create_interval_settings(3, self.interval, self.random_enabled)
        self.ui.create_overlap_settings(4, self.overlap, self.random_overlap_enabled)
        self.ui.create_process_button(5, self.process_video)
        self.progress = self.ui.create_progress_bar(6)
        
    def browse_video(self):
        filename = self.file_handler.browse_video()
        if filename:
            self.video_path.set(filename)
            
    def browse_audio(self):
        filename = self.file_handler.browse_audio()
        if filename:
            self.audio_path.set(filename)
            
    def process_video(self):
        if not self.video_path.get() or not self.audio_path.get():
            messagebox.showerror("Error", "Please select both video and audio files")
            return
            
        try:
            resolution = int(self.resolution.get())
            interval_val = int(self.interval.get())
            scene_val = int(self.overlap.get())
            
            for progress in self.video_processor.process_video(
                self.video_path.get(),
                self.audio_path.get(),
                resolution,
                interval_val,
                scene_val,
                self.random_enabled.get(),
                self.random_overlap_enabled.get()
            ):
                self.progress['value'] = progress
                self.root.update_idletasks()
            
            messagebox.showinfo("Success", "Video processing completed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecapEditor(root)
    root.mainloop()
    
    # Jika menggunakan virtual display, hentikan setelah aplikasi ditutup
    if "display" in globals():
        display.stop()
