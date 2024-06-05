import json

from django.shortcuts import render
from django.http import JsonResponse
from .models import GptAnswer, Character
from django.conf import settings
import openai
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status



def gpt_answer_list(request):
    answers = GptAnswer.objects.all()





class CreateView(APIView):
    @swagger_auto_schema(
        operation_description="Post data to GPT and create a character with the response",
        operation_id="Create GPT Character",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['character_name', 'tone', 'text_length', 'situation', 'language'],
            properties={
                'character_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the character"),
                'tone': openapi.Schema(type=openapi.TYPE_STRING, description="Tone of the message"),
                'text_length': openapi.Schema(type=openapi.TYPE_INTEGER, description="Length of the text"),
                'situation': openapi.Schema(type=openapi.TYPE_STRING, description="Situation or context for the message"),
                'language': openapi.Schema(type=openapi.TYPE_STRING, description="Language of the character"),
            },
        ),
        responses={
            201: openapi.Response(description="성공"),
            400: openapi.Response(description="실패"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            character_name = data.get('character_name')
            if not character_name:
                return Response({'error': 'Character name is required'}, status=status.HTTP_400_BAD_REQUEST)

            tone = data.get('tone')
            text_length = data.get('text_length')
            situation = data.get('situation')
            language = data.get('language')

            new_character = Character.objects.create(
                character_name=character_name,
                tone=tone,
                text_length=text_length,
                situation=situation,
                language=language
            )

            prompt = f"{situation} [Tone: {tone}, Length: {text_length}, Language: {language}]"
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "Start conversation."},
                          {"role": "user", "content": prompt}],
                api_key=settings.OPENAI_API_KEY
            )

            msg = response['choices'][0]['message']['content']

            GptAnswer.objects.create(
                character=new_character,
                response_content=msg,
            )

            return Response({'message': 'Character created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GptAnswerListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of all GPT answers",
        responses={
            200: openapi.Response(description="A list of GPT answers"),
            500: openapi.Response(description="Internal server error")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            answers = GptAnswer.objects.all().values()
            return Response({'answers': list(answers)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
