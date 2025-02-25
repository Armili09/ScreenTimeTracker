import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class StatsFrame(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup statistics UI components"""
        # Today's usage section
        ttk.Label(self, text="Today's Usage", font=('Helvetica', 14, 'bold')).pack(pady=10)
        self.today_usage_frame = ttk.Frame(self)
        self.today_usage_frame.pack(fill='x', padx=10)
        
        # Weekly statistics section
        ttk.Label(self, text="Weekly Statistics", font=('Helvetica', 14, 'bold')).pack(pady=10)
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)
        
    def update_stats(self):
        """Update statistics display"""
        # Clear previous stats
        for widget in self.today_usage_frame.winfo_children():
            widget.destroy()
            
        # Update today's usage
        row = 0
        for app_name in self.data_manager.data["usage"].keys():
            usage_seconds = self.data_manager.get_today_usage(app_name)
            usage_minutes = usage_seconds / 60
            limit = self.data_manager.get_app_limit(app_name)
            
            ttk.Label(self.today_usage_frame, text=app_name).grid(row=row, column=0, pady=2)
            ttk.Label(self.today_usage_frame, 
                     text=f"{usage_minutes:.1f} min / {limit} min").grid(row=row, column=1, pady=2)
            
            # Progress bar
            if limit > 0:
                progress = ttk.Progressbar(self.today_usage_frame, length=200, mode='determinate')
                progress['value'] = min(100, (usage_minutes / limit) * 100)
                progress.grid(row=row, column=2, padx=10, pady=2)
            
            row += 1
            
        # Update weekly chart
        self.ax.clear()
        for app_name in self.data_manager.data["usage"].keys():
            weekly_usage = self.data_manager.get_weekly_usage(app_name)
            dates = list(weekly_usage.keys())
            minutes = [seconds/60 for seconds in weekly_usage.values()]
            self.ax.plot(dates, minutes, label=app_name, marker='o')
            
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Minutes')
        self.ax.legend()
        self.ax.tick_params(axis='x', rotation=45)
        self.fig.tight_layout()
        self.canvas.draw()

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup settings UI components"""
        ttk.Label(self, text="App Time Limits", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # App limit settings
        self.limits_frame = ttk.Frame(self)
        self.limits_frame.pack(fill='x', padx=20)
        
        row = 0
        for app_name in ["Google Chrome", "Firefox", "Microsoft Edge", "Netflix", "YouTube"]:
            ttk.Label(self.limits_frame, text=app_name).grid(row=row, column=0, pady=5)
            
            limit_var = tk.StringVar(value=str(self.data_manager.get_app_limit(app_name)))
            limit_entry = ttk.Entry(self.limits_frame, textvariable=limit_var, width=10)
            limit_entry.grid(row=row, column=1, padx=10)
            
            ttk.Label(self.limits_frame, text="minutes").grid(row=row, column=2)
            
            ttk.Button(self.limits_frame, 
                      text="Save", 
                      command=lambda a=app_name, v=limit_var: self.save_limit(a, v)).grid(row=row, column=3, padx=10)
            
            row += 1
            
    def save_limit(self, app_name, limit_var):
        """Save app time limit"""
        try:
            limit = int(limit_var.get())
            self.data_manager.set_app_limit(app_name, limit)
        except ValueError:
            pass
