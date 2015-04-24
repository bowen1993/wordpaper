from django.db import models
from accounts.models import User

# Create your models here.

class Word(models.Model):
    origin_word   = models.CharField(max_length=128, default=None, null=False)
    explanation   = models.TextField(default=None, null=True)
    mean          = models.TextField(default=None, null=True)
    level         = models.IntegerField(default=0)
    count         = models.IntegerField(default=0)
    create_date   = models.DateTimeField(auto_now_add=True)
    is_remembered = models.BooleanField(default=False)
    is_delete     = models.BooleanField(default=False)
    remember_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    delete_date   = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    user          = models.ForeignKey(User)

    def __unicode__(self):
        return self.origin_word

    class Meta:
        db_table = "words_word"
