from django.shortcuts import render
from .models import Student, Student_Profile, CohortGroup, Program
import pdb

# Create your views here.
def student_list(request):
    students = Student.objects.all()  # Query all Student records
    context = {
        'students': students  # Pass the query result to the template context
    }
    # pdb.set_trace
    return render(request, 'blog/indexmain.html', context)

