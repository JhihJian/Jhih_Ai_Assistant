# qq消息处理 需要一个上下文
# 1. 固定格式，进行固定功能的消息


# 查询功能列表
from util.DbHelper import DbHelper


# JJ_SCORE_KEY = "JJ_SCORE_KEY"
# ZZ_SCORE_KEY = "ZZ_SCORE_KEY"


class Context:
    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.function_key = None
        self.current_message = None
        self.function_step = 0
        self.add_score = 0
        self.score_reason = ""
        # 用于拦截需要协商的请求
        self.intercept_id = None


class MessageHandle:
    def __init__(self, monitorQQ):
        self.handle_dict = {
            "功能列表": self.functionDisplay,
            "查询分数": self.queryScore,
            "加分审核": self.scoreTalk,
            # "计时提醒": self.scoreTalk,
            # "事件提醒": self.scoreTalk,
        }
        # 用于处理需要协商的内容
        self.form_context = None
        self.context_dict = {}
        self.monitorQQ = monitorQQ
        self.db = DbHelper()

    # 主入口
    # TODO context 会变，有多线程问题
    def mainEntry(self, sender_id, message):
        # 如果属于协商信息，则直接返回
        if self.intercept_form_confirm(sender_id, message):
            return
        if sender_id in self.context_dict.keys():
            context = self.context_dict[sender_id]
        else:
            context = Context(sender_id)
            self.context_dict[sender_id] = context
        context.current_message = message
        function = self.getMapFunction(context)
        function(context)

    def getMapFunction(self, context):
        function = None
        # 倘若 功能已进行中
        if context.function_key:
            function = self.handle_dict[context.function_key]
        # 倘若 属于 功能关键词
        elif context.current_message in self.handle_dict.keys():
            function = self.handle_dict[context.current_message]
            context.function_key = context.current_message
            context.function_step = 0
        # 否则 无效
        else:
            function = self.notFoundFunction
        return function

    def notFoundFunction(self, context):
        self.monitorQQ.send_message(context.sender_id, "没发现对应功能")
        context.function_key = None

    def queryScore(self, context):
        zz_score = self.db.get_zz_score()
        jj_score = self.db.get_jj_score()
        reply_message = f"当前仔仔分数:{zz_score}\r\n当前健健分数:{jj_score}"
        self.monitorQQ.send_message(context.sender_id, reply_message)
        context.function_key = None

    def functionDisplay(self, context):
        reply_message = "功能列表:\n\r"
        for i in range(1, len(self.handle_dict)):
            key = list(self.handle_dict.keys())[i]
            reply_message += f"{i}. {key}.\n\r"
        self.monitorQQ.send_message(context.sender_id, reply_message)
        context.function_key = None

    # 加分审核
    def scoreTalk(self, context):
        if context.function_step == 0:
            self.monitorQQ.send_message(context.sender_id, "申请为自己增加多少分？")
            context.function_step = 1
            return
        elif context.function_step == 1:
            try:
                context.add_score = float(context.current_message)
            except Exception as e:
                self.monitorQQ.send_message(context.sender_id, f"输入值不正确，退出流程？错误信息{e}")
                context.function_step = 0
                context.function_key = None
                return
            self.monitorQQ.send_message(context.sender_id, "申请为自己加分原因？")
            context.function_step = 2
            return

        elif context.function_step == 2:
            context.score_reason = context.current_message
            self.monitorQQ.send_message(context.sender_id, "正在发给对方审核确认，请稍等")
            if context.sender_id == 980858153:
                ask_man = "健健"
                target_id = 1600074410
            else:
                ask_man = "仔仔"
                target_id = 980858153
            form_message = f"{ask_man} 申请增加分数 {context.add_score} 原因:{context.score_reason} 请问是否同意?\r\n回复”同意“或”不同意“"
            self.monitorQQ.send_message(target_id, form_message)
            context.intercept_id = target_id
            self.form_context = context
            context.function_step = 3
            return

        # 如果同意
        elif context.function_step == 3:
            if context.sender_id == 980858153:
                self.db.update_jj_score(context.add_score, context.score_reason)
            else:
                self.db.update_zz_score(context.add_score, context.score_reason)

            self.monitorQQ.send_message(context.sender_id, "对方已同意，加分成功")

        # 如果不同意
        elif context.function_step == 4:
            self.monitorQQ.send_message(context.sender_id, "对方未同意，加分失败")

        context.function_step = 0
        context.function_key = None

    # 返回是否拦截成功，若拦截成功，则信息不处理
    def intercept_form_confirm(self, sender_id, message):

        if self.form_context and self.form_context.intercept_id == sender_id:
            if message == "同意" or message == "不同意":
                if message == "同意":
                    context = self.form_context
                    self.selfEntry(context)
                else:
                    context = self.form_context
                    context.function_step += 1
                    self.selfEntry(context)

                self.form_context = None
                return True

        return False

    def selfEntry(self, context):
        function = self.getMapFunction(context)
        function(context)
