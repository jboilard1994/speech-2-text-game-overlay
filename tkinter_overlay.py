import logging
import tkinter as tk
import sys
from datetime import datetime
from typing import Callable, Any
from state_machine import SpeechStates
from pynput import keyboard
from speech_processing import speech2text

from threading import Thread
from queue import Queue

logger = logging.getLogger(__name__)

def report_callback_exception(exc_type, val, tb):
    if issubclass(exc_type, GracefulExit):
        sys.exit(0)

    logger.error('Exception occured, exiting:', exc_info=(exc_type, val, tb))
    sys.exit(1)



class GracefulExit(Exception):
    "Allows callbacks to gracefully exit without logging error" 


class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """
    def __init__(self,
                 close_callback: Callable[[Any], None],
                 initial_text: str,
                 initial_delay: int,
                 get_new_text_callback: Callable[[], "tuple[int, str]"]):
        self.state="waiting"
        self.close_callback = close_callback
        self.initial_text = initial_text
        self.initial_delay = initial_delay
        self.get_new_text_callback = get_new_text_callback
        self.root = tk.Tk()
        self.sm = SpeechStates(self)
        self.first_time_listening = True
        self.q = Queue()
        self.thread = None
        

        # Set up Close Label
        self.close_label = tk.Label(
            self.root,
            text=' X ',
            font=('Consolas', '10'),
            fg='grey10',
            bg='thistle3'
        )
        self.close_label.bind("<Button-1>", close_callback)
        self.close_label.grid(row=0, column=0)

        # Set up text Label
        self.text = tk.StringVar()
        self.text_label = tk.Label(
            self.root,
            textvariable=self.text,
            font=('Consolas', '10'),
            fg='grey1',
            bg='light pink'
        )
        self.text_label.grid(row=0, column=1)

        # Define Window Geometry
        self.root.overrideredirect(True)
        self.root.geometry("+100+1045")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def update_label(self) -> None:
        self.root.wm_attributes("-topmost", 1)
        if self.state != "listening":
            self.first_time_listening = True
        
        if self.state == "waiting":
            update_text = "waiting..."
            bg_color = 'grey82'
            self.text.set(update_text)
            self.text_label.config(bg=bg_color)
            
        elif self.state == "listening":
            self.text.set("listening...")
            self.text_label.config(bg='light goldenrod')

            if self.first_time_listening == True:
                self.translated_text = ""
                self.thread = Thread(target=speech2text, args=[self.q])
                self.thread.start()
                self.first_time_listening = False
            elif not self.thread.is_alive(): #thread execution ended
                if self.q.empty():
                    self.sm.stop_listening()
                else:
                    self.translated_text = self.q.get()
                    self.sm.init_pasting() #change state
                
        elif self.state == "pasting":
            if self.translated_text == "":
                self.is_paste_or_abort = 0
                self.sm.paste_or_abort()
            else:
                self.text.set(self.translated_text)
                self.sm.text_to_paste = self.translated_text
                self.text_label.config(bg='DarkSeaGreen1')

    
        self.root.after(self.initial_delay, self.update_label)


    def run(self) -> None:
        with keyboard.GlobalHotKeys({'<ctrl>': self.sm.start_abort, '<enter>': self.sm.copy}) as h:
            self.text.set(self.initial_text)
            self.root.after(self.initial_delay, self.update_label)
            self.root.mainloop()

#from .overlay import Overlay, GracefulExit

class Events:
    """
    This the main logic that is called by the GUIs event loop
    """
    def __init__(self):
        pass
        
    def close(self, _) -> None:
        sys.exit()

    def update_text(self):
        """Return tuple of milliseconds till next update and string message to display"""
        return str(datetime.today())

