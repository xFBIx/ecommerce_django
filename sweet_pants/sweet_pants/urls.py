"""
URL configuration for sweet_pants project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from users.decorators import unauthenticated_user

urlpatterns = [
    path("ecommerce/accounts/", include("allauth.urls")),
    path("ecommerce/admin/", admin.site.urls),
    path("ecommerce/", include("mainpage.urls")),
    path("ecommerce/purpose/", user_views.purpose, name="purpose"),
    # path('ecommerce/register/' , user_views.register, name='register'),
    # path('ecommerce/login/', unauthenticated_user(auth_views.LoginView.as_view(template_name='users/login.html')), name='login'),
    # path('ecommerce/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path("ecommerce/edit-profile/", user_views.edit_profile, name="edit-profile"),
    path("ecommerce/profile/", user_views.profile, name="profile"),
    path(
        "ecommerce/profile/generate-coupon/",
        user_views.generate_coupon,
        name="generate-coupon",
    ),
    path(
        "ecommerce/profile/remove-coupon/",
        user_views.remove_coupon,
        name="remove-coupon",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
