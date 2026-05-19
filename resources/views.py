from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResourceCategory, MemberResource


@login_required
def resources_view(request):
    resources = MemberResource.objects.all().select_related('category')
    categories = ResourceCategory.objects.all()
    
    context = {
        'resources': resources,
        'categories': categories,
    }
    return render(request, 'dashboard/resources.html', context)


@login_required
def resources_by_category(request, category_slug):
    category = get_object_or_404(ResourceCategory, slug=category_slug)
    resources = category.resources.all()
    
    context = {
        'category': category,
        'resources': resources,
    }
    return render(request, 'dashboard/resources_category.html', context)


@login_required
def resource_detail(request, resource_slug):
    resource = get_object_or_404(MemberResource, slug=resource_slug)
    
    # Increment view count
    resource.view_count += 1
    resource.save()
    
    context = {
        'resource': resource,
    }
    return render(request, 'dashboard/resource_detail.html', context)
