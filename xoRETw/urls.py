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
    
    url(r'^views/delete_constraint$', views.delete_constraint, name='delete_constraint'),
    url(r'^views/edit_constraint$', views.edit_constraint, name='edit_constraint'),
    
    url(r'^views/get_conditions$', views.get_conditions, name='get_conditions'),
    url(r'^views/get_steps$', views.get_steps, name='get_steps'),
    url(r'^views/get_scenarios$', views.get_scenarios, name='get_scenarios'),

    url(r'^views/delete_permission$', views.delete_permission, name='delete_permission'),
    #url(r'^views/edit_permission$', views.edit_permission, name='edit_permission'),
    
    url(r'^views/delete_step$', views.delete_step, name='delete_step'),
    url(r'^views/delete_scenario$', views.delete_scenario, name='delete_scenario'),
    url(r'^views/delete_task$', views.delete_task, name='delete_task'),
    
    url(r'^views/edit_scenario$', views.edit_scenario, name='edit_scenario'),
    
    

    (r'^accounts/', include('registration.backends.simple.urls')),
)
