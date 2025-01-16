from django.contrib import admin
from django.contrib import admin
from .models import Project,Service,ServiceImage,ProjectImage,Blog,Comment,Testimonial,Client

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'client', 'date', 'category')
    prepopulated_fields = {'slug': ('title',)}

class ServiceImageInline(admin.TabularInline):  # Inline editing for images
    model = ServiceImage
    extra = 1  # Number of empty image fields to show by default


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline]  # Attach the inline model to Service admin


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'category', 'tags')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'created_date')
    search_fields = ('name', 'email', 'content')
    list_filter = ('created_date',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('client_name', 'review')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)