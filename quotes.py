#!/usr/bin/python3
import requests
import datetime
import tkinter as tk
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
import time

appear_time_in_seconds = 15
interval_time = 10 # In minutes

def get_random_quote():
    try:
        response = requests.get('https://api.quotable.io/random', verify=False)
        if response.status_code == 200:
            quote_data = response.json()
            return quote_data['content'], quote_data['author']
        return None, None
    except Exception as e:
        print(f"Quote fetch error: {e}")
        return None, None

def display_quote_overlay():
    quote, author = get_random_quote()
    if quote and author:
        # Create overlay window
        overlay = tk.Tk()
        overlay.overrideredirect(True)  # Removes window decorations
        overlay.attributes('-topmost', True)  # Keeps window on top
        overlay.attributes('-alpha', 0.7)  # Translucent background
        
        # Position and size
        screen_width = overlay.winfo_screenwidth()
        screen_height = overlay.winfo_screenheight()
        window_width = 400
        window_height = 150
        x = (screen_width - window_width) // 2
        y = 50  # 50 pixels from the top
        
        overlay.geometry(f'{window_width}x{window_height}+{x}+{y}')
        overlay.configure(bg='lightgray')
        
        # Quote text
        quote_label = tk.Label(
            overlay, 
            text=f'"{quote}"\n- {author}', 
            wraplength=380, 
            bg='lightgray', 
            font=('Arial', 12)
        )
        quote_label.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Function to close overlay on click
        def close_on_click(event):
            overlay.destroy()
        
        # Bind click event to the entire window
        overlay.bind('<Button-1>', close_on_click)
        
        # Auto-close after specified time
        def auto_close():
            if overlay.winfo_exists():
                overlay.destroy()
        
        overlay.after(appear_time_in_seconds * 1000, auto_close)
        overlay.mainloop()


def main():
    # Create a scheduler
    scheduler = BlockingScheduler()
    
    # Schedule quote display every hour
    scheduler.add_job(display_quote_overlay, 'interval', minutes=interval_time)
    
    print("Quote Overlay Service Started!")
    
    try:
        # This will keep the script running
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nQuote Overlay Service stopped.")

if __name__ == "__main__":
    main()

