from django.shortcuts import render
from django.views.generic import View
from .models import Student, Student_Profile, CohortGroup, Program

class HomepageView(View):
    def get(self, request):
        return render(request, 'blog/')