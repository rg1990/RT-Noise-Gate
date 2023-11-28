# Real Time Noise Gate


Currently a work in progress, this is a prototype [noise gate](https://en.wikipedia.org/wiki/Noise_gate) application built using Python. <br>
The purpose of this project is to build a prototype in Python before implementing the noise gate as a VST plugin using C++ with the JUCE framework.

## Design and Implementation
- The state design pattern is used to control the noise gate's behaviour and state transitions. The `State` abstract base class and the concrete classes are defined in `gate_states.py`.<br>

## Features
- Configurable noise gate parameters: threshold, attack time, hold time, release time, and lookahead time.
- Faster than real-time processing enables use with an audio output stream, processing audio during playback.


## To Do
- Fix the implementation of the hold parameter. The definition is currently wrong.
- ~~Handle threshold and signal values in dBFS rather than amplitude/magnitude.~~
- ~~Process blocks of audio in a stream (`sounddevice.OutputStream`) rather than processing the whole array at once.~~
- Build a GUI with noise gate controls, a waveform viewer/navigator with playhead, and real-time scrolling display of unprocessed & processed audio. Simple wireframe shown below.

![noise_gate_gui_wireframe](https://github.com/rg1990/RT-Noise-Gate/assets/70291897/27502eb8-a10a-40f4-ad82-b2b156baef48)


## Future Feature Development
- **Filtering**: Add low-pass and high-pass filters so gate responds to filtered signal.
- **ML Classifier**: Add a machine learning classifier to reject unwanted sounds that exceed the threshold. An example of this is bleed in the snare microphone from other drum kit components in a multi-track drum recording. A low threshold value may be needed to capture subtle snare dynamics e.g. ghost notes, however this can lead to the gate being triggered by other drum kit components that are picked up by the snare mic. A machine learning model may help reject such false positives.
