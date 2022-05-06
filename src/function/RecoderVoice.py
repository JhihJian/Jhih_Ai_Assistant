import wave
from datetime import datetime
import threading
import time

import keyboard
import pyaudio

from src.function.CapsLockMonitor import CapsLockMonitor

MC_KEY_NAME = "输入麦克风"


# audio.terminate() 没有调用
class RecordVoice:
    CHUNK = 1024  # 数据包或者数据片段
    FORMAT = pyaudio.paInt16  # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
    CHANNELS = 1  # 声道，1为单声道，2为双声道
    RATE = 16000  # 采样率，每秒钟16000次
    MAX_RECORD_TIME = 60  # 秒
    voice_recording = False
    recording_finish = False
    record_frames = []
    device_index = 1
    is_ready = None

    def beginRecordVoice(self):
        print("开始录音")
        self.record_frames = []
        self.voice_recording = True
        threading.Thread(target=self.recording).start()  # 开始录音

    def finishRecordVoice(self):
        print("录音结束")
        self.voice_recording = False
        self.finish()

    def get_record_frames(self):
        return self.record_frames

    def is_recoder_finish(self):
        return not self.voice_recording

    def __init__(self, audio=pyaudio.PyAudio()):
        self.audio = audio
        self.device_index = self.choose_device()

    def choose_device(self):
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        # 默认用1
        deviceIndex = 1
        deviceName = ""
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                name = self.audio.get_device_info_by_host_api_device_index(0, i).get('name')
                if MC_KEY_NAME in name:
                    deviceIndex = i
                    deviceName = name
                print("Input Device id ", i, " - ", name)

        print("recording via index:" + str(deviceIndex) + "and name:" + deviceName)
        return deviceIndex

    def recording(self):
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                 rate=self.RATE, input=True, input_device_index=self.device_index,
                                 frames_per_buffer=self.CHUNK)
        self.record_frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.MAX_RECORD_TIME)):
            if not self.voice_recording:
                break
            data = stream.read(self.CHUNK)
            self.record_frames.append(data)

        print("recording stopped,记录长度:" + str(len(self.record_frames)))
        stream.stop_stream()
        stream.close()
        self.recording_finish = True

    def finish(self):
        while not self.recording_finish:
            time.sleep(0.01)
        # self.audio.terminate()
        self.save_to_file()

    def save_to_file(self):
        WAVE_OUTPUT_FILENAME = "recordedFile.wav"
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.record_frames))
        waveFile.close()


if __name__ == '__main__':
    recordVoice = RecordVoice()
    monitor = CapsLockMonitor(begin_event_hook=recordVoice.beginRecordVoice,
                              finish_event_hook=recordVoice.finishRecordVoice)
    # 开始监听大写锁定键()
    monitor.run()

    # 阻塞进程
    keyboard.wait()
