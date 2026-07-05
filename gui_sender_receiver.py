import tkinter as tk
from tkinter import ttk
import random
import socket


class SensorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Julian Álvarez — Barcelona Transfer Sensor')
        self.geometry('780x520')
        self.resizable(False, False)
        self.configure(bg='#07111d')

        self.current_probability = 4.8
        self.history = [4.8] * 30
        self.server_online = False
        self.create_widgets()
        self.update_sensor()

    def create_widgets(self):
        title = tk.Label(self, text='Julian Álvarez Transfer Radar', font=('Segoe UI', 18, 'bold'), fg='#ffcf4d', bg='#07111d')
        title.pack(pady=(14, 8))

        subtitle = tk.Label(self, text='Live simulation of his chance to join Barcelona (0–15%)', font=('Segoe UI', 11), fg='#9dd8ff', bg='#07111d')
        subtitle.pack(pady=(0, 10))

        card = tk.Frame(self, bg='#10233a', bd=2, relief='ridge')
        card.pack(fill='x', padx=18, pady=8)

        self.prob_var = tk.StringVar(value='4.8%')
        tk.Label(card, text='Current probability', font=('Segoe UI', 12, 'bold'), fg='white', bg='#10233a').grid(row=0, column=0, padx=12, pady=10, sticky='w')
        tk.Label(card, textvariable=self.prob_var, font=('Segoe UI', 20, 'bold'), fg='#00f5ff', bg='#10233a').grid(row=0, column=1, padx=12, pady=10, sticky='w')

        self.status_var = tk.StringVar(value='Signal: stable')
        tk.Label(card, textvariable=self.status_var, font=('Segoe UI', 10), fg='#d1fae5', bg='#10233a').grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 10), sticky='w')

        self.canvas = tk.Canvas(self, width=740, height=260, bg='#08111c', highlightthickness=0)
        self.canvas.pack(padx=16, pady=8)

        self.log = tk.Text(self, height=7, width=85, bg='#0d1724', fg='#d1fae5', insertbackground='white')
        self.log.pack(padx=16, pady=(4, 12))
        self.log.insert('end', '⚡ Real-time sensor started...\n')

    def update_sensor(self):
        self.server_online = self.check_server()
        if self.server_online:
            drift = random.uniform(-0.4, 0.4)
            if random.random() < 0.15:
                drift += random.choice([-1.0, 1.0])
            self.current_probability = max(0.0, min(15.0, self.current_probability + drift))
            self.history.append(self.current_probability)
            if len(self.history) > 40:
                self.history.pop(0)

            if self.current_probability >= 12.0:
                status = 'Signal: strong Barcelona interest'
            elif self.current_probability >= 8.0:
                status = 'Signal: growing momentum'
            elif self.current_probability >= 4.0:
                status = 'Signal: moderate chance'
            else:
                status = 'Signal: quiet market'

            self.prob_var.set(f'{self.current_probability:.1f}%')
            self.status_var.set(status)
            self.draw_chart()
            self.log.insert('end', f'[{len(self.history)}] Chance updated: {self.current_probability:.1f}%\n')
        else:
            self.prob_var.set('offline')
            self.status_var.set('Signal: server offline — no live data')
            self.draw_chart(offline=True)
            self.log.insert('end', '[offline] Server is not available.\n')

        self.log.see('end')
        self.after(1000, self.update_sensor)

    def check_server(self):
        try:
            with socket.create_connection(('127.0.0.1', 9999), timeout=0.3):
                return True
        except OSError:
            return False

    def draw_chart(self, offline=False):
        self.canvas.delete('all')
        w, h = 740, 260
        margin_left, margin_right = 40, 20
        margin_top, margin_bottom = 20, 30
        plot_w = w - margin_left - margin_right
        plot_h = h - margin_top - margin_bottom

        self.canvas.create_line(margin_left, margin_top, margin_left, h - margin_bottom, fill='#3b82f6', width=2)
        self.canvas.create_line(margin_left, h - margin_bottom, w - margin_right, h - margin_bottom, fill='#3b82f6', width=2)

        self.canvas.create_text(margin_left - 8, margin_top, text='15%', anchor='e', fill='#ffcf4d')
        self.canvas.create_text(margin_left - 8, h - margin_bottom, text='0%', anchor='e', fill='#ffcf4d')
        self.canvas.create_text(w // 2, h - 5, text='time', fill='#9dd8ff')

        if offline:
            self.canvas.create_text(w // 2, h // 2, text='Offline mode', fill='#ff4fd8', font=('Segoe UI', 16, 'bold'))
            return

        if len(self.history) < 2:
            return

        points = []
        for i, value in enumerate(self.history):
            x = margin_left + (i / max(1, len(self.history) - 1)) * plot_w
            y = margin_top + (15.0 - value) / 15.0 * plot_h
            points.append((x, y))

        for idx in range(1, len(points)):
            x1, y1 = points[idx - 1]
            x2, y2 = points[idx]
            self.canvas.create_line(x1, y1, x2, y2, fill='#00f5ff', width=2)

        last_x, last_y = points[-1]
        self.canvas.create_oval(last_x - 4, last_y - 4, last_x + 4, last_y + 4, fill='#ff4fd8', outline='')


if __name__ == '__main__':
    app = SensorApp()
    app.mainloop()
