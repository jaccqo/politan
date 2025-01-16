from .models import Service,Blog,Project

def services_context(request):
    services = Service.objects.all()
    return {
        'services': services
    }

def footer_context(request):
    recent_posts = Blog.objects.order_by('-published_date')[:4]
    recent_projects = Project.objects.order_by('-id')[:6]
    return {
        'latest_posts': recent_posts,
        'latest_projects': recent_projects,
    }