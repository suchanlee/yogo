import time

from django.db import models


class AbstractTimeStampedModel(models.Model):

    '''
    Abstract model class that keeps track of created and modified times.
    Created and modified are automatically kept track on every save.
    '''

    class Meta:
        abstract = True

    created = models.BigIntegerField()
    modified = models.BigIntegerField()

    def _get_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        now_timestamp = time.time()
        self.modified = now_timestamp
        if not self.created:
            self.created = now_timestamp
        super(AbstractTimeStampedModel, self).save(*args, **kwargs)


class MappableModel(object):

    '''
    Provide methods to shallow/deep mappify a Django model.

    In shallow mappification, relation fields (many-to-many and foreignkey)
    return id's of the related object, if it exists.

    In deep mappification, relation fields are recursively
    traveled (1-level) to return a JSON representation of the related object.

    FileField and ImageField returns the url.

    '''

    def deep_mappify(self, exception_fields=[]):
        return self._mappify(deep_copy=True, exception_fields=exception_fields)

    def shallow_mappify(self, exception_fields=[]):
        return self._mappify(deep_copy=False, exception_fields=exception_fields)

    def _mappify(self, deep_copy=False, exception_fields=[]):
        model = {}
        for field in self._meta.fields:
            if field.name in exception_fields:
                pass
            elif isinstance(field, models.FileField) or isinstance(field, models.ImageField):
                try:
                    model[field.name] = getattr(self, field.name).url
                except:
                    model[field.name] = ''
            elif isinstance(field, models.ForeignKey):
                if deep_copy:
                    model[field.name] = self._mappify(getattr(self, field.name))
                else:
                    try:
                        model[field.name] = getattr(self, field.name).id
                    except:
                        model[field.name] = ''
            elif isinstance(field, models.ManyToManyField):
                print field.name
                if deep_copy:
                    model[field.name] = self._mappify(getattr(self, field.name))
                else:
                    try:
                        model[field.name] = map(lambda o: o.id, list(getattr(self, field.name).all()))
                    except:
                        model[field.name] = []
            else:
                model[field.name] = getattr(self, field.name)

        return model
