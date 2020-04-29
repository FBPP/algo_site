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
    test_total = models.IntegerField(default = 1)
    test_path = models.CharField(max_length = 100)

    def __str__(self):
        return self.question_title

class Record(models.Model):
    q_id = models.ForeignKey(Question, on_delete = models.CASCADE)
    u_id = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField(max_length = 20) 
    code = models.TextField(max_length = 2000)
    lang = models.TextField(max_length = 10)
    time = models.DateTimeField()
    timeused = models.IntegerField(default = 0)
    memoryused = models.IntegerField(default = 0)
    def __str__(self):
        return self.status

class Solution(models.Model):
    author_id = models.ForeignKey(User, on_delete = models.CASCADE)
    qid = models.IntegerField(default = -1)
    title = models.CharField(max_length = 60)
    source_link = models.URLField()
    vote = models.IntegerField(default = 0)
    level = models.IntegerField(default = 0)
    time = models.DateTimeField(default = None)
    content = models.TextField(default = None)

    def __str__(self):
        return self.title

class Sol_vote(models.Model):
    sol_id = models.ForeignKey(Solution, on_delete = models.CASCADE)
    u_id = models.ForeignKey(User, on_delete = models.CASCADE)
    up = models.IntegerField(default = 0)
    down = models.IntegerField(default = 0)

    def __str__(self):
        return self.sol_id.title

class Sol_comment(models.Model):
    sol_id = models.ForeignKey(Solution, on_delete = models.CASCADE)
    u_id = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return self.text
    




# Create your models here.
