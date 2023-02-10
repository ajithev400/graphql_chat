import graphene
from django.contrib.auth.models import User
from chat.models import Chat
from chat.schema.types import ChatType



class CreateChat(graphene.Mutation):

    chat = graphene.Field(ChatType)
    error = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        name = graphene.String()
    
    @classmethod
    def mutate(cls, _, info, email=None, name=None):
        user = info.context.user
        if email:
            users = []
            participants = User.objects.get(email=email)
            users.append(user)
            users.append(participants)
            chat = Chat.objects.create(
                name = name
            )
            chat.participants.add(*users)
            chat.save()
        else:
            return CreateChat(error="you have to provide the participants email ")
    
        return CreateChat(chat=chat)