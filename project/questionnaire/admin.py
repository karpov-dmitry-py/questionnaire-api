from django.contrib import admin
from .models import Questionnaire, Question, Answer, Poll, CompletedPoll

admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Poll)
admin.site.register(CompletedPoll)
