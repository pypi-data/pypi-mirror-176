from typing import Optional

from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.event import Event, EventWithChat

from nonebot_plugin_pixivbot import context
from nonebot_plugin_pixivbot.model import PostIdentifier, T_UID, T_GID
from nonebot_plugin_pixivbot.protocol_dep.post_dest import PostDestination as BasePostDestination, \
    PostDestinationFactory as BasePostDestinationFactory, PostDestinationFactoryManager


class PostDestination(BasePostDestination[int, int]):
    def __init__(self, bot: Bot,
                 user_id: Optional[int] = None,
                 chat_id: Optional[int] = None,
                 chat_type: Optional[str] = None) -> None:
        self.bot = bot
        self._user_id = user_id
        self.chat_type = chat_type
        self.chat_id = chat_id

    @property
    def identifier(self) -> PostIdentifier[T_UID, T_GID]:
        return PostIdentifier("telegram", self._user_id, self.chat_id)

    def normalized(self) -> "PostDestination[T_UID, T_GID]":
        return self

    @property
    def real_chat_id(self) -> int:
        if self.chat_id is not None:
            return self.chat_id
        else:
            return self._user_id


@context.require(PostDestinationFactoryManager).register
class PostDestinationFactory(BasePostDestinationFactory[int, int]):
    @classmethod
    def adapter(cls) -> str:
        return "telegram"

    def build(self, bot: Bot,
              user_id: Optional[int],
              group_id: Optional[int]) -> PostDestination:
        return PostDestination(bot, user_id=user_id, chat_id=group_id)

    def from_event(self, bot: Bot, event: Event) -> PostDestination:
        if isinstance(event, EventWithChat):
            from_ = getattr(event, "from_", None)
            if from_ is not None:
                user_id = from_.id
            else:
                user_id = None

            chat_id = event.chat.id
            if chat_id == user_id:
                # 私聊消息的chat_id == user_id
                chat_id = None

            return PostDestination(bot, user_id=user_id, chat_id=chat_id, chat_type=event.chat.type)
        else:
            raise ValueError("invalid event type: " + str(type(event)))
