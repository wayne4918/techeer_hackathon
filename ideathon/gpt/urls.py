# gpt/urls.py
from django.urls import path
from .views import gpt_answer_list, CreateView, GptAnswerListView

urlpatterns = [
    path('answers/', gpt_answer_list, name='answer_list'),
    path('send/', CreateView.as_view(), name='send_to_gpt'),
    path('gpt-answers/', GptAnswerListView.as_view(), name='gpt-answers'),
]
