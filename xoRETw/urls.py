from django.conf.urls import patterns, include, url
from django.contrib import admin
from rbac import views
from rbac import views
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xoretw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='accounts/login', permanent=False), name='index'),
    url(r'^views/dashboard$', views.dashboard, name='dashboard'),

    url(r'^views/delete_objective$', views.delete_objective, name='delete_objective'),
    url(r'^views/edit_objective$', views.edit_objective, name='edit_objective'),

    url(r'^views/delete_obstacle$', views.delete_obstacle, name='delete_obstacle'),
    url(r'^views/edit_obstacle$', views.edit_obstacle, name='edit_obstacle'),

    url(r'^views/delete_condition$', views.delete_condition, name='delete_condition'),
    url(r'^views/edit_condition$', views.edit_condition, name='edit_condition'),

    #url(r'^views/delete_permission$', views.delete_permission, name='delete_permission'),
    #url(r'^views/edit_permission$', views.edit_permission, name='edit_permission'),


    (r'^accounts/', include('registration.backends.simple.urls')),
)
