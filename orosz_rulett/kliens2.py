import socket
import tkinter as tk
import os
import subprocess
from tkinter import messagebox

# Szerver kapcsolódás
SERVER_IP = "127.0.0.1"  # Szerver IP-je
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# Videó lejátszása
def play_video(video_path):
    if os.path.exists(video_path):
        process = subprocess.Popen(video_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        process.terminate()

# Hang lejátszása
def play_sound(sound_path):
    if os.path.exists(sound_path):
        subprocess.Popen(["start", "/min", sound_path], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Játék kezdése
def start_game():
    client.send("FIRE".encode())  # Küldjük a szervernek, hogy lőni akarunk
    result = client.recv(1024).decode()

    if result == "DEAD":
        play_video("Project_01-21_4K.mp4")
        play_sound("gunshot.mp3")
        messagebox.showinfo("Játék vége", "Meghaltál! Próbáld újra!")
    elif result == "SAFE":
        play_video("második_4K.mp4")
        play_sound("click.mp3")
        messagebox.showinfo("Szerencséd volt", "Túlélted!")
    elif result == "NOT_YOUR_TURN":
        messagebox.showwarning("Nem te jössz!", "Várd meg, amíg a másik játékos lő!")

# Tkinter GUI
root = tk.Tk()
root.title("Orosz Rulett - Multiplayer")
root.geometry("300x200")

start_button = tk.Button(root, text="Lövés", command=start_game, font=("Arial", 14))
start_button.pack(pady=40)

root.mainloop()
