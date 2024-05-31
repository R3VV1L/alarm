import tkinter as tk
from tkinter import filedialog
import pygame
from datetime import datetime, timedelta
import winsound
from tkinter import ttk
from PIL import Image, ImageTk


class Alarm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Будильник")
        self.geometry("350x350")
        self.configure(bg="#C0C0C0")  # Светло-серый фон

        # Создание стиля для закругленных краев
        self.style = ttk.Style()
        self.style.configure(
            "MyRounded.TButton",
            borderwidth=0,
            relief="flat",
            background="#FFA500",  # Оранжевый цвет для кнопок
            foreground="#333333",  # Темно-серый цвет текста
            font=("Consolas", 12),
        )
        self.style.map("MyRounded.TButton", background=[("active", "#6A4C9C")])

        # Создание виджетов
        self.label = tk.Label(
            self,
            text="Установите время будильника:",
            font=("Consolas", 14),
            bg="#C0C0C0",
            fg="#333333",
        )
        self.label.pack(pady=10)

        self.time_entry = tk.Entry(
            self, font=("Consolas", 12), relief="flat", bg="#FFA500", fg="#333333"
        )
        self.time_entry.pack(pady=10)

        self.set_button = ttk.Button(
            self, text="Установить", command=self.set_alarm, style="MyRounded.TButton"
        )
        self.set_button.pack(pady=10)

        self.stop_button = ttk.Button(
            self,
            text="Остановить",
            command=self.stop_alarm,
            state="disabled",
            style="MyRounded.TButton",
        )
        self.stop_button.pack(pady=10)

        self.canvas = tk.Canvas(
            self, bg="#C0C0C0", width=350, height=50, bd=0, highlightthickness=0
        )
        self.canvas.pack(side="bottom", pady=25)

        # Создание полупрозрачной надписи с помощью Pillow
        text = "by R3vv1l"
        font = ("Consolas", 10)
        image = Image.new("RGBA", (350, 50), (192, 192, 192, 128))  # Полупрозрачный фон
        draw = ImageTk.PhotoImage(image)
        self.footer_text = self.canvas.create_image(175, 25, image=draw)
        self.canvas.create_text(175, 25, text=text, font=font, fill="#333333")

        self.alarm_time = None
        self.is_ringing = False
        self.music_file = "cruel-angels-thesis meloboom.mp3"

    def set_alarm(self):
        alarm_time = self.time_entry.get()
        try:
            self.alarm_time = datetime.strptime(alarm_time, "%H:%M").time()
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, f"{self.alarm_time.strftime('%H:%M')}")
            self.after(1000, self.check_alarm)
            self.set_button.config(state="disabled")
            self.stop_button.config(state="normal")
        except ValueError:
            self.label.config(text="Неверный формат времени.\n Используйте HH:MM.")

    def check_alarm(self):
        if datetime.now().time() >= self.alarm_time and not self.is_ringing:
            self.ring_alarm()
        self.after(1000, self.check_alarm)

    def ring_alarm(self):
        self.is_ringing = True
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()
        self.label.config(text="Будильник звонит!")

    def stop_alarm(self):
        if self.is_ringing:
            pygame.mixer.music.stop()
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.label.config(text="Будильник остановлен.")
            self.is_ringing = False
        self.set_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.alarm_time = None


if __name__ == "__main__":
    alarm = Alarm()
    alarm.mainloop()
