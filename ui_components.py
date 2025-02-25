import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class CustomStyle:
    """Custom styling for the application with gamified elements"""
    # Vibrant color palette inspired by fitness apps
    BG_COLOR = "#1E1E2E"  # Dark background
    CARD_BG = "#2A2A3C"   # Slightly lighter for cards
    PRIMARY_COLOR = "#FF4B6C"  # Hot pink
    SECONDARY_COLOR = "#00E1D9"  # Cyan
    ACCENT_COLOR = "#7B61FF"  # Purple
    SUCCESS_COLOR = "#00FF94"  # Neon green
    WARNING_COLOR = "#FFB800"  # Warning yellow
    TEXT_COLOR = "#FFFFFF"  # White text
    FONT_FAMILY = "Helvetica"

    # Chart colors - vibrant gradient
    CHART_COLORS = ['#FF4B6C', '#7B61FF', '#00E1D9', '#00FF94', '#FFB800']

    @staticmethod
    def apply():
        style = ttk.Style()

        # Configure main styles
        style.configure(".", 
                      font=(CustomStyle.FONT_FAMILY, 10),
                      background=CustomStyle.BG_COLOR,
                      foreground=CustomStyle.TEXT_COLOR)

        # Title style
        style.configure("Title.TLabel",
                      font=(CustomStyle.FONT_FAMILY, 24, "bold"),
                      foreground=CustomStyle.PRIMARY_COLOR,
                      background=CustomStyle.BG_COLOR)

        # Subtitle style
        style.configure("Subtitle.TLabel",
                      font=(CustomStyle.FONT_FAMILY, 16, "bold"),
                      foreground=CustomStyle.SECONDARY_COLOR,
                      background=CustomStyle.BG_COLOR)

        # Stats label style
        style.configure("Stats.TLabel",
                      font=(CustomStyle.FONT_FAMILY, 12),
                      foreground=CustomStyle.TEXT_COLOR,
                      background=CustomStyle.CARD_BG)

        # Custom button style
        style.configure("Custom.TButton",
                      font=(CustomStyle.FONT_FAMILY, 12, "bold"),
                      background=CustomStyle.ACCENT_COLOR,
                      foreground=CustomStyle.TEXT_COLOR)

        # Progress bar style with gradient effect
        style.configure("Horizontal.TProgressbar",
                      thickness=25,
                      background=CustomStyle.SUCCESS_COLOR,
                      troughcolor=CustomStyle.CARD_BG,
                      bordercolor=CustomStyle.CARD_BG,
                      lightcolor=CustomStyle.SUCCESS_COLOR,
                      darkcolor=CustomStyle.PRIMARY_COLOR)

        style.configure("Main.TFrame", background=CustomStyle.CARD_BG, padding=10)
        style.configure("Custom.TEntry", foreground=CustomStyle.TEXT_COLOR, background=CustomStyle.CARD_BG, fieldbackground=CustomStyle.CARD_BG)


class StatsFrame(ttk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()

    def setup_ui(self):
        """Setup statistics UI components"""
        self.configure(padding="20", style="Main.TFrame")
        self["background"] = CustomStyle.BG_COLOR

        # Today's usage section with card-like appearance
        title_frame = ttk.Frame(self)
        title_frame["style"] = "Main.TFrame"
        title_frame.pack(fill='x', pady=(0,20))

        ttk.Label(title_frame, 
                 text="🎯 Today's Progress", 
                 style="Title.TLabel").pack(side='left')

        self.today_usage_frame = ttk.Frame(self)
        self.today_usage_frame["style"] = "Main.TFrame"
        self.today_usage_frame.pack(fill='x', padx=10)

        # Weekly statistics section
        weekly_title_frame = ttk.Frame(self)
        weekly_title_frame["style"] = "Main.TFrame"
        weekly_title_frame.pack(fill='x', pady=(20,15))

        ttk.Label(weekly_title_frame, 
                 text="📊 Your Journey", 
                 style="Title.TLabel").pack(side='left')

        # Configure matplotlib style for gaming aesthetic
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor(CustomStyle.BG_COLOR)
        self.ax.set_facecolor(CustomStyle.CARD_BG)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    def update_stats(self):
        """Update statistics display"""
        for widget in self.today_usage_frame.winfo_children():
            widget.destroy()

        # Update today's usage with gaming-inspired styling
        row = 0
        for app_name in self.data_manager.data["usage"].keys():
            usage_seconds = self.data_manager.get_today_usage(app_name)
            usage_minutes = usage_seconds / 60
            limit = self.data_manager.get_app_limit(app_name)

            # Create card-like frame for each app
            app_frame = ttk.Frame(self.today_usage_frame)
            app_frame["style"] = "Main.TFrame"
            app_frame.grid(row=row, column=0, pady=10, sticky='ew')
            app_frame["padding"] = 10

            # App name with emoji
            emoji_map = {
                "Google Chrome": "🌐",
                "Firefox": "🦊",
                "Microsoft Edge": "📱",
                "Netflix": "🎬",
                "YouTube": "▶️"
            }
            emoji = emoji_map.get(app_name, "📱")

            ttk.Label(app_frame, 
                     text=f"{emoji} {app_name}", 
                     style="Subtitle.TLabel").grid(row=0, column=0, sticky='w')

            # Usage stats with gaming-style formatting
            progress_text = f"⏱️ {usage_minutes:.1f}m / {limit}m"
            if limit > 0:
                progress_percent = min(100, (usage_minutes / limit) * 100)
                level = int(progress_percent / 20) + 1
                progress_text += f" (Level {level})"

            ttk.Label(app_frame, 
                     text=progress_text,
                     style="Stats.TLabel").grid(row=0, column=1, padx=10)

            if limit > 0:
                progress = ttk.Progressbar(app_frame, 
                                        length=300, 
                                        mode='determinate', 
                                        style="Horizontal.TProgressbar")
                progress['value'] = min(100, (usage_minutes / limit) * 100)
                progress.grid(row=1, column=0, columnspan=2, pady=(10,0), sticky='ew')

            row += 1

        # Update weekly chart with gaming aesthetic
        self.ax.clear()
        self.ax.set_facecolor(CustomStyle.CARD_BG)

        # Plot data with gradients and glow effects
        for i, app_name in enumerate(self.data_manager.data["usage"].keys()):
            weekly_usage = self.data_manager.get_weekly_usage(app_name)
            dates = list(weekly_usage.keys())
            minutes = [seconds/60 for seconds in weekly_usage.values()]

            color = CustomStyle.CHART_COLORS[i % len(CustomStyle.CHART_COLORS)]
            self.ax.plot(dates, minutes, 
                        label=app_name, 
                        marker='o', 
                        linewidth=3,
                        color=color,
                        markerfacecolor=color,
                        markeredgecolor='white',
                        markeredgewidth=2,
                        markersize=8)

        self.ax.set_xlabel('Date', fontsize=12, color=CustomStyle.TEXT_COLOR)
        self.ax.set_ylabel('Minutes', fontsize=12, color=CustomStyle.TEXT_COLOR)
        self.ax.legend(frameon=True, facecolor=CustomStyle.CARD_BG, 
                      edgecolor=CustomStyle.SECONDARY_COLOR)
        self.ax.tick_params(axis='both', colors=CustomStyle.TEXT_COLOR)
        self.ax.grid(True, alpha=0.2, color=CustomStyle.SECONDARY_COLOR)

        # Add some padding around the plot
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
        self["background"] = CustomStyle.BG_COLOR

        # App Management Section
        ttk.Label(self, text="⚙️ App Control Center", 
                 style="Title.TLabel").pack(pady=(0,20))

        # Add new app/site section
        add_frame = ttk.Frame(self)
        add_frame["style"] = "Main.TFrame"
        add_frame.pack(fill='x', pady=(0,20))

        ttk.Label(add_frame, text="🎮 Add New App to Track", 
                 style="Subtitle.TLabel").pack(anchor='w')

        input_frame = ttk.Frame(add_frame)
        input_frame["style"] = "Main.TFrame"
        input_frame.pack(fill='x', pady=(10,0))

        self.new_app_var = tk.StringVar()
        entry = ttk.Entry(input_frame, 
                         textvariable=self.new_app_var, 
                         width=30)
        entry.pack(side='left', padx=(0,10))
        entry["style"] = "Custom.TEntry"

        ttk.Button(input_frame, 
                  text="Add", 
                  style="Custom.TButton",
                  command=self.add_new_app).pack(side='left')

        # Time limits section
        ttk.Label(self, text="⏱️ Time Limits", 
                 style="Subtitle.TLabel").pack(anchor='w', pady=(20,10))

        self.limits_frame = ttk.Frame(self)
        self.limits_frame["style"] = "Main.TFrame"
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
            app_frame["style"] = "Main.TFrame"
            app_frame.pack(fill='x', pady=10)

            ttk.Label(app_frame, 
                     text=f"🎮 {app_name}", 
                     width=30,
                     style="Stats.TLabel").pack(side='left')

            limit_var = tk.StringVar(value=str(self.data_manager.get_app_limit(app_name)))
            limit_entry = ttk.Entry(app_frame, 
                                  textvariable=limit_var, 
                                  width=10)
            limit_entry.pack(side='left', padx=10)
            limit_entry["style"] = "Custom.TEntry"

            ttk.Label(app_frame, 
                     text="minutes",
                     style="Stats.TLabel").pack(side='left')

            ttk.Button(app_frame, 
                      text="Save", 
                      style="Custom.TButton",
                      command=lambda a=app_name, v=limit_var: self.save_limit(a, v)).pack(side='left', padx=10)

            ttk.Button(app_frame, 
                      text="Remove", 
                      style="Custom.TButton",
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