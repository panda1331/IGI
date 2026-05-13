from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question
