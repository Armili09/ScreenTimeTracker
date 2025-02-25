from tkinter import messagebox
import platform
import os

class NotificationSystem:
    def __init__(self):
        self.system = platform.system()
        self.streak_count = 0

    def show_notification(self, title, message):
        """Show a system notification with gamified messages"""
        self.streak_count += 1

        # Add gaming-inspired elements to the message
        emojis = ["🎮", "⭐", "🏆", "🌟", "💪", "🎯"]
        emoji = emojis[self.streak_count % len(emojis)]

        gamified_title = f"{emoji} {title}"

        # Add motivational messages
        motivational_messages = [
            "Keep going! You're doing great!",
            "Time for a quick break! Stretch and refresh!",
            "Level up your productivity!",
            "Challenge yourself to stay focused!",
            "You're on a streak! Keep it up!"
        ]

        gamified_message = f"{message}\n\n{motivational_messages[self.streak_count % len(motivational_messages)]}"

        # Use tkinter messagebox for all platforms in Replit environment
        messagebox.showinfo(gamified_title, gamified_message)