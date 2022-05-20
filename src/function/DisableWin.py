from pynput import keyboard
from datetime import datetime


class DisableKey:
    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(self, key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    wait_time = 1000 * 1000  # 设置监听缓存时间，长按1000毫秒后开始
    last_time = datetime.now()

    def win32_event_filter(self, msg, data):
        # win key ,disable win
        if data.vkCode == 0x5B:
            # Suppress x
            listener.suppress_event()
        # 1秒内连按两下left crtl 屏蔽第二下
        print('0x%x' % data.vkCode)
        if data.vkCode == 0xa2:
            diff = (datetime.now() - self.last_time).microseconds
            print("按下crtl,时差:{}".format(diff))
            if diff < self.wait_time:
                listener.suppress_event()
            self.last_time = datetime.now()


if __name__ == '__main__':
    disableKey = DisableKey()
    # Collect events until released
    with keyboard.Listener(
            on_press=disableKey.on_press,
            on_release=disableKey.on_release, win32_event_filter=disableKey.win32_event_filter) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    # listener = keyboard.Listener(win32_event_filter=win32_event_filter)
    # listener.start()
