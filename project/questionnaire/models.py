from django.db import models


class Questionnaire(models.Model):
    title = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    body = models.TextField()

    def __str__(self):
        return f'[id: {self.id}] {self.title}, дата начала: {self.start_date}, дата окончания: {self.end_date}'

    class Meta:
        ordering = ['start_date']


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('text', 'ответ текстом'),
        ('single_choice', 'ответ с выбором одного варианта'),
        ('multiple_choices', 'ответ с выбором нескольких вариантов'),
    )

    title = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, default='text')
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f'[Questionnaire id: {self.questionnaire.id}] id: {self.id}. {self.title}'


class Answer(models.Model):
    text = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'[Question id: {self.question}] id: {self.id}. {self.text}'


class Poll(models.Model):
    user_id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='polls')
    user_answer = models.CharField(max_length=500, null=False)

    def __str__(self):
        return f'[ user id: {self.user_id}, question id: {self.question.id}] id: {self.id}. ответ: {self.user_answer}'


class CompletedPoll(models.Model):
    user_id = models.IntegerField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='completed_polls')
    completion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user id: {self.user_id}, questionnaire id: {self.questionnaire.id}, опрос пройден: {self.completion_date}'
