#!/usr/bin/env python3

import os
import shutil
import sys
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, ttk


def process_files(src_dir, sort_option, nest, progress_bar, status_label, open_button):
    dest_dir = src_dir + "_sorted"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    files_to_process = []
    for foldername, _, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mov', '.mp4', '.avi')):
                filepath = os.path.join(foldername, filename)
                files_to_process.append(filepath)

    progress_bar["maximum"] = len(files_to_process)
    progress_bar['value'] = 0
    root.update_idletasks()  # Force the UI to update

    for filepath in files_to_process:
        foldername = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        timestamp = os.path.getmtime(filepath)
        dt_object = datetime.fromtimestamp(timestamp)
        city = foldername.split('/')[-1]

        if sort_option == "day":
            time_folder = dt_object.strftime('%Y-%m-%d') if not nest else os.path.join(dt_object.strftime('%Y'), dt_object.strftime('%m'), dt_object.strftime('%d'))
        elif sort_option == "month":
            time_folder = dt_object.strftime('%Y-%m') if not nest else os.path.join(dt_object.strftime('%Y'), dt_object.strftime('%m'))
        else:
            time_folder = dt_object.strftime('%Y')

        dest_folder = os.path.join(dest_dir, city, time_folder)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.copy2(filepath, os.path.join(dest_folder, filename))
        progress_bar['value'] += 1
        root.update_idletasks()

    status_label.config(text=f"Sorting Done. Sorted Directory: {dest_dir}")
    open_button.config(command=lambda: open_in_file_explorer(dest_dir), state=tk.NORMAL)

def start_sorting(src_dir, sort_option, nest, progress_bar, status_label, open_button):
    if src_dir:
        progress_bar.pack(pady=10)
        status_label.pack(pady=10)
        open_button.pack(pady=10)
        root.after(100, lambda: process_files(src_dir, sort_option, nest, progress_bar, status_label, open_button))

def open_in_file_explorer(path):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":  # macOS
        os.system(f"open {path}")
    else:  # Linux
        os.system(f"xdg-open {path}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Select Folder to Organize")
    root.geometry("600x400")

    selected_dir = tk.StringVar(root)
    sort_option = tk.StringVar(root)
    nest_option = tk.BooleanVar(root)

    frame_options = tk.Frame(root)
    frame_options.pack(pady=10)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    tk.Label(frame_options, text="Sort by:").pack(side=tk.LEFT)
    sort_options = {"Day": "day", "Month": "month", "Year": "year"}
    for text, mode in sort_options.items():
        tk.Radiobutton(frame_options, text=text, variable=sort_option, value=mode).pack(side=tk.LEFT)

    tk.Checkbutton(frame_options, text="Nest Directories", variable=nest_option).pack(side=tk.LEFT)

    select_button = tk.Button(
        frame_buttons,
        text="Select Folder",
        command=lambda: [
            selected_dir.set(filedialog.askdirectory()),
            start_button.pack(side=tk.LEFT, padx=5) if selected_dir.get() else start_button.pack_forget()
        ]
    )
    select_button.pack(side=tk.LEFT, padx=5)

    start_button = tk.Button(
        frame_buttons,
        text="Start Sorting",
        command=lambda: start_sorting(selected_dir.get(), sort_option.get(), nest_option.get(), progress, status_label, open_button)
    )

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    status_label = tk.Label(root, text="")
    open_button = tk.Button(root, text="Open Directory", state=tk.DISABLED)

    root.mainloop()
