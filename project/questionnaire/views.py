from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Questionnaire, Question, Answer, Poll
from .serializers import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer, PollSerializer
from datetime import datetime


class QuestionnaireViewSet(ModelViewSet):
    queryset = Questionnaire.objects.filter(end_date__gt=datetime.now())
    serializer_class = QuestionnaireSerializer

    def update(self, request, pk=None):

        serializer = QuestionnaireSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        questionnaire = self.get_object()
        if questionnaire.start_date != serializer.validated_data['start_date']:
            return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True)
    def questions(self, request, pk=None):
        questionnaire = Questionnaire.objects.get(pk=pk)
        questions = Question.objects.filter(questionnaire=questionnaire)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True)
    def answers(self, request, pk=None):
        question = Question.objects.get(pk=pk)
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=False)
    def answers(self, request):
        user_id = request.data.get('user_id', 0)
        user_answers = Poll.objects.filter(user_id=user_id)
        serializer = PollSerializer(user_answers, many=True)
        return Response(serializer.data)
