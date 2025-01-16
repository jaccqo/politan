from django.urls import path
from . import views

app_name="core"

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('services/', views.services, name='services'),  # Services
    path('gallery/', views.gallery, name='gallery'),  # Gallery
    path('contact/', views.contact, name='contact'),  # Contact Us
    path('about/', views.about, name='about'),  # About Us
    path('get-quote/<str:service_slug>/', views.get_quote, name='get_quote'),
     path('submit-quote/', views.submit_quote, name='submit_quote'),
     path('project/<slug:project_slug>/', views.project_detail, name='project_detail'),
    path('contact-form-handler/', views.contact_form_handler, name='contact_form_handler'),
     path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('post-comment/', views.post_comment, name='post_comment'),
    path('search/', views.search_blog, name='search_blog'),

]
