from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(SubGuardian)
admin.site.register(UserLoginStreak)
admin.site.register(ContactMessage)
admin.site.register(AssessmentSession)
admin.site.register(MCQQuestion)
admin.site.register(MCQResponse)
admin.site.register(Game1Result)
admin.site.register(Game2Result)
admin.site.register(PersonalizedTask)
admin.site.register(UserTaskStatus)
admin.site.register(DailyProgress)