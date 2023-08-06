# audio-snippets

## Install
```bash
pip install audio-snippets
```

## Usage
I suggest you use jupyter notebooks to take full advantage of all functions

### Load Audio
```python
from audio_snippets import Sound
s = Sound.from_path('/path/to/audio/file.mp3')
```
### Data
```python
print(s.audio) # just the numpy array :D
print(s.Fs)    # sampling frequency
```
### Play it
```python
s.play()
s.play(x=5)    # play the audio in 5x speed
```
### Size of audio
```python
len(s)         # Number of samples
s.size         # Number of seconds of audio
s.formatted_size 
# length of the audio in seconds/minutes/hours
# E.g.  # 5.323 seconds ; 6.43 minutes ; 1.53 hours
```
### Slice the audio
```python
t = s[3:5]     # Slices the audio from 3 to 5 seconds
t.play()
t = s[:5]      # Slice first 5 seconds
t = s[5:]      # Slice from 5 seconds onward
t = s[::2]     # select every second sample (speeds the audio by 2x)
```
### Plot the waveform
```python
s.plot()             # interactive plotly
s.plot(slice(5, 25)) # plot a slice of the waveform
```
