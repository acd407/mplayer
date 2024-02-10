#!/bin/python
import sys
import time
import mido

class Note:
    SPEED :int = 120
    SEGMENT :int = 0
    OFFSET :int = 0

class Output:
    def __init__(self) -> None:
        self.port = mido.open_output('FluidSynth GM')

    def send(self, tone) -> None:
        self.port.send(mido.Message('note_on', note=tone, velocity=127))

def parse(s: str) -> tuple[int, float]:
    if s[0] == 'S':
        Note.SPEED = int(s[1:])
        return 0, 0.
    elif s[0] == 'O':
        if s[1] == '+':
            Note.SEGMENT += 1
        elif s[1] == '-':
            Note.SEGMENT -= 1
        elif s[1] >= '1' and s[1] <= '7':
            Note.OFFSET = int(s[1])
        return 0, 0.
    else:
        # C, C#, D, D#, E, F, F#, G, G#, A, A#, B,
        # 0      2      4  5      7      9      11 
        natural_note = [0,2,4,5,7,9,11]
        delay, segment, offset = 6e4 / Note.SPEED, Note.SEGMENT, Note.OFFSET
        tone = 1
        # 前缀
        if s[0] == '#':
            offset += 1
            s = s[1:]
        while s[0] == '+':
            segment += 1
            s = s[1:]
        while s[0] == '-':
            segment -= 1
            s = s[1:]
        # 音符
        if s[0] == '0':
            tone = 0
        elif s[0] > '0' and s[0] <= '7':
            offset += natural_note[int(s[0])-1]
        else:
            tone = 0
            delay = 0
        s = s[1:]

        if len(s) > 0 and s[0] == '\'':
            delay = 0
            # ' 用于和下一个音符连起来，因此不需要向后取字符
        # 延时
        # '3/-' 等价于 '3.'
        # '/' 相当于小数部分，'-' 相当于整数部分
        while len(s) > 0 and s[0] == '/':
            delay /= 2
            s = s[1:]
        if len(s) > 0 and s[0] == '.':
            delay *= 1.5
            s = s[1:]
        while len(s) > 0 and s[0] == '-':
            delay += 6e4 / Note.SPEED
            # delay *= 2
            s = s[1:]
        if tone:
            tone = 60 + segment * 12 + offset
        return tone, delay


def main():
    with open(sys.argv[1]) as file:
        output = Output()
        for line in file:
            for s in line.split(','):
                s = s.strip()
                if len(s) == 0:
                    continue
                if s[0] == '@':
                    break
                print(f'{s:<8}', end='')
                tone, delay = parse(s)
                print(f'{tone:<4}', f'{delay:.2f}')
                if tone:
                    output.send(tone)
                if delay:
                    time.sleep(delay / 1e3)


if __name__ == '__main__':
    main()
