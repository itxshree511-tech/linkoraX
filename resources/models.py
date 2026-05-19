from django.db import models
import uuid


class ResourceCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    
    icon = models.CharField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resource_categories'
        verbose_name = 'Resource Category'
        verbose_name_plural = 'Resource Categories'
    
    def __str__(self):
        return self.name


class MemberResource(models.Model):
    class ResourceType(models.TextChoices):
        PDF = 'pdf', 'PDF'
        VIDEO = 'video', 'Video'
        ARTICLE = 'article', 'Article'
        LINK = 'link', 'Link'
        DOWNLOAD = 'download', 'Download'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()
    
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    
    file = models.FileField(upload_to='resources/files/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', blank=True, null=True)
    
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'member_resources'
        verbose_name = 'Member Resource'
        verbose_name_plural = 'Member Resources'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
