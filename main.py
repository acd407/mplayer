#!/bin/python
import sys
import time
import mido


class Output:

    def __init__(self) -> None:
        self.port = mido.open_output("FluidSynth GM")

    def send(self, tone) -> None:
        self.port.send(mido.Message("note_on", note=tone, velocity=127))


class Note:
    SPEED: int = 120
    OFFSET: int = 0


# tone:
#   -1 => speed
#   -2 => offset
#   -3 => timbre
def parse(s: str) -> tuple[int, float]:
    # S & O 就在parse里改
    # 需要输出的返回到tuple里
    if s[0] == "S":
        Note.SPEED = int(s[1:])
        return -1, Note.SPEED
    elif s[0] == "O":
        offset = 0
        if s[1] == "+":
            offset = 12
        elif s[1] == "-":
            offset = -12
        else:
            offset = int(s[1:])
        Note.OFFSET += offset
        return -2, offset
    elif s[0] == "T":
        return -3, int(s[1:])
    else:
        # C, C#, D, D#, E, F, F#, G, G#, A, A#, B,
        # 0      2      4  5      7      9      11
        natural_note = [0, 2, 4, 5, 7, 9, 11]
        delay, offset = 6e4 / Note.SPEED, Note.OFFSET
        tone = 1
        # 前缀
        if s[0] == "#":
            offset += 1
            s = s[1:]
        while s[0] == "+":
            offset += 12
            s = s[1:]
        while s[0] == "-":
            offset -= 12
            s = s[1:]
        # 音符
        if s[0] == "0":
            tone = 0
        elif s[0] > "0" and s[0] <= "7":
            offset += natural_note[int(s[0]) - 1]
        else:
            tone = 0
            delay = 0
        s = s[1:]

        if len(s) > 0 and s[0] == "'":
            delay = 0
            # ' 用于和下一个音符连起来，因此不需要向后取字符
        # 延时
        # '3/-' 等价于 '3.'
        # '/' 相当于小数部分，'-' 相当于整数部分
        while len(s) > 0 and s[0] == "/":
            delay /= 2
            s = s[1:]
        if len(s) > 0 and s[0] == ".":
            delay *= 1.5
            s = s[1:]
        while len(s) > 0 and s[0] == "-":
            delay += 6e4 / Note.SPEED
            # delay *= 2
            s = s[1:]
        if tone:
            tone = 60 + offset
        return tone, delay


def main():
    with open(sys.argv[1]) as file:
        output = Output()
        for line in file:
            for s in line.split(","):
                s = s.strip()
                if len(s) == 0:
                    continue
                if s[0] == "@":
                    break
                print(f"{s:<8}", end="")
                match parse(s):
                    case tone, delay if tone >= 0:
                        print(f"{tone:<2}", f"{delay:.2f}")
                        if tone > 0:
                            output.send(tone)
                        if delay > 0:
                            time.sleep(delay / 1e3)
                    case -1, speed:
                        print("S ", f"{speed:d}")
                        pass
                    case -2, offset:
                        print("O ", f"{offset:d}")
                        pass
                    case -3, timbre:
                        print("T ", f"{timbre:d}")
                        output.port.send(
                            mido.Message("program_change", program=timbre))


if __name__ == "__main__":
    main()
