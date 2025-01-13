import keyboard

def replace_characters():
    print("Bắt đầu chế độ thay thế ký tự")
    print("Nhấn ESC để thoát")

    def swap_char(event):
        if event.name == 'a':
            keyboard.press_and_release('backspace')
            keyboard.write('b')
            return False
        elif event.name == 'b':
            keyboard.press_and_release('backspace')
            keyboard.write('a')
            return False
        return True

    keyboard.on_press(swap_char)
    keyboard.wait('esc')
    keyboard.unhook_all()
    print("Đã thoát chế độ thay thế")

if __name__ == "__main__":
    try:
        replace_characters()
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        keyboard.unhook_all()   