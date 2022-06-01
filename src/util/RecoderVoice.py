import wave
import threading
import time

import pyaudio

from util.AliRecognizer import AliRecognizer
from function.FunctionController import FunctionController
from util.CapsLockMonitor import CapsLockMonitor


# MC_KEY_NAME = "输入麦克风"


def recoder_get_input_devices_name():
    audio = pyaudio.PyAudio()
    info = audio.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    names = []
    for i in range(0, num_devices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            name = audio.get_device_info_by_host_api_device_index(0, i).get('name')
            names.append(name)
    return names


# 从名为"输入麦克风"的设备 进行录音
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

    def __init__(self, input_mc_name, audio=pyaudio.PyAudio(), is_write_wave_file=False):
        self.audio = audio
        self.is_write_wave_file = is_write_wave_file
        self.input_mc_name = input_mc_name
        self.device_index = self.choose_device()

    def beginRecordVoice(self):
        print("开始录音")
        self.record_frames = []
        self.voice_recording = True
        self.recording()  # 开始录音

    def finishRecordVoice(self):
        print("录音结束")
        self.voice_recording = False
        self.finish()

    # 用于语音识别的对外接口
    def get_record_frames(self):
        return self.record_frames

    # 用于语音识别的对外接口
    def is_recoder_finish(self):
        return not self.voice_recording

    def choose_device(self):
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        # 默认用1
        deviceIndex = 1
        deviceName = ""
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                name = self.audio.get_device_info_by_host_api_device_index(0, i).get('name')
                if self.input_mc_name in name:
                    deviceIndex = i
                    deviceName = name
                # print("Input Device id ", i, " - ", name)

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
        if self.is_write_wave_file:
            self.save_to_file()

    def save_to_file(self):
        WAVE_OUTPUT_FILENAME = "recordedFile.wav"
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.record_frames))
        waveFile.close()

# if __name__ == '__main__':
#     fc = FunctionController()
#     fc.start()
#     recordVoice = RecordVoice()
#     aliRecognizer = AliRecognizer(get_record_frames=recordVoice.get_record_frames,
#                                   is_finish=recordVoice.is_recoder_finish, recognizer_callable=lambda s: print(s))
#
#
#     def begin_reg():
#         recordVoice.beginRecordVoice()
#         aliRecognizer.run()
#
#
#     monitor = CapsLockMonitor(begin_event_hook=begin_reg,
#                               finish_event_hook=recordVoice.finishRecordVoice)
#     # 开始监听大写锁定键()
#
#     task = fc.append_sync_task(monitor.run)
#
#     # time.sleep(8)
#     # print("task.cancel()")
#     # task.cancel()
#     # time.sleep(3)
#     # print("fc.stop")
#     # fc.stop()
#
#     # 阻塞进程
#     # keyboard.wait()
