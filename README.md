## Examples

```bash
./demo.sh
```

```
./main.py demo/mu1.txt
```

## Requirement

* `python` 3

* `fluidsynth` lib, and it's `python` binding `pyfluidsynth`

* `Posix` compatible shell, for running examples

    *this branch don't need a midi port*

## About `fluidsynth`

`FluidSynth` is a real-time software synthesizer based on the `SoundFont` 2 specifications and has reached widespread distribution.

### About it's `python` binding

On `ArchLinux` , you can find it on `AUR` which named with `pyfluidsynth-git` .

On other platform, just use `pip` .

the source is [`fluidsynth`](https://github.com/FluidSynth/fluidsynth) .

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

    *so `5.` equals `5/-`*

### other instructions

* `T` for choose musical instrument

* `S` for set speed (per one minute)

* `O` for fixed note decorated
