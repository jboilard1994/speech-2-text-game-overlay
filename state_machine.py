import keyboard as keycheck
from pynput import keyboard
from statemachine import StateMachine, State
import pyperclip as pc


import time

class SpeechStates(StateMachine):
 
    #states
    waiting = State('waiting', initial=True)
    listening = State('listening')
    pasting = State('pasting') 

    #transitions
    start = waiting.to(listening)
    stop_listening = listening.to(waiting)
    init_pasting = listening.to(pasting)
    paste_or_abort = pasting.to(waiting)
    
    def __init__(self, obj):
        self.keyboard_control = keyboard.Controller()
        self.is_paste_or_abort = 0
        self.text_to_paste = ""
        self.start_abort, self.copy = self.return_fns()
        super(SpeechStates, self).__init__(obj)

    def on_enter_waiting(self):
        print('waiting')
        
    def on_enter_listening(self):
        print('listening')

    def on_exit_pasting(self):
        if self.is_paste_or_abort == 1:
            pc.copy(self.text_to_paste)
            time.sleep(0.5)
            # open chat
            self.keyboard_control.press(keyboard.Key.enter)
            self.keyboard_control.release(keyboard.Key.enter)

            
            # Press and release space
            time.sleep(0.1)
            self.keyboard_control.type(self.text_to_paste)    



            """self.keyboard_control.press(keyboard.Key.ctrl_l)
            self.keyboard_control.press("v")
            self.keyboard_control.release("v")
            self.keyboard_control.release(keyboard.Key.ctrl_l)"""
            # send to chat
            self.keyboard_control.press(keyboard.Key.enter)
            self.keyboard_control.release(keyboard.Key.enter)
        self.is_paste_or_abort = 0

    def return_fns(self):
        def start_abort():
            if self.current_state == self.waiting:
                self.start()
            elif self.current_state == self.listening:
                self.stop_listening()
            elif self.current_state == self.pasting:
                self.is_paste_or_abort = 0
                self.paste_or_abort()
            
        def copy():
            if self.current_state == self.pasting:
                self.is_paste_or_abort = 1
                self.paste_or_abort()

        return start_abort, copy


    
    



