from rest_framework import status
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Questionnaire, Question, Answer, Poll, CompletedPoll
from .permissions import IsAdminOrReadOnly
from .serializers import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer, \
    PollSerializer, CompletedPollSerializer
from datetime import datetime


class QuestionnaireViewSet(ModelViewSet):
    queryset = Questionnaire.objects.filter(end_date__gt=datetime.now())
    serializer_class = QuestionnaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

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

    @action(detail=True)
    def completed_polls(self, request, pk=None):
        questionnaire = Questionnaire.objects.get(pk=pk)
        completed_polls = questionnaire.completed_polls.all()
        serializer = CompletedPollSerializer(completed_polls, many=True)
        return Response(serializer.data)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    @action(detail=True)
    def polls(self, request, pk=None):
        user_id = request.query_params.get('user_id', 0)
        question = Question.objects.get(pk=pk)
        polls = question.polls.filter(user_id=user_id) if user_id else question.polls.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def answers(self, request, pk=None):
        question = Question.objects.get(pk=pk)
        answers = question.answers.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=False)
    def answers(self, request):
        user_id = request.query_params.get('user_id', 0)
        user_answers = Poll.objects.filter(user_id=user_id)
        serializer = PollSerializer(user_answers, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        save_result = super().create(request, *args, **kwargs)

        # проверим, можно ли считать опрос пройденным
        question_id = request.data['question']
        user_id = request.data['user_id']
        question = Question.objects.get(pk=question_id)
        questionnaire = question.questionnaire
        questions = questionnaire.questions.all()
        polls = Poll.objects.filter(question__questionnaire=questionnaire).filter(user_id=user_id)

        # есть как минимум один ответ для каждого вопроса
        for question in questions:
            result = any(question.id == poll.question.id for poll in polls)
            if not result:
                break
        else:
            completed_poll = CompletedPoll(user_id=user_id, questionnaire=questionnaire)
            completed_poll.save()

        return save_result


class CompletedPollViewSet(ModelViewSet):
    queryset = CompletedPoll.objects.all()
    serializer_class = CompletedPollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    @action(detail=False)
    def by_user(self, request):
        user_id = request.query_params.get('user_id', 0)
        user_completed_polls = CompletedPoll.objects.filter(user_id=user_id)
        serializer = CompletedPollSerializer(user_completed_polls, many=True)
        return Response(serializer.data)
