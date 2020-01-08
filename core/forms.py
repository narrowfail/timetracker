from datetime import timedelta

from django.core.exceptions import ValidationError
from django.forms import ModelForm, modelformset_factory
from isoweek import Week

from .models import RowModel


class RowModelForm(ModelForm):
    def clean(self):
        cleaned_data = super(RowModelForm, self).clean()
        year = cleaned_data.get('year')
        week = cleaned_data.get('week')

        if year is None:
            raise ValidationError({'year': 'Year cannot be empty.'})

        if week is None:
            raise ValidationError({'week': 'Week cannot be empty.'})

        # Validate week number
        if week < 1 or week > Week.last_week_of_year(year).week:
            raise ValidationError({'week': 'Week does not exist on this year.'})

        # Validate day is not exceeded.
        days = ['day_1', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6', 'day_7']
        for day in days:
            current_day = cleaned_data.get(day)
            if current_day is not None and current_day > timedelta(hours=24):
                raise ValidationError(
                    {day: 'Value cannot exceed 24 hours.'})

        return cleaned_data

    class Meta:
        model = RowModel
        fields = '__all__'


RowModelFormSet = modelformset_factory(RowModel, exclude=('year', 'week',
                                                          'project'), extra=0)
