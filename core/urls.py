from django.urls import path

from .views import RowEditorView, RowDeleteView, RowCreateView

urlpatterns = [
    path(r'', RowEditorView.as_view(), name='home'),

    path(r'<int:year>/<int:week>/', RowEditorView.as_view(), name='home-param'),
    # You could use a regexp here instead, but pattern matching is easier.

    path(r'row/<int:pk>/delete/', RowDeleteView.as_view(), name='row-delete'),

    path(r'row/create/', RowCreateView.as_view(), name='row-create'),

]
