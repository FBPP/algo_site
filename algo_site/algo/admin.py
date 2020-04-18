from django.contrib import admin

from .models import Question, Record, Solution, Sol_vote, Sol_comment

admin.site.register(Question)
admin.site.register(Record)
admin.site.register(Solution)
admin.site.register(Sol_vote)
admin.site.register(Sol_comment)

# Register your models here.
