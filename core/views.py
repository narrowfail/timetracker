import datetime

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import View, DeleteView
from isoweek import Week

from .forms import RowModelForm, RowModelFormSet
from .models import RowModel


class RowEditorView(View):
    form_class = RowModelFormSet

    initial = {'key': 'value'}
    template_name = 'row-editor.html'

    @staticmethod
    def calc_next(current_year, current_week):
        if current_week + 1 > Week.last_week_of_year(current_year).week:
            return current_year + 1, 1
        return current_year, current_week + 1

    @staticmethod
    def calc_previous(current_year, current_week):
        if current_week - 1 < 1:
            return current_year - 1, Week.last_week_of_year(
                current_year - 1).week
        return current_year, current_week - 1

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year') or datetime.datetime.now().year
        week = kwargs.get('week') or Week.thisweek().week

        if week < 1 or week > Week.last_week_of_year(year).week:
            raise Http404('Invalid week / year.')

        next_year, next_week = self.calc_next(year, week)
        previous_year, previous_week = self.calc_previous(year, week)

        rows = RowModel.objects.filter(year=year, week=week)
        row_formset = self.form_class(queryset=rows)

        create_row_form = RowModelForm()

        return render(request, self.template_name,
                      {'create_row_form': create_row_form,
                       'row_formset': row_formset,
                       'week': week,
                       'year': year,
                       'next_week': next_week,
                       'next_year': next_year,
                       'previous_week': previous_week,
                       'previous_year': previous_year})

    def post(self, request, *args, **kwargs):
        year = kwargs.get('year') or datetime.datetime.now().year
        week = kwargs.get('week') or Week.thisweek().week

        if week < 1 or week > Week.last_week_of_year(year).week:
            raise Http404('Invalid week / year.')

        next_year, next_week = self.calc_next(year, week)
        previous_year, previous_week = self.calc_previous(year, week)

        row_formset = self.form_class(request.POST)

        if row_formset.is_valid():
            row_formset.save()
            success_url = reverse('home-param', args=(year, week))
            return HttpResponseRedirect(success_url)

        create_row_form = RowModelForm()

        return render(request, self.template_name,
                      {'create_row_form': create_row_form,
                       'row_formset': row_formset,
                       'week': week,
                       'year': year,
                       'next_week': next_week,
                       'next_year': next_year,
                       'previous_week': previous_week,
                       'previous_year': previous_year})


class RowDeleteView(DeleteView):
    model = RowModel
    object = None

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = reverse('home-param', args=(self.object.year,
                                                  self.object.week))
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RowCreateView(View):
    object = None

    def post(self, request, *args, **kwargs):
        form = RowModelForm(request.POST)
        if form.is_valid():
            self.object = form.save()
            success_url = reverse('home-param', args=(self.object.year,
                                                      self.object.week))
        else:
            # Warning: Silent form error.
            success_url = reverse('home')

        return HttpResponseRedirect(success_url)
