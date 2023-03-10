import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
from threading import Thread

class DownloadApp:
    def __init__(self, master):
        self.master = master
        master.title("PyDown")
        master.geometry("400x200")
        master.resizable(width=False, height=False)
        self.url_label = tk.Label(master, text="Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.pack()
        self.save_label = tk.Label(master, text="Save Path:")
        self.save_label.pack()
        self.save_entry = tk.Entry(master, width=50)
        self.save_entry.pack()
        self.download_button = tk.Button(master, text="Download", command=self.download_video)
        self.download_button.pack()
        self.progress = tk.DoubleVar()
        self.progressbar = tk.ttk.Progressbar(master, orient="horizontal", mode="determinate", variable=self.progress)
        self.progressbar.pack(fill="x")
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.save_entry.delete(0, tk.END)
        self.save_entry.insert(0, folder_selected)
    
    def download_video(self):
        url = self.url_entry.get()
        save_path = self.save_entry.get()
        
        if not url or not save_path:
            messagebox.showwarning("Warning", "Please provide a valid URL and save path!")
            return
        
        try:
            video = YouTube(url, on_progress_callback=self.progress_hook)
        except Exception as e:
            messagebox.showerror("Error", f"Could not access video at {url}\n\nError: {e}")
            return
        
        video_title = video.title
        messagebox.showinfo("Info", f"Starting download of '{video_title}'")
        t = Thread(target=self.download_thread, args=(video, save_path))
        t.start()
        
    def download_thread(self, video, save_path):
        try:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(save_path)
            messagebox.showinfo("Info", f"Download of '{video.title}' complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not download video\n\nError: {e}")
        
    def progress_hook(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        
        progress_percent = bytes_downloaded / total_size * 100.0
        self.progress.set(progress_percent)

root = tk.Tk()
app = DownloadApp(root)
root.mainloop()
