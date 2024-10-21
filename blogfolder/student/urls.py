# from django.urls import path
# from . import views 

# urlpatterns = [
#     path('students/', views.student_list, name='student_list'),
# ]

from django.urls import path
from . import views
from .home import HomepageView

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('', HomepageView.as_view(), name= 'homeview')
]
