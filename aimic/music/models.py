from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)

    class Meta:
        db_table = "Register"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Feedback"
