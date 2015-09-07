from threading import Lock

from django.conf.urls import patterns, url
from django.shortcuts import get_object_or_404
from django.utils.html import escape

from restless.exceptions import Unauthorized, BadRequest
from restless.preparers import FieldsPreparer
from restless.resources import skip_prepare

from base.api import AbstractBezzistResource
from .models import Poll


class PollResource(AbstractBezzistResource):

    resource_name = 'polls'
    resource_lock = Lock()

    preparer = FieldsPreparer(fields={
        'id'                        : 'id',
        'question'                  : 'question',
        'finished'                  : 'finished',
        'created'                   : 'created',
        'modified'                  : 'modified',
        'locked'                    : 'locked',
        'default_visible_answers'   : 'default_visible_answers',
        'hide_score_until_finished' : 'hide_score_until_finished',
    })

    def __init__(self, *args, **kwargs):
        super(PollResource, self).__init__(*args, **kwargs)
        self.http_methods.update({
            'answers': {
                'GET': 'answers',
            }
        })

    def wrap_list_response(self, data):
        return {
            'polls'     : data,
            'per_page'  : self.paginator.per_page,
            'count'     : self.paginator.count,
            'num_pages' : self.paginator.num_pages,
        }

    # GET /api/v1/polls
    def list(self):
        raise BadRequest()

    # GET /api/v1/polls/<uuid>
    def detail(self, uuid):
        return get_object_or_404(Poll, uuid=uuid)

    # POST /api/Polls/
    def create(self):
        return Poll.objects.create(poll=escape(self.data.get('poll')))

    # PUT /api/Polls/<uuid>
    def update(self, uuid):
        raise BadRequest()

    # DELETE /api/Polls/<pk>/
    def delete(self, pk):
        raise Unauthorized()

    # GET /api/Polls/<pk>/answers
    @skip_prepare
    def answers(self, pk):
        poll = get_object_or_404(Poll, pk=pk)
        return {
            'answers': map(lambda a: a.shallow_mappify(), poll.answers.all())
        }

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(PollResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns(
            '',
            url(r'^(?P<pk>\d+)/answers$',
                cls.as_view('answers'),
                name=cls.build_url_name('answers', name_prefix)),
        )
