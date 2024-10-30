# from django.shortcuts import render
# from .models import Student, Student_Profile, CohortGroup, Program
# from django.core.paginator import Paginator
# import pdb

# # Create your views here.
# def student_list(request):
#     students = Student.objects.all()  # Query all Student records
#     paginator = Paginator(students, 3)
#     context = {
#         'students': students  # Pass the query result to the template context
#     }
#     # pdb.set_trace
#     return render(request, 'blog/indexmain.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Student, Student_Profile, CohortGroup, Program
from django.core.paginator import Paginator

def student_list(request):
    students = Student.objects.all()  # Query all Student records
    paginator = Paginator(students, 3)  # Show 3 students per page

    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    context = {
        'page_obj': page_obj  # Pass the paginated object to the template context
    }

    return render(request, 'blog/indexmain.html', context)


def student_prof(request, username):
    # Get the student by username or return a 404 if not found
    studentprof = get_object_or_404(Student, username=username)

    # Access related courses and programs
    cohortgroup = studentprof.cohortgroup.all()
    courses = studentprof.courses.all()

    # Find related students based on the same cohort group(s)
    related_students = Student.objects.filter(
        cohortgroup__in=cohortgroup
    ).exclude(id=studentprof.id)  # Exclude the current student
    

    # pass the student data to the template
    context = {
        'studentprof': studentprof,
        'courses': courses,
        'cohortgroup': cohortgroup,
        'related_students': related_students,
    }
    return render(request, "blog/about2.html", context)
