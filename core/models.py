from django.db import models
from django.db import models
from taggit.managers import TaggableManager  # For tag handling
from django.urls import reverse

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('playgrounds', 'Playgrounds'),
        ('schools', 'Schools'),
        ('sports', 'Sports Facilities'),
    ]

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.CharField(max_length=200)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:project_detail', args=[self.slug])

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.title}"
    
class Service(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')  # One-to-many relationship
    image = models.ImageField(upload_to='services/')  # Image field for storing files
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for the image

    def __str__(self):
        return f"Image for {self.service.name}"
    

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # Single category
    tags = TaggableManager()  # For multiple tags

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.blog.title}'


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, f'{i} Stars') for i in range(1, 6)])  # Ratings from 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name
    


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="The name of the client.")
    logo = models.ImageField(upload_to='clients/logos/', help_text="Upload the client's logo image.")
    website = models.URLField(blank=True, null=True, help_text="Optional: Add the client's website.")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']

    def __str__(self):
        return self.name