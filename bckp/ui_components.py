import tkinter as tk
from tkinter import ttk

class UIComponents:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        
    def create_file_selection(self, row, label_text, path_var, browse_command):
        ttk.Label(self.main_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=path_var, width=50).grid(row=row, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=browse_command).grid(row=row, column=2)
        
    def create_resolution_selection(self, row, resolution_var):
        ttk.Label(self.main_frame, text="Resolution:").grid(row=row, column=0, sticky=tk.W, pady=5)
        resolution_frame = ttk.Frame(self.main_frame)
        resolution_frame.grid(row=row, column=1, sticky=tk.W)
        ttk.Radiobutton(resolution_frame, text="720p", variable=resolution_var, value="720").pack(side=tk.LEFT)
        ttk.Radiobutton(resolution_frame, text="480p", variable=resolution_var, value="480").pack(side=tk.LEFT)
        
    def create_interval_settings(self, row, interval_var, random_var):
        ttk.Label(self.main_frame, text="Interval (seconds):").grid(row=row, column=0, sticky=tk.W, pady=5)
        interval_frame = ttk.Frame(self.main_frame)
        interval_frame.grid(row=row, column=1, sticky=tk.W)
        ttk.Entry(interval_frame, textvariable=interval_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(interval_frame, text="Random Interval (tidak dipakai)", variable=random_var).pack(side=tk.LEFT)
        
    def create_overlap_settings(self, row, overlap_var, random_overlap_var):
        ttk.Label(self.main_frame, text="Scene Duration (seconds):").grid(row=row, column=0, sticky=tk.W, pady=5)
        overlap_frame = ttk.Frame(self.main_frame)
        overlap_frame.grid(row=row, column=1, sticky=tk.W)
        ttk.Entry(overlap_frame, textvariable=overlap_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(overlap_frame, text="Random Scene", variable=random_overlap_var).pack(side=tk.LEFT)
        
    def create_process_button(self, row, command):
        ttk.Button(self.main_frame, text="Process Video", command=command).grid(row=row, column=0, columnspan=3, pady=20)
        
    def create_progress_bar(self, row):
        progress = ttk.Progressbar(self.main_frame, length=300, mode='determinate')
        progress.grid(row=row, column=0, columnspan=3, pady=10)
        return progress
