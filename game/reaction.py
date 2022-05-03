from threading import Thread
from time import sleep
import platform

done = False

class _Getch:
    def __init__(self):
        if platform.system() == "Windows":
            self.impl = _GetchWindows()
        else:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()


class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


class Game:
    def __init__(self, attempts, length, time):
        self.done = False
        self.time = time
        self.length = length + 1 if length % 2 == 0 else length
        self.attempts = attempts
        self.attempt = 0
        self.sides = int((self.length - 1)/2)
        self.win = lambda x: x == self.length//2 + 1
        self.top = self.eadge_maker("_")
        self.bottom = self.eadge_maker("‾")
        self.ends = ["|","|"]
        self.line = " "

    def start(self, win_msg = "You pass", fail_msg = "You fail"):
        for i in range(self.attempts):
            self.attempt = i + 1
            self.t = ThreadWithResult(target=self.play)
            self.t.start()
            
            self.space()

            self.done = True
            self.t.join()
            result = self.t.result

            if result:
                print(win_msg)
                return True
            else:
                print(fail_msg)

            self.space()
            
            self.done = False
        return False

    def printer(self, current):
        pos = self.length - current - 1
        print(self.top)
        print(self.ends[0] + self.line*current + "●" + self.line*pos + self.ends[1])
        print(self.bottom)

    def play(self):
        pac = False
        while True:
            if pac:
                ran = range(self.length-1, 0, -1)
                pac = False
            else:
                ran = range(self.length)
                pac = True
            for i in ran:
                print('\033[H\033[J', end="")
                print(f"You are on attempt {self.attempt} of {self.attempts}!")
                self.printer(i)
                if self.done:
                    if self.win(i):
                        return True
                    else:
                        return False
                sleep(self.time)
    
    def space(self):
        while True:
            if ord(getch()) == 32:
                break

    def eadge_maker(self, symbol, margin = 0, seperator = "|"):
        side = symbol*(self.sides - margin)
        if margin == 0:
            return " " + side + seperator + side
        else:
            return " " + side + seperator + symbol*(2 * margin - 1) + seperator + side

    def change(self, margin, seperator = ["|","|"], eadge = ["_","‾"], ends = ["|","|"], line = " "):
        self.line = line
        self.ends = ends
        self.top = self.eadge_maker(eadge[0], margin, seperator[0])
        self.bottom = self.eadge_maker(eadge[1], margin, seperator[1])
        if margin != 0:
            self.win = lambda x: self.length//2 - margin < x < self.length//2 + 2 + margin