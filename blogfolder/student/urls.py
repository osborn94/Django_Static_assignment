# from django.urls import path
# from . import views 

# urlpatterns = [
#     path('students/', views.student_list, name='student_list'),
# ]

from django.urls import path
from . import views
# from .home import HomepageView
from .views  import StudentDetailView, Add_Students, EditStudentView, DeleteView
from .cohorts_groups import CreateCohort, CohortVeiw,ChortDeleteView

urlpatterns = [
    path('', views.student_list, name='student_list'),
    # path('', HomepageView.as_view(), name= 'homeview'),
    path('abouts/<str:username>/', views.student_prof, name= 'about'),
    path('send-message', views.send_message, name='send_message'),
    path('add', Add_Students.as_view() ,name='add_student'),
    path('<str:username>', StudentDetailView.as_view, name='profiles'),
    # path('delete/<str:username>', DeleteView.as_view, name='delete'),
    path('student/<str:username>/delete/', DeleteView.as_view(), name='delete_student'),
    path('edit/<str:username>/', EditStudentView.as_view(), name='edit_student'),
    path('add_view', CohortVeiw.as_view(), name='add_view'),
    path('add_cohort', CreateCohort.as_view(), name='add_cohort'),
    path('add-view', ChortDeleteView.as_view(), name='delete_view'),

]
