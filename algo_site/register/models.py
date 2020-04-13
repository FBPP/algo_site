from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length = 20)
    email = models.EmailField()
    password = models.CharField(max_length = 20)
    has_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user_name
class ConfirmString(models.Model):
    code = models.CharField(max_length = 256)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    c_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.user_name + ":" + self.code


# Create your models here.
