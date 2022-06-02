import keyboard

from function.BaseFunction import BaseFunction, FunctionStatus
from function.TimeReminderFunction import TimeReminderFunction
from util.AliRecognizer import AliRecognizer
from util.CapsLockMonitor import CapsLockMonitor
from util.RecoderVoice import RecordVoice, recoder_get_input_devices_name

ak_id_key = "ak_id_key"
ak_secret_key = "ak_secret_key"
app_key_key = "app_key_key"
input_mc_name_key = "input_mc_name_key"


def get_input_devices_name():
    return recoder_get_input_devices_name()


class VoiceRecognizerFunction(BaseFunction):
    def __init__(self, function_controller, db, monitor_qq_function):
        super().__init__(function_controller)
        self.aliRecognizer = None
        self.monitor_task = None
        self.recordVoice = None
        self.db = db
        # 如果monitor_qq_function重启怎么办
        self.time_reminder_function = TimeReminderFunction(function_controller, monitor_qq_function)

    def __begin_reg(self):
        # self.aliRecognizer.run()
        self.function_controller.append_sync_task(self.aliRecognizer.run)
        self.function_controller.append_sync_task(self.recordVoice.beginRecordVoice)
        # threading.Thread(target=self.recordVoice.beginRecordVoice).start()

    def start(self):
        ak_id = self.db.get_str_by_key(ak_id_key)
        ak_secret = self.db.get_str_by_key(ak_secret_key)
        app_key = self.db.get_str_by_key(app_key_key)
        if (not ak_id) or (not ak_secret) or (not app_key):
            self.logger.error("语音识别功能:ak_id ak_secret app_key must set.")
            return
        input_mc_name = self.db.get_str_by_key(input_mc_name_key)
        if not input_mc_name:
            self.logger.error("语音识别功能:无输入设备，无法启动")
            return
        self.recordVoice = RecordVoice(input_mc_name)

        self.logger.info("语音识别功能:启动中...")

        def handleRecognizerResult(result):
            if self.time_reminder_function.mainEntry(result):
                return
            else:
                keyboard.write(result)

        self.aliRecognizer = AliRecognizer(ak_id=ak_id, ak_secret=ak_secret, app_key=app_key,
                                           get_record_frames=self.recordVoice.get_record_frames,
                                           is_finish=self.recordVoice.is_recoder_finish,
                                           recognizer_callable=handleRecognizerResult)

        self.function_status = FunctionStatus.STARTING

        self.monitor = CapsLockMonitor(begin_event_hook=self.__begin_reg,
                                       finish_event_hook=self.recordVoice.finishRecordVoice)
        # 开始监听大写锁定键()

        self.monitor_task = self.function_controller.append_sync_task(self.monitor.run)
        self.function_status = FunctionStatus.RUNNING
        self.logger.info("语音识别功能:启动完成")

    def quit(self):
        self.logger.info("语音识别功能:退出中...")
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
            self.logger.info("monitor task cancel")
        self.aliRecognizer.finish()
        self.logger.info("语音识别功能:退出完成")

        self.function_status = FunctionStatus.STOP
