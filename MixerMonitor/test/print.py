import tkinter as tk
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
import time
import subprocess

def open_print_wizard(image_path):
    # 시스템 기본 이미지 뷰어 및 인쇄 마법사 열기
    subprocess.run(["start", "mspaint", "/pt", image_path], shell=True)

def capture_tkinter_window(window_title):
    tkinter_window = gw.getWindowsWithTitle(window_title)
    
    if len(tkinter_window) == 0:
        print(f"{window_title} 창을 찾을 수 없습니다.")
        return

    window_x, window_y, window_width, window_height = tkinter_window[0].left, tkinter_window[0].top, tkinter_window[0].width, tkinter_window[0].height

    # pyautogui.moveTo(window_x, window_y)
    time.sleep(0.5)

    screenshot = ImageGrab.grab(bbox=(window_x+10, window_y+3, window_x + window_width -10, window_y + window_height -10))
    screenshot.save("captured_tkinter_window.png")
    print("Tkinter 창 캡쳐가 완료되었습니다.")
    open_print_wizard("captured_tkinter_window.png")

def on_capture_button_click():
    capture_tkinter_window("Tkinter Window")

# Tkinter 창 생성
root = tk.Tk()
root.title("Tkinter Window")

# 버튼 생성 및 이벤트 핸들러 연결
capture_button = tk.Button(root, text="창 캡쳐", command=on_capture_button_click)
capture_button.pack(pady=10)

# Tkinter 창 표시
root.mainloop()

