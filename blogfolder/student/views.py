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


from .models import Student, Student_Profile, CohortGroup, Program, student_types
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View


def student_list(request):
    students = Student.objects.all()  # Query all Student records
    paginator = Paginator(students, 3)  # Show 3 students per page

    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    context = {
        'page_obj': page_obj, # Pass the paginated object to the template context
        'student_rank': student_types,
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


# modal message
# def send_message(request, username):
def send_message(request):
    # student = get_object_or_404(Student, username=username)
    if request.method == "POST":
        recipient_name = request.POST.get("recipient_name")
        recipient_email = request.POST.get("recipient_email")
        email_title = request.POST.get("email_title", "No Subject")
        message_body = request.POST.get("message_body")
        sender_contact = request.POST.get("sender_contact")
        sender_name = request.POST.get("sender_name")
        sender_email = request.POST.get("sender_email")

        # Validate recipient email
        try:
            validate_email(recipient_email)
            full_message = f"From: {sender_name} with phone number({sender_contact}) and email address ({sender_email})\n\n{message_body}"
            send_mail(
                subject=email_title,
                message=full_message,
                from_email=sender_email,
                recipient_list=[recipient_email],
            )
            messages.success(request, "Message sent successfully!")
        except ValidationError:
            messages.error(request, "Invalid recipient email address.")
        except Exception as e:
            messages.error(request, f"An error occurred:{str(e)}")  

        # return render(request, "blog/about2.html")
        return redirect('student_list')       
    # return render(request, "blog/about2.html")
    return redirect('student_list')
   
class DeleteView(View):
    def get(self, request, username):
        students = get_object_or_404(Student, username=username)
        students.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')

class Add_Students(View):
    def post(self, request):
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname  = request.POST.get('lastname')
        role =     request.POST.get('role')
        cohort_id = request.POST.get('cohort')
        courses = request.POST.get('courses')
        bio =  request.POST.get('bio')
        dob = request.POST.get('dob')
        addrsss =request.POST.get('addrsss')
        rating = request.POST.get('rating')
        profile = request.FILES.get('profile_images')

        print(bio)
        print(dob)
        print(addrsss)
        print(rating)
        print(profile)

        

        if not username:
            return HttpResponse('username field  is required')
        


        if not bio:
            return HttpResponse('about field  is required')
        

        if not rating:
            return HttpResponse('rating field  is required')
        

        
        if Student.objects.filter(username=username).exists():
            return HttpResponse('username already taken')
        
        
        if not role:
            return HttpResponse('role field  is required')
        
         # Check if the role already exists for another student
        if role in ['president', 'secretary'] and Student.objects.filter(student_type=role).exists():
            return HttpResponse(f"The role '{role}' is already assigned to another student.")



        #create student
        students =  Student.objects.create(

            username=username,
            first_name=firstname, 
            last_name =lastname,
            student_type  = role

        )


        Student_Profile.objects.create(
            student=students,
            bio = bio,
            date_of_birth=dob,
            address=addrsss,
            rating = rating,
            profile_picture  = profile

        )
        return HttpResponse('created')


class StudentDetailView(View):
    def get(self, request, username):
        try:
            student_personal_info = Student.objects.get(username=username)
            context = {'student_personal_info': student_personal_info}
            return render(request, 'student_detail.html', context)
        except Student.DoesNotExist:
            return redirect('404')



class EditStudentView(View):
    def get(self, request, username):
        student = get_object_or_404(Student, username=username)
        student_profile = student.student_profile

        # Pass current student data to the template
        context = {
            'student': student,
            'student_profile': student_profile,
        }
        return render(request, 'blog/edit_student.html', context)

    def post(self, request, username):
        student = get_object_or_404(Student, username=username)
        student_profile = student.student_profile

        # Get the updated values from the form
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        role = request.POST.get('role')
        bio = request.POST.get('bio')
        dob = request.POST.get('dob')
        addrsss = request.POST.get('addrsss')
        rating = request.POST.get('rating')
        profile = request.FILES.get('profile_images')

        # Update student and profile information
        student.first_name = firstname
        student.last_name = lastname
        student.student_type = role
        student.save()

        student_profile.bio = bio
        student_profile.date_of_birth = dob
        student_profile.address = addrsss
        student_profile.rating = rating
        if profile:
            student_profile.profile_picture = profile
        student_profile.save()

        messages.success(request, "Student information updated successfully!")
        return redirect('student_list')






    #     try:
    #         validate_email(recipient_email)
    #         full_message = f"From: {sender_name} with phone number({sender_contact}) and email address ({sender_email})\n\n{message_body}"
    #         send_mail(
    #             subject=email_title,
    #             message=full_message,
    #             from_email=sender_email,
    #             recipient_list=[recipient_email],
    #         )
    #         # Return a JSON response indicating success
    #         return JsonResponse({'status': 'success'})
    #     except ValidationError:
    #         return JsonResponse({'status': 'error', 'error': 'Invalid recipient email address.'})
    #     except Exception as e:
    #         return JsonResponse({'status': 'error', 'error': f'An error occurred: {str(e)}'})

    # return JsonResponse({'status': 'error', 'error': 'Invalid request method.'})


    