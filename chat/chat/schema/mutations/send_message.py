import graphene
from django.utils import timezone
from chat.schema.types import MessageType
from chat.models import Chat, Message
from chat.subscriptions import OnNewMessage



class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        message = graphene.String(required=True)
        chat_id = graphene.Int(required=True)

    @classmethod
    def mutate(cls, _, info, message, chat_id):
        user = info.context.user
        chat = Chat.objects.prefetch_related("participants").get(participants=user, id=chat_id)
        message = Message.objects.create(
            sender=user,
            text=message,
            created=timezone.now()
        )
        chat.messages.add(message)
        users = [usr for usr in chat.participants.all() if usr != user]
        for usr in users:
            OnNewMessage.broadcast(payload=message, group=usr.username)
        return SendMessage(message=message)