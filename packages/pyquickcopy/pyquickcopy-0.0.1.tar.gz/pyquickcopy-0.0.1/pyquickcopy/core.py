import time
import pyperclip
import traceback


class QuickCopy:
    def __init__(self, listener, listen_rate: float, debug: bool = True):
        self.listener = listener
        self.listen_rate = listen_rate
        self.debug = debug

    def copy(self, string: str):
        try:
            pyperclip.copy(string)
        except:
            traceback.print_exc()

    def paste(self):
        try:
            return pyperclip.paste()
        except:
            traceback.print_exc()

    def clear(self):
        self.copy("")

    def loop(self):
        print("started")
        while True:
            try:
                clipboard = pyperclip.paste()
                _type = type(clipboard).__name__
                _len = len(clipboard)
                if self.debug:
                    template = "type: {}\t len: {}\tclipboard: {}"
                    print(template.format(_type, _len, clipboard))
                self.listener(clipboard)
            except KeyboardInterrupt:
                print("stopping")
                break
            except:
                traceback.print_exc()
            finally:
                time.sleep(self.listen_rate)



