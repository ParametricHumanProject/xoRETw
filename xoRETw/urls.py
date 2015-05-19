from django.conf.urls import patterns, include, url
from django.contrib import admin
from rbac import views
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xoretw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='accounts/login', permanent=False), name='index'),
    url(r'^views/dashboard$', views.dashboard, name='dashboard'),
    (r'^accounts/', include('registration.backends.simple.urls')),
)
