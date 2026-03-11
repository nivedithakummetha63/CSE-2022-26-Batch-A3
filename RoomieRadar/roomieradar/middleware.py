from django.shortcuts import redirect
from django.urls import reverse


class AdminRedirectMiddleware:
    """
    Middleware to redirect superuser to admin panel and restrict access.
    Only superusers can access admin panel.
    Regular users and staff cannot access admin panel.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip middleware for static/media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        
        # Skip for logout and activation
        if request.path in ['/accounts/logout/', '/accounts/activate/']:
            return self.get_response(request)
        
        # Skip for login and register pages
        if request.path in ['/accounts/login/', '/accounts/register/']:
            return self.get_response(request)
        
        # If user is authenticated
        if request.user.is_authenticated:
            # Superuser only (admin access)
            if request.user.is_superuser:
                # Allow access to admin panel
                if request.path.startswith('/admin/'):
                    return self.get_response(request)
                
                # Redirect superuser from any other page to admin panel
                # Except index page (allow them to see landing page)
                if request.path != '/':
                    return redirect('/admin/')
            
            # Regular users and staff (no admin access)
            else:
                # Block access to admin panel for everyone except superuser
                if request.path.startswith('/admin/'):
                    return redirect('/app/')
        
        # Continue with normal request processing
        response = self.get_response(request)
        return response
