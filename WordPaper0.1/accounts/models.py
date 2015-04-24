from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table="words_user"
