


from tkinter_overlay import Events, Overlay

if __name__ == "__main__":
    events = Events()
    overlay = Overlay(events.close, 'waiting for text input...', 100, events.update_text)
    overlay.run()

    