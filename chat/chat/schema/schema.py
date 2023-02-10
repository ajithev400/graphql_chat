import graphene
import channels
import channels_graphql_ws
from graphql_auth.schema import MeQuery
from graphene_django.filter import DjangoFilterConnectionField
from chat.schema.mutations.graph_auth import AuthMutation
from chat.schema.mutations.send_message import SendMessage
from chat.schema. mutations.create_chat import CreateChat
from chat.schema.types import MessageType, ChatFilter, ChatType, MessageFilter
from chat.models import Chat
from chat.subscriptions import OnNewMessage


class Query(MeQuery, graphene.ObjectType):
    chats = DjangoFilterConnectionField(ChatType, filterset_class=ChatFilter)
    chat = graphene.Field(ChatType, id=graphene.ID())
    messages = DjangoFilterConnectionField(
        MessageType,
        filterset_class=MessageFilter, id=graphene.ID())

    @staticmethod
    def resolve_chats(cls, info, **kwargs):
        user = info.context.user
        return Chat.objects.prefetch_related("messages", "participants").filter(participants=user)

    @staticmethod
    def resolve_chat(cls, info, id, **kwargs):
        user = info.context.user
        return Chat.objects.prefetch_related("participants").get(participants=user, id=id)

    @staticmethod
    def resolve_messages(cls, info, id, **kwargs):
        user = info.context.user
        chat = Chat.objects.prefetch_related("messages", "participants").get(participants=user, id=id)
        return chat.messages.all()


class Mutations(AuthMutation, graphene.ObjectType):
    send_message = SendMessage.Field()
    create_chat = CreateChat.Field()

    
class Subscription(graphene.ObjectType):
    on_new_message = OnNewMessage.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, subscription=Subscription)



class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema

    async def on_connect(self, payload):
        self.scope['user'] = await channels.auth.get_user(self.scope)