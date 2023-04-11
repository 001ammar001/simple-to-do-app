from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.main_view,name='main'),
    path('logout/',views.logout_view,name='logout'),
    path('add-task/',views.add_task_view,name='add-task'),
    path('succsess/',views.succsess_tasks_view,name='succsess-tasks'),
    path('archived/',views.archived_tasks_view,name='archived-tasks'),
    path('overdue/',views.overdue_tasks_view,name='overdue-tasks'),
    path('change/<int:id>',views.change_task_view,name='change'),
]