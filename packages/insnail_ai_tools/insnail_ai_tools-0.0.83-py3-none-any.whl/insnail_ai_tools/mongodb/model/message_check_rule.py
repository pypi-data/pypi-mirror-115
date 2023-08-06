import datetime

import mongoengine
from mongoengine import EmbeddedDocumentField

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin, StrChoicesMixin
from insnail_ai_tools.mongodb.model.wecom.wecom_personal_messge import UserRoleChoices


class RuleContentTypeChoices(StrChoicesMixin):
    text = "text"
    weapp = "weapp"
    link = "link"
    file = "file"
    image = "image"
    voice = "voice"
    record = "record"
    meeting_voice = "meeting_voice"
    all = "all"


class RuleMeta(mongoengine.EmbeddedDocument):
    rule = mongoengine.StringField(verbose_name="规则")
    note = mongoengine.StringField(verbose_name="备注")


class NotifyModeChoices(StrChoicesMixin):
    """
    选择realtime就是，实时通知到质检，self的那个就是会通知到说话的本人。record就是单纯的记录
    """

    REAL_TIME = "REAL_TIME"
    SELF_NOTIFY = "SELF_NOTIFY"
    RECORD = "RECORD"


class MessageCheckRule(mongoengine.DynamicDocument, MultiDatabaseMixin):
    content_type = mongoengine.StringField(
        verbose_name="内容的类型",
        choices=RuleContentTypeChoices.choices(),
        max_length=50,
        default=RuleContentTypeChoices.all,
        help_text="内容的类型，比如文本，link, 如果填写ALL，则对所有类型对话检查",
    )
    role = mongoengine.StringField(
        verbose_name="检查对象", choices=UserRoleChoices.choices(), help_text="检查对象，即说话的对象"
    )
    level = mongoengine.IntField(
        verbose_name="风险等级", default=1, help_text="风险等级，等级越高越紧急"
    )
    notify_mode = mongoengine.StringField(
        verbose_name="通知方式",
        choices=NotifyModeChoices.choices(),
        default=NotifyModeChoices.RECORD,
    )
    is_legal = mongoengine.BooleanField(
        verbose_name="是否合法", default=False, help_text="如果为True，则相当于白名单"
    )
    illegal_type = mongoengine.StringField(
        verbose_name="违规类型", max_length=100, help_text="违规类型，比如跳单"
    )
    note = mongoengine.StringField(verbose_name="备注")
    notice_text = mongoengine.StringField(verbose_name="通知文本")

    rule_type = mongoengine.StringField(
        verbose_name="规则类型",
        choices=(("REGEX", "REGEX"), ("SUBSTRING", "SUBSTRING")),
    )
    rule_list = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(RuleMeta), verbose_name="规则列表"
    )
    exclude_rule_list = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(RuleMeta),
        verbose_name="除外规则列表",
    )
    exclude_black_user_id = mongoengine.BooleanField(
        verbose_name="剔除违禁微信名单", default=False
    )

    meta = {
        "collection": "message_check_rule",
        "indexes": [
            "content_type",
            "role",
            "level",
            "is_legal",
            "illegal_type",
            "rule_type",
            "exclude_black_user_id",
        ],
        "abstract": True,
    }

    def __str__(self):
        return f"{self.content_type}_{self.illegal_type}_{self.role}"


class WecomUserExtraInfo(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    用户额外信息的库，一般在质检中用到，比如收集用户个人的微信号、手机号等
    """

    user_id = mongoengine.StringField(verbose_name="用户ID", primary_key=True)
    user_name = mongoengine.StringField(verbose_name="用户名称")
    phone_number = mongoengine.StringField(verbose_name="手机号")
    black_wechat_id = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="违禁微信列表"
    )

    meta = {
        "collection": "wecom_user_extra_info",
        "indexes": ["#user_name", "#phone_number"],
        "abstract": True,
    }


class IllegalMeta(mongoengine.EmbeddedDocument):
    illegal_type = mongoengine.StringField(verbose_name="违规类型")
    illegal_level = mongoengine.IntField(verbose_name="违规等级")
    illegal_words = mongoengine.ListField(mongoengine.StringField(), verbose_name="违规词")

    def __str__(self):
        return f"{self.illegal_type}-{self.illegal_type}-{self.illegal_words}"


class MessageCheckResult(mongoengine.DynamicDocument, MultiDatabaseMixin):
    msg_id = mongoengine.StringField(verbose_name="对于消息的ID")
    msg_mode = mongoengine.StringField(verbose_name="消息类型")
    msg_time = mongoengine.DateTimeField(verbose_name="消息时间")

    content = mongoengine.StringField(
        verbose_name="消息预览", help_text="消息预览，如果需要查看全部消息请跳转"
    )
    illegal_list = mongoengine.ListField(
        EmbeddedDocumentField(IllegalMeta), verbose_name="违规列表"
    )

    illegal_with_review = mongoengine.BooleanField(
        verbose_name="复核是否违规", default=None, help_text="复核之后是否为真的违规"
    )

    create_time = mongoengine.DateTimeField(
        verbose_name="创建时间", default=datetime.datetime.now
    )

    meta = {
        "collection": "message_check_result",
        "indexes": ["#msg_id", "#msg_mode", "msg_time", "illegal_with_review"],
        "abstract": True,
    }

    def __str__(self):
        return f"{self.msg_id}-{self.msg_mode}-{self.illegal_list}"


class MonitorMessageType(StrChoicesMixin):
    PERSONAL = "PERSONAL"
    GROUP = "GROUP"


class MonitorExpireType(StrChoicesMixin):
    H_24 = "H_24"
    H_48 = "H_48"


class ReplyMonitorResult(mongoengine.DynamicDocument, MultiDatabaseMixin):
    external_user_id = mongoengine.StringField(verbose_name="对应external_user_id")
    user_id = mongoengine.StringField(verbose_name="对应user_id")

    group_id = mongoengine.StringField(verbose_name="群ID")
    owner_id = mongoengine.StringField(verbose_name="群主ID")

    msg_id = mongoengine.StringField(verbose_name="消息ID")

    msg_type = mongoengine.StringField(
        verbose_name="消息类型，群消息OR个人消息", choices=MonitorMessageType.choices()
    )
    expire_type = mongoengine.StringField(
        verbose_name="过期类型", choices=MonitorExpireType.choices()
    )

    create_time = mongoengine.DateTimeField(
        verbose_name="创建时间", default=datetime.datetime.now
    )
    meta = {
        "collection": "reply_monitor_result",
        "indexes": [
            "#external_user_id",
            "#user_id",
            "#group_id",
            "#owner_id",
        ],
        "abstract": True,
    }


class ReplyMonitorSkipText(mongoengine.DynamicDocument, MultiDatabaseMixin):
    text = mongoengine.StringField(verbose_name="文本", max_length=200, unique=True)
    is_delete = mongoengine.BooleanField(verbose_name="是否删除", default=False)
    create_time = mongoengine.DateTimeField(
        verbose_name="创建时间", default=datetime.datetime.now
    )

    meta = {
        "collection": "reply_monitor_skip_text",
        "indexes": ["text", "create_time"],
        "abstract": True,
    }
