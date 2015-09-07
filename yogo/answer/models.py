from django.db import models

from base.models import AbstractTimeStampedModel


class Answer(AbstractTimeStampedModel):

    score = models.IntegerField(default=0)
    answer = models.CharField(max_length=300)

    class Meta:
        ordering = ['-score', 'created']

    def __unicode__(self):
        return self.answer
