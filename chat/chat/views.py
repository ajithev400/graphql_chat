
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from chat.schema.schema import schema

@csrf_exempt
def chat_graphql_view(request):
    return GraphQLView.as_view(graphiql=True, schema=schema)(request)
