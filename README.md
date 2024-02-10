## Examples

```bash
./demo.sh
```

```
./main.py demo/mu1.txt
```

## Requirement

* `python` 3
* `mido` lib, [Document](https://mido.readthedocs.io/en/stable/index.html)
* `Posix` compatible shell, for running examples
* a MIDI device

## MIDI Document

please see [`mido`](https://mido.readthedocs.io/en/stable/index.html) and [MIDI](https://en.wikipedia.org/wiki/MIDI)

## The syntax of `mplayer`

* [optional] `<note decorated>`
* note: from `0` - `7`
* [optional] `'` Hyphens: for playing notes together
* [optional] `<time decorated>`

`<note decorated>`:

* `+` and `-` : increase or decrease the segment
* `#` : add half tone

`<time decorated>`

* `.` for 1.5 times long
* `/` for 0.5 times long (Effect stacking)
* `-` for extra original 1 times long (Effect stacking)

### other instructions

* `T` for choose musical instrument

* `S` for set speed (per one minute)

* `O` for fixed note decorated