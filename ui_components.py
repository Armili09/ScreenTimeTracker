import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class CustomStyle:
    """Custom styling for the application"""
    # Main colors
    BG_COLOR = "#E8F5E9"  # Light mint background
    PRIMARY_COLOR = "#2E7D32"  # Dark green
    SECONDARY_COLOR = "#1976D2"  # Blue
    ACCENT_COLOR = "#FF5722"  # Orange
    WARNING_COLOR = "#F44336"  # Red
    TEXT_COLOR = "#263238"  # Dark gray
    FONT_FAMILY = "Helvetica"

    # Chart colors
    CHART_COLORS = ['#2E7D32', '#1976D2', '#FF5722', '#9C27B0', '#FFC107']

    @staticmethod
    def apply():
        style = ttk.Style()

        # Configure main styles
        style.configure(".", 
                      font=(CustomStyle.FONT_FAMILY, 10),
                      background=CustomStyle.BG_COLOR)

        # Title style
        style.configure("Title.TLabel",
                      font=(CustomStyle.FONT_FAMILY, 16, "bold"),
                      foreground=CustomStyle.PRIMARY_COLOR)

        # Subtitle style
        style.configure("Subtitle.TLabel",
                      font=(CustomStyle.FONT_FAMILY, 12, "bold"),
                      foreground=CustomStyle.SECONDARY_COLOR)

        # Custom button style
        style.configure("Custom.TButton",
                      font=(CustomStyle.FONT_FAMILY, 10, "bold"),
                      background=CustomStyle.ACCENT_COLOR,
                      foreground="white")

        # Progress bar style
        style.configure("Horizontal.TProgressbar",
                      background=CustomStyle.PRIMARY_COLOR,
                      troughcolor=CustomStyle.BG_COLOR,
                      bordercolor=CustomStyle.SECONDARY_COLOR,
                      lightcolor=CustomStyle.PRIMARY_COLOR,
                      darkcolor=CustomStyle.SECONDARY_COLOR)

class StatsFrame(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        """Setup statistics UI components"""
        self.configure(padding="20")

        # Today's usage section
        ttk.Label(self, text="Today's Usage", style="Title.TLabel").pack(pady=(0,15))
        self.today_usage_frame = ttk.Frame(self)
        self.today_usage_frame.pack(fill='x', padx=10)

        # Weekly statistics section
        ttk.Label(self, text="Weekly Statistics", style="Title.TLabel").pack(pady=(20,15))

        # Configure matplotlib style
        plt.style.use('default')  # Use default style instead of seaborn
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor(CustomStyle.BG_COLOR)
        self.ax.set_facecolor(CustomStyle.BG_COLOR)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    def update_stats(self):
        """Update statistics display"""
        for widget in self.today_usage_frame.winfo_children():
            widget.destroy()

        # Update today's usage with improved styling
        row = 0
        for app_name in self.data_manager.data["usage"].keys():
            usage_seconds = self.data_manager.get_today_usage(app_name)
            usage_minutes = usage_seconds / 60
            limit = self.data_manager.get_app_limit(app_name)

            app_frame = ttk.Frame(self.today_usage_frame)
            app_frame.grid(row=row, column=0, pady=5, sticky='ew')

            ttk.Label(app_frame, text=app_name, style="Subtitle.TLabel").grid(row=0, column=0, sticky='w')
            ttk.Label(app_frame, 
                     text=f"{usage_minutes:.1f} min / {limit} min",
                     style="Subtitle.TLabel").grid(row=0, column=1, padx=10)

            if limit > 0:
                progress = ttk.Progressbar(app_frame, length=300, mode='determinate', style="Horizontal.TProgressbar")
                progress['value'] = min(100, (usage_minutes / limit) * 100)
                progress.grid(row=1, column=0, columnspan=2, pady=(5,0), sticky='ew')

            row += 1

        # Update weekly chart with improved styling
        self.ax.clear()
        self.ax.set_facecolor(CustomStyle.BG_COLOR)

        i = 0
        for app_name in self.data_manager.data["usage"].keys():
            weekly_usage = self.data_manager.get_weekly_usage(app_name)
            dates = list(weekly_usage.keys())
            minutes = [seconds/60 for seconds in weekly_usage.values()]
            self.ax.plot(dates, minutes, label=app_name, marker='o', linewidth=2, color=CustomStyle.CHART_COLORS[i % len(CustomStyle.CHART_COLORS)])
            i += 1

        self.ax.set_xlabel('Date', fontsize=10, color=CustomStyle.TEXT_COLOR)
        self.ax.set_ylabel('Minutes', fontsize=10, color=CustomStyle.TEXT_COLOR)
        self.ax.legend(frameon=True)
        self.ax.tick_params(axis='both', colors=CustomStyle.TEXT_COLOR)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        """Setup settings UI components"""
        self.configure(padding="20")

        # App Management Section
        ttk.Label(self, text="App & Website Management", style="Title.TLabel").pack(pady=(0,20))

        # Add new app/site section
        add_frame = ttk.Frame(self)
        add_frame.pack(fill='x', pady=(0,20))

        ttk.Label(add_frame, text="Add New App/Site to Track", style="Subtitle.TLabel").pack(anchor='w')

        input_frame = ttk.Frame(add_frame)
        input_frame.pack(fill='x', pady=(10,0))

        self.new_app_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.new_app_var, width=30).pack(side='left', padx=(0,10))
        ttk.Button(input_frame, text="Add", style="Custom.TButton", 
                   command=self.add_new_app).pack(side='left')

        # Existing apps/sites limits
        ttk.Label(self, text="Time Limits", style="Subtitle.TLabel").pack(anchor='w', pady=(20,10))

        self.limits_frame = ttk.Frame(self)
        self.limits_frame.pack(fill='x')

        self.update_limits_ui()

    def add_new_app(self):
        """Add new app/site to track"""
        new_app = self.new_app_var.get().strip()
        if new_app:
            self.data_manager.set_app_limit(new_app, 0)
            self.new_app_var.set("")
            self.update_limits_ui()

    def update_limits_ui(self):
        """Update the limits UI"""
        for widget in self.limits_frame.winfo_children():
            widget.destroy()

        row = 0
        for app_name in self.data_manager.data["limits"].keys():
            app_frame = ttk.Frame(self.limits_frame)
            app_frame.pack(fill='x', pady=5)

            ttk.Label(app_frame, text=app_name, width=30).pack(side='left')

            limit_var = tk.StringVar(value=str(self.data_manager.get_app_limit(app_name)))
            limit_entry = ttk.Entry(app_frame, textvariable=limit_var, width=10)
            limit_entry.pack(side='left', padx=10)

            ttk.Label(app_frame, text="minutes").pack(side='left')

            ttk.Button(app_frame, text="Save", style="Custom.TButton",
                      command=lambda a=app_name, v=limit_var: self.save_limit(a, v)).pack(side='left', padx=10)

            ttk.Button(app_frame, text="Remove", style="Custom.TButton",
                      command=lambda a=app_name: self.remove_app(a)).pack(side='left')

            row += 1

    def save_limit(self, app_name, limit_var):
        """Save app time limit"""
        try:
            limit = int(limit_var.get())
            self.data_manager.set_app_limit(app_name, limit)
        except ValueError:
            pass

    def remove_app(self, app_name):
        """Remove app from tracking"""
        if app_name in self.data_manager.data["limits"]:
            del self.data_manager.data["limits"][app_name]
            if app_name in self.data_manager.data["usage"]:
                del self.data_manager.data["usage"][app_name]
            self.data_manager.save_data()
            self.update_limits_ui()

CustomStyle.apply()