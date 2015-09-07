from threading import Lock

from django.shortcuts import get_object_or_404
from django.utils.html import escape

from restless.exceptions import BadRequest, HttpError
from restless.preparers import FieldsPreparer

from base.api import AbstractBezzistResource
from .models import Answer
from poll.models import Poll


class AnswerResource(AbstractBezzistResource):

    resource_name = 'answers'
    resource_lock = Lock()

    hidden_score = -1

    preparer = FieldsPreparer(fields={
        'id'       : 'id',
        'answer'   : 'answer',
        'score'    : 'score',
        'created'  : 'created',
        'modified' : 'modified'
    })

    def prepare(self, data):
        prepped = super(AnswerResource, self).prepare(data)
        if self.poll.hide_score_until_finished:
            prepped['score'] = self.hidden_score
        return prepped

    def wrap_list_response(self, data):
        return {
            'answers': data
        }

    def list(self):
        raise BadRequest(msg='List not supported')

    def detail(self, pk):
        return get_object_or_404(Answer, pk=pk)

    def create(self):
        poll = get_object_or_404(Poll, id=self.data.get('uuid'))
        self.poll = poll  # store for post-prep
        if not poll.finished:
            answer = Answer.objects.create(answer=escape(self.data.get('answer')))
            poll.answers.add(answer)
        else:
            raise HttpError(msg='Answers cannot be added to a closed question.')
        return answer

    # PUT /api/answers/<pk>
    def update(self, pk):
        self.resource_lock.acquire()
        answer = get_object_or_404(Answer, pk=pk)
        poll = Poll.objects.get(id=self.data.get('uuid'))  # poll must exist for answer to exist
        self.poll = poll  # store for post-prep
        if not poll.finished:
            answer.score = self.data.get('score')
            answer.save()
            self.resource_lock.release()
            return answer
        else:
            self.resource_lock.release()
            raise HttpError(msg='This answer can no longer be modified because the question is now closed.' )

    def delete(self, pk):
        raise BadRequest(msg='Delete not yet supported')

