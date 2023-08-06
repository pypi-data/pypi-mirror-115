import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin
from insnail_ai_tools.mongodb.model.wecom.meta import (
    IllegalMeta,
    WecomMessageActionChoices,
)


class WecomGroupMessage(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    origin data scheme:
    +--------------+-------------+------+-----+-------------------+-----------------------------+
    | Field        | Type        | Null | Key | Default           | Extra                       |
    +--------------+-------------+------+-----+-------------------+-----------------------------+
    | msg_id       | varchar(64) | NO   | PRI | NULL              |                             |
    | room_id      | varchar(64) | YES  | MUL | NULL              |                             |
    | from_user_id | varchar(64) | NO   |     | NULL              |                             |
    | msg_time     | timestamp   | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
    | msg_type     | varchar(32) | NO   |     | NULL              |                             |
    | to_list      | text        | YES  |     | NULL              |                             |
    | action       | varchar(10) | YES  |     | NULL              |                             |
    | content      | text        | YES  |     | NULL              |                             |
    | url          | text        | YES  |     | NULL              |                             |
    | create_time  | timestamp   | YES  |     | NULL              |                             |
    +--------------+-------------+------+-----+-------------------+-----------------------------+
    """

    msg_id = mongoengine.StringField(verbose_name="消息ID", primary_key=True)
    room_id = mongoengine.StringField(verbose_name="群id")
    from_user_id = mongoengine.StringField(verbose_name="发送者id", max_length=64)
    msg_type = mongoengine.StringField(verbose_name="消息类型", max_length=100)
    to_list = mongoengine.ListField(mongoengine.StringField(), verbose_name="消息接收方列表")
    action = mongoengine.StringField(
        verbose_name="action",
        max_length=16,
        choices=WecomMessageActionChoices.choices(),
        default="send",
        required=True,
    )
    content = mongoengine.DictField(verbose_name="消息内容")
    content_text = mongoengine.StringField(verbose_name="文本内容")  # 从content中提取的文本内容
    url = mongoengine.StringField(verbose_name="消息附加链接", null=True)

    msg_time = mongoengine.DateTimeField(verbose_name="发送时间")
    create_time = mongoengine.DateTimeField(verbose_name="创建时间")

    # 质检
    is_legal = mongoengine.BooleanField(verbose_name="是否合规", default=None)
    illegal_list = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(IllegalMeta), verbose_name="违规列表"
    )

    illegal_with_review = mongoengine.BooleanField(
        verbose_name="复核是否违规", default=None, help_text="复核之后是否为真的违规"
    )
    meta = {
        "collection": "wecom_group_message",
        "indexes": [
            "#room_id",
            "#from_user_id",
            "#msg_type",
            "#action",
            "msg_time",
            "is_legal",
            "illegal_with_review",
        ],
        "abstract": True,
    }
