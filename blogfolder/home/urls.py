from django.urls import path
from .views import blog_home, post_list, succ_ess, inquiry_view
from .about import About_us

urlpatterns = [
    path('', blog_home, name='home'),
    path('about_us/', About_us, name='aboutus'),  # Added trailing slash for consistency
    path('contact_us/', inquiry_view, name='contactus'),  # Update this to point to inquiry_view
    path('post_list/', post_list, name='post'),  # Added trailing slash for consistency
    path('success/', succ_ess, name='success'),  # Added trailing slash for consistency
]
