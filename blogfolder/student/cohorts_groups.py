
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views.generic import View
from .models import CohortGroup,Student


class CohortVeiw(View):
    def get(self, request):
        all_cohort = CohortGroup.objects.all()
        return render(request,'blog/cohortview.html', {'all_cohort':all_cohort})


class CreateCohort(View):
    def post(self,request):
        name = request.POST['cohortname']

        if not name:
            return HttpResponse('cohort name cannot be empty')
        
        if CohortGroup.objects.filter(name=name).exists():
             return HttpResponse('cohort name already exists')
        
        CohortGroup.objects.create(name=name)
        return HttpResponse('cohort name created')




class ChortDeleteView(View):
    def get(self, request, pk):
        cohorts   =  get_object_or_404(CohortGroup, pk=pk)
        cohorts.delete()
        return redirect('add_view')