from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Project,Service,Blog,Comment,Testimonial,Client

from django.db.models import Count
from django.core.paginator import Paginator

def home(request):
    # Get all projects, sorted by date (most recent first)
    projects = Project.objects.all().order_by('-date')

    # Get distinct categories for filtering
    categories = Project.CATEGORY_CHOICES

    clients = Client.objects.all()
   

    return render(request, 'index.html', {'projects': projects, 'categories': categories,'clients': clients})

# Services view
def services(request):
    services = Service.objects.prefetch_related('images').all()
    return render(request, 'services.html', {'services': services})

def gallery(request):
    # Retrieve all projects, prefetch related images for efficiency
    projects = Project.objects.prefetch_related('images').all()

    # Get distinct categories for the filter
    categories = Project.objects.values_list('category', flat=True).distinct()

    # Filter projects by category if specified
    category_filter = request.GET.get('category', None)
    if category_filter:
        projects = projects.filter(category=category_filter)

    return render(request, 'gallery.html', {'projects': projects, 'categories': categories})

# Contact Us view
def contact(request):
    return render(request, 'contact.html')

# About Us view
def about(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'about.html',{'testimonials': testimonials})


def get_quote(request, service_slug):
    # Fetch the service from the database or return 404 if not found
    service = get_object_or_404(Service, slug=service_slug)

    # Store the selected service in session
    request.session['selected_service'] = {
        "name": service.name,
        "description": service.description,
    }

    # Render the quote page with service details
    return render(request, 'get_quote.html', {'service': service})


def submit_quote(request):
    if request.method == 'POST':
        # Retrieve service details from session
        selected_service = request.session.get('selected_service')
        if not selected_service:
            return JsonResponse({'error': 'No service selected'}, status=400)

        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        details = request.POST.get('details')

        # Email setup
        admin_email = settings.CONTACT_EMAIL
        subject = f"New Quote Request for {selected_service['name']}"

        # Render the HTML email content
        html_content = render_to_string('emails/quote_request.html', {
            'service': selected_service['name'],
            'name': name,
            'email': email,
            'details': details,
        })

        # Create and send the email
        try:
            email_message = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email_message.content_subtype = 'html'  # Specify that the email is HTML
            email_message.send()
        except Exception as e:
            return JsonResponse({'error': 'Failed to send email. Please try again later.'}, status=500)

        # Clear the selected service from session
        if 'selected_service' in request.session:
            del request.session['selected_service']

        # Return success response
        return JsonResponse({
            'service': selected_service['name'],
            'name': name,
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def contact_form_handler(request):
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate data
        if not name or not email or not subject or not message:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        # Combine the message with the sender's details
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Send the email
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],  # Replace with the recipient email
            )
            return JsonResponse({'success': 'Message sent successfully.'})
        except Exception as e:
        
            return JsonResponse({'error': 'Failed to send message. Please try again later.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def project_detail(request, project_slug):
   
    project = get_object_or_404(Project.objects.prefetch_related('images'), slug=project_slug)
    return render(request, 'project_detail.html', {'project': project})

# Blog list view
def blog_list(request):
    # Get category and tag filters from the request
    category_filter = request.GET.get('category', None)
    tag_filter = request.GET.get('tag', None)

    # Get all blogs with filtering
    blogs = Blog.objects.all()

    if category_filter:
        blogs = blogs.filter(category=category_filter)

    if tag_filter:
        blogs = blogs.filter(tags__name=tag_filter)  # Assuming 'tags' is a many-to-many relationship with Blog

    categories = Blog.objects.values('category').annotate(count=Count('category'))
    tags = Blog.tags.most_common()  # Get common tags, this depends on your tags setup
    recent_posts = Blog.objects.order_by('-published_date')[:5]  # Recent posts
    # Pagination
    paginator = Paginator(blogs, 10)  # Show 10 blogs per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)


    return render(request, 'blogs.html', {
        'blogs': blogs,
        'categories': categories,
        'recent_posts': recent_posts,
        'tags': tags
    })



def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    
    # Getting recent blog posts (last 3 published)
    recent_posts = Blog.objects.order_by('-published_date')[:5]
    
    # Getting categories and count of each category
    categories = Blog.objects.values('category').annotate(count=Count('category')).order_by('category')
    
    # Getting tags (adjust this part according to your tag system)
    tags = Blog.tags.most_common()  # Assuming you have a tag manager or a custom tag system
    
    # Breadcrumb data
    breadcrumb = [
        {"name": "Home", "url": "/"},
        {"name": "Blog", "url": "/blog/"},
        {"name": blog.title, "url": "#" }
    ]
    
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
        'breadcrumb': breadcrumb,
        'background_image': blog.image.url if blog.image else None  # Optional background image from blog object
    })

def post_comment(request):
    if request.method == "POST":
        blog_id = request.POST.get("blog_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        content = request.POST.get("content")

        if not all([blog_id, name, email, content]):
            return JsonResponse({"success": False, "error": "All fields are required."})

        try:
            blog = Blog.objects.get(pk=blog_id)
            comment = Comment.objects.create(
                blog=blog,
                name=name,
                email=email,
                content=content,
            )
            return JsonResponse({
                "success": True,
                "comment": {
                    "name": comment.name,
                    "created_date": comment.created_date.strftime("%B %d, %Y %I:%M %p"),
                    "content": comment.content,
                },
            })
        except Blog.DoesNotExist:
            return JsonResponse({"success": False, "error": "Blog not found."})

    return JsonResponse({"success": False, "error": "Invalid request."})


def search_blog(request):
    query = request.GET.get('q', '')
    if query:
        results = Blog.objects.filter(title__icontains=query)
    else:
        results = Blog.objects.none()

    search_results = [
        {
            'title': result.title,
            'url': result.get_absolute_url(),
            'image_url': result.image.url if result.image else '',  # Assuming you have an image field in Blog
        } for result in results
    ]

    return JsonResponse({'results': search_results})
