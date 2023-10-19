import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter as ctk
from mutagen.mp3 import MP3
import threading
import pygame
import time
import os
from timnhac import play_music_by_name,stop_music
import speech_recognition as sr
import sys
# Khởi tạo mixer của pygame
pygame.mixer.init()
import sys

# Lưu vị trí hiện tại của âm nhạc
current_position = 0
paused = False
selected_folder_path = ""  # Lưu đường dẫn thư mục được chọn


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Nghe...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="vi")
        print(f"Bạn đã nói: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Không thể nhận diện giọng nói.")
        return ""
    except sr.RequestError as e:
        print(f"Lỗi kết nối đến Google API: {e}")
        return ""


def cap_nhat_tien_trinh():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos() / 1000
            pbar["value"] = current_position

            # Kiểm tra xem bài hát hiện tại đã đạt đến thời lượng tối đa chưa
            if current_position >= pbar["maximum"]:
                dung_nhac()  # Dừng phát nhạc
                pbar["value"] = 0  # Đặt lại thanh tiến trình

            window.update()
        time.sleep(0.1)


# Tạo một luồng để cập nhật thanh tiến trình
pt = threading.Thread(target=cap_nhat_tien_trinh)
pt.daemon = True
pt.start()

exit_flag = False
music_thread = None

# Tạo biến cờ để kiểm soát tạm dừng
pause_flag = threading.Event()


def tim_Nhac():
    global pause_flag
    while not pause_flag.is_set():
        song_name = recognize_speech()
        play_music_by_name(song_name)

def run_tim_Nhac_thread():
    
    music_thread = threading.Thread(target=tim_Nhac)
    music_thread.start()

def tat_nhac():
    window.destroy()
    import index
    


def chon_thu_muc_nhac():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                # Chèn chỉ tên tệp, không phải đường dẫn đầy đủ
                lbox.insert(tk.END, filename)


def bai_truoc():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index > 0:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index - 1)
            chay_bai_hat_da_chon()


def bai_tiep_theo():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size() - 1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index + 1)
            chay_bai_hat_da_chon()


def phat_nhac():
    global paused
    if paused:
        # Nếu nhạc đang tạm dừng, tiếp tục phát
        pygame.mixer.music.unpause()
        paused = False

    else:
        # Nếu nhạc không tạm dừng, phát bài hát đã chọn
        chay_bai_hat_da_chon()


def chay_bai_hat_da_chon():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        # Thêm đường dẫn đầy đủ
        full_path = os.path.join(selected_folder_path, selected_song)
        pygame.mixer.music.load(full_path)  # Tải bài hát đã chọn
        # Phát bài hát từ vị trí hiện tại
        pygame.mixer.music.play(start=current_position)
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        # Đặt giá trị tối đa của thanh tiến trình là thời lượng bài hát
        pbar["maximum"] = song_duration


def tam_dung_nhac():
    global paused
    # Tạm dừng nhạc đang phát
    pygame.mixer.music.pause()
    paused = True


def dung_nhac():
    global paused
    # Dừng nhạc đang phát và đặt lại thanh tiến trình
    pygame.mixer.music.stop()
    paused = False


# Tạo cửa sổ chính
window = tk.Tk()
window.title("Ứng dụng Nghe Nhạc")
window.geometry("600x500")

# Tạo nhãn cho tiêu đề trình phát nhạc
l_music_player = tk.Label(window, text="Genius Music",
                          font=("TkDefaultFont", 30, "bold"))
l_music_player.pack(pady=10)


# Tạo nút để chọn thư mục nhạc
btn_select_folder = ctk.CTkButton(window, text="Select Folder",
                                  command=chon_thu_muc_nhac,
                                  font=("TkDefaultFont", 18),
                                  )

btn_select_folder.place(x=450, y=40)
btn_select_folder1 = ctk.CTkButton(window, text="Tìm nhạc",
                                   command=run_tim_Nhac_thread,
                                   font=("TkDefaultFont", 18)
                                   )

# btn_select_folder1.pack(padx=100,side=tk.LEFT)
btn_select_folder1.place(x=5, y=40)

# Tạo danh sách để hiển thị các bài hát có sẵn
lbox = tk.Listbox(window, width=50, font=("TkDefaultFont", 16))
lbox.pack(pady=20)

# Tạo khung để chứa các nút điều khiển
btn_frame = tk.Frame(window)
btn_frame.pack(pady=20)

# Tạo nút để chuyển đến bài hát trước
btn_previous = ctk.CTkButton(btn_frame, text="<", command=bai_truoc,
                             width=50, font=("TkDefaultFont", 18))
btn_previous.pack(side=tk.LEFT, padx=5)

# Tạo nút để phát nhạc
btn_play = ctk.CTkButton(btn_frame, text="Play", command=phat_nhac, width=50,
                         font=("TkDefaultFont", 18))
btn_play.pack(side=tk.LEFT, padx=5)

# Tạo nút để tạm dừng nhạc
btn_pause = ctk.CTkButton(btn_frame, text="Pause", command=tam_dung_nhac, width=50,
                          font=("TkDefaultFont", 18))
btn_pause.pack(side=tk.LEFT, padx=5)

# Tạo nút để chuyển đến bài hát tiếp theo
btn_next = ctk.CTkButton(btn_frame, text=">", command=bai_tiep_theo, width=50,
                         font=("TkDefaultFont", 18))
btn_next.pack(side=tk.LEFT, padx=5)


btn_next = ctk.CTkButton(window, text="tắt nhạc", command=tat_nhac, width=50,
                         font=("TkDefaultFont", 18))
btn_next.pack(side=tk.LEFT, padx=5)

# Tạo thanh tiến trình để chỉ ra tiến trình của bài hát hiện tại
pbar = Progressbar(window, length=300, mode="determinate")
pbar.pack(pady=10)

window.mainloop()
