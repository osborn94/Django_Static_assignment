from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import InquiryForm
# from .models import Inquiry

# Create your views here.

def inquiry_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Send an email to the admin
            send_mail(
                'New Submission from {}'.format(inquiry.name),
                'Message: {}\nEmail: {}'.format(inquiry.message, inquiry.email),
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],  # Admin email
                fail_silently=False,
            )

            # Send email to the user
            send_mail(
                'Thank you for your submission',
                'We have received your message: {}'.format(inquiry.message),
                settings.EMAIL_HOST_USER,
                [inquiry.email],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('success')
        else:
            messages.error(request, 'There was an error in the form submission. Please try again.')
    else:
        form = InquiryForm()

    return render(request, 'blog/contact.html', {'form': form})        

def succ_ess(request):
    return render(request, "blog/success.html")

def blog_home(request):
    return render(request, "blog/index.html")

# def Contact_us(request):
#     return render(request, "blog/contact.html")

def post_list(request):
    return render(request, "blog/post.html")
