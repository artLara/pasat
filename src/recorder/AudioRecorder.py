import pyaudio
import wave

class AudioRecorder:
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=None):
        self.__recording = True
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = pyaudio.PyAudio() if py is None else py
        self.frames = []
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def start(self):
        self.__recording = True
        while self.__recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        self.stream.close()

    def stop(self):
        self.__recording = False

    def save(self, path):
        wf = wave.open(path+'audio.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
    
    def saveRelax1(self, path,index):
        if index ==1:
            # path = path+'relax/'
            wf = wave.open(path+'audioRelax.wav', 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
        elif index ==2:
            # path = path+'Instrucciones/'
            wf = wave.open(path+'audioInstrucciones.wav', 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()          