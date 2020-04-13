from django.db import models
from register.models import User

class Question(models.Model):
    question_title = models.CharField(max_length = 40)
    question_level = models.IntegerField(default = 1)
    question_text = models.TextField(max_length = 600)
    question_source = models.CharField(max_length = 40)
    question_lable = models.CharField(max_length = 20)
    cin_format = models.TextField(max_length = 300)
    cout_format = models.TextField(max_length = 300)
    data_range = models.TextField(max_length = 300)
    cin_example = models.TextField(max_length = 100)
    cout_example = models.TextField(max_length = 100)
    time_limit = models.IntegerField(default = 1000)
    memory_limit = models.IntegerField(default = 65536)

    def __str__(self):
        return self.question_title

class Record(models.Model):
    q_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    u_id = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length = 20) 
    code = models.TextField(max_length = 2000)
    cout = models.TextField(max_length = 2000)
    lang = models.TextField(max_length = 10)
    time = models.IntegerField(default = 0)
    memory = models.IntegerField(default = 0)
    def __str__(self):
        return self.status

# Create your models here.
