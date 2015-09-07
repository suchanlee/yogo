import uuid

from django.db import models

from base.models import AbstractTimeStampedModel

from answer.models import Answer


class Poll(AbstractTimeStampedModel):

    question = models.CharField(max_length=300)
    answers = models.ManyToManyField(Answer, blank=True, related_name='poll')
    uuid = models.CharField(max_length=36)

    # Meta
    locked = models.BooleanField(default=False)
    default_visible_answers = models.SmallIntegerField(default=5)
    hide_score_until_finished = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super(Poll, self).save(*args, **kwargs)
