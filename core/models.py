import operator
from datetime import timedelta
from functools import reduce

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (Model, CharField, TextField, DurationField,
                              PositiveIntegerField, ForeignKey, CASCADE)


class ProjectModel(Model):
    name = CharField('name', max_length=250)
    description = TextField('description', null=True, blank=True)

    def __str__(self):
        return self.name

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        ordering = ('-id',)


class RowModel(Model):
    year = PositiveIntegerField('year', validators=[MaxValueValidator(2500),
                                                    MinValueValidator(1900)])
    week = PositiveIntegerField('week number')
    project = ForeignKey(ProjectModel, verbose_name='project',
                         on_delete=CASCADE)

    day_1 = DurationField('monday', blank=True, null=True)
    day_2 = DurationField('tuesday', blank=True, null=True)
    day_3 = DurationField('wednesday', blank=True, null=True)
    day_4 = DurationField('thursday', blank=True, null=True)
    day_5 = DurationField('friday', blank=True, null=True)
    day_6 = DurationField('saturday', blank=True, null=True)
    day_7 = DurationField('sunday', blank=True, null=True)

    def total_duration(self):
        return reduce(operator.add, filter(None, [self.day_1, self.day_2,
                                                  self.day_3, self.day_4,
                                                  self.day_5, self.day_6,
                                                  self.day_7]),
                      timedelta(seconds=0))

    def __str__(self):
        return str(self.id)

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'row'
        verbose_name_plural = 'rows'
        ordering = ('-id',)
        unique_together = (('year', 'week', 'project'),)
