import keyboard
keyboard.add_hotkey('a', lambda: print('a pressed'))
keyboard.add_hotkey('d', lambda: print('d pressed'))
keyboard.add_hotkey('w', lambda: print('w pressed'))
keyboard.wait()