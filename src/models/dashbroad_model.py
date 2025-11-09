# dashbroad_page.py (Ví dụ cho cấu trúc Multi-Frame)
import tkinter as tk
from tkinter import ttk


class DashbroadPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Chia Frame thành 2 cột: Sidebar (1) và Content (2)
        self.columnconfigure(0, weight=0)  # Cột 0: Sidebar (cố định)
        self.columnconfigure(1, weight=1)  # Cột 1: Nội dung (mở rộng)

        # 1. Thêm thanh điều hướng (Sidebar) vào cột 0
        self.create_navigation_sidebar()

        # 2. Thêm nội dung chính vào cột 1
        content_frame = ttk.Frame(self, padding="20")
        content_frame.grid(row=0, column=1, sticky="nsew")

        # --- Bắt đầu Nội dung Dashboard ---
        ttk.Label(content_frame, text="📊 DASHBOARD TỔNG QUAN",
                  font=("Arial", 20, "bold")).pack(pady=20, anchor="w")

        # ... (Thêm các thành phần Dashboard khác vào content_frame) ...

    def create_navigation_sidebar(self):
        sidebar = ttk.Frame(self, width=150, relief='groove')
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ttk.Label(sidebar, text="MENU",
                  font=("Arial", 14, "bold")).pack(pady=(20, 10), padx=10, fill="x")

        pages = [
            ("Dashboard", "DashbroadPage"),
            ("Lái Xe", "DriverPage"),
            ("Phương Tiện", "VehiclePage")
        ]

        for text, page_name in pages:
            btn = ttk.Button(sidebar, text=text,
                             command=lambda p=page_name: self.controller.show_frame(p))
            btn.pack(pady=5, padx=10, fill="x")