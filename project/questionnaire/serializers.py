from .models import Questionnaire, Question, Answer, Poll, CompletedPoll
from rest_framework import serializers


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'start_date', 'end_date', 'body']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'question_type', 'questionnaire']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'question']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'user_id', 'question', 'user_answer']

    def throw_exc(self, msg):
        raise serializers.ValidationError(msg)

    def is_user_poll_active(self):
        user_id = self.validated_data['user_id']
        question = self.validated_data['question']
        questionnaire = question.questionnaire
        user_completed_polls = questionnaire.completed_polls.filter(user_id=user_id)

        if user_completed_polls:
            msg = f'Пользователь <{user_id}> ранее уже прошел опрос <{questionnaire.id}>'
            self.throw_exc(msg)

        return True

    def is_wrong_user_answer(self):
        user_id = self.validated_data['user_id']
        question = self.validated_data['question']
        questionnaire = question.questionnaire

        user_answer = self.validated_data['user_answer']
        user_polls = question.polls.filter(user_id=user_id)
        user_polls_count = len(user_polls)

        user_matched_polls = user_polls.filter(user_answer=user_answer)
        user_matched_polls_count = len(user_matched_polls)

        available_answers = question.answers.all()
        available_answers_count = len(available_answers)

        matched_answers = question.answers.filter(text=user_answer)
        matched_answers_count = len(matched_answers)

        # некорректный текст ответа
        is_correct_answer = True if question.question_type == 'text' else bool(matched_answers_count)
        if not is_correct_answer:
            msg = f'Ответ ({user_answer}) пользователя <{user_id}> не соответствует вариантам ответа ' \
                  f'на вопрос <{question.id}> в опросе ({questionnaire.id})'
            self.throw_exc(msg)

        if user_polls_count:

            # лишний ответ
            is_excessive_answer = question.question_type in ('text', 'single_choice') \
                                  or user_polls_count >= available_answers_count
            if is_excessive_answer:
                msg = f'Пользователь <{user_id}> уже ответил на вопрос <{question.id}> в опросе ({questionnaire.id})'
                self.throw_exc(msg)

            # задублированный (не уникальный) ответ
            is_repeated_answer = bool(user_matched_polls_count)
            if is_repeated_answer:
                msg = f'Получен повторяющийся ответ пользователя <{user_id}> на вопрос <{question.id}> ' \
                      f'в опросе ({questionnaire.id})'
                self.throw_exc(msg)

        return True

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=True)

        # проверка - прошел ли пользователь этот опрос ранее
        self.is_user_poll_active()

        # проверка ответа
        self.is_wrong_user_answer()

        return True


class CompletedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedPoll
        fields = ['id', 'user_id', 'questionnaire', 'completion_date']
