import channels
import channels_graphql_ws
import graphene
from chat.schema.types import MessageType


class OnNewMessage(channels_graphql_ws.Subscription):
    message = graphene.Field(MessageType)

    class Arguments:
        chatroom = graphene.String()

    def subscribe(cls, info, chatroom=None):
        return [chatroom] if chatroom is not None else None

    def publish(self, info, chatroom=None):
        return OnNewMessage(
            message=self
        )