from django.conf.urls import patterns, include, url
from django.contrib import admin
from rbac import views
from rbac import api
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xoretw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='accounts/login', permanent=False), name='index'),
    url(r'^views/dashboard$', views.dashboard, name='dashboard'),

  


    # new api
    #url(r'^api/perm_create$', api.perm_create, name='perm_create'),
    
    url(r'^api/exist_role$', api.exist_role, name='exist_role'),
    
    url(r'^api/add_derived_abstract_context_condition_to_objective$', api.add_derived_abstract_context_condition_to_objective, name='add_derived_abstract_context_condition_to_objective'),
    url(r'^api/add_derived_abstract_context_condition_to_obstacle$', api.add_derived_abstract_context_condition_to_obstacle, name='add_derived_abstract_context_condition_to_obstacle'),
    url(r'^api/add_tasks_to_work_profile$', api.add_tasks_to_work_profile, name='add_tasks_to_work_profile'),
    url(r'^api/add_scenarios_to_task$', api.add_scenarios_to_task, name='add_scenarios_to_task'),
    url(r'^api/link_context_constraints_to_perm$', api.link_context_constraints_to_perm, name='link_context_constraints_to_perm'),
    url(r'^api/set_ssd_perm_constraint', api.set_ssd_perm_constraint, name='set_ssd_perm_constraint'),
    url(r'^api/set_ssd_role_constraint', api.set_ssd_role_constraint, name='set_ssd_role_constraint'),
    
    
    # clear
    url(r'^api/clear_derived_condition_list_of_objective$', api.clear_derived_condition_list_of_objective, name='clear_derived_condition_list_of_objective'),
    url(r'^api/clear_derived_condition_list_of_obstacle$', api.clear_derived_condition_list_of_obstacle, name='clear_derived_condition_list_of_obstacle'),
    url(r'^api/clear_task_list_of_work_profile$', api.clear_task_list_of_work_profile, name='clear_task_list_of_work_profile'),
    url(r'^api/clear_scenario_list_of_task$', api.clear_scenario_list_of_task, name='clear_scenario_list_of_task'),
    url(r'^api/unlink_context_constraints_from_perm$', api.unlink_context_constraints_from_perm, name='unlink_context_constraints_from_perm'),
    url(r'^api/unset_ssd_perm_constraint$', api.unset_ssd_perm_constraint, name='unset_ssd_perm_constraint'),
    url(r'^api/unset_ssd_role_constraint$', api.unset_ssd_role_constraint, name='unset_ssd_role_constraint'),
    
    # edit init
    url(r'^api/edit_objective_init$', api.edit_objective_init, name='edit_objective_init'),
    url(r'^api/edit_obstacle_init$', api.edit_obstacle_init, name='edit_obstacle_init'),
    url(r'^api/edit_condition_init$', api.edit_condition_init, name='edit_condition_init'),
    url(r'^api/edit_step_init$', api.edit_step_init, name='edit_step_init'),
    url(r'^api/edit_profile_init$', api.edit_profile_init, name='edit_profile_init'),
    url(r'^api/edit_task_init$', api.edit_task_init, name='edit_task_init'),
    url(r'^api/edit_permcard_init$', api.edit_permcard_init, name='edit_permcard_init'),
    url(r'^api/edit_rolecard_init$', api.edit_rolecard_init, name='edit_rolecard_init'),
    url(r'^api/edit_perm_cc_mgmt_init$', api.edit_perm_cc_mgmt_init, name='edit_perm_cc_mgmt_init'),
    url(r'^api/edit_scenario_init$', api.edit_scenario_init, name='edit_scenario_init'),
    
    # edit save
    url(r'^api/edit_objective_save$', api.edit_objective_save, name='edit_objective_save'),
    url(r'^api/edit_obstacle_save$', api.edit_obstacle_save, name='edit_obstacle_save'),
    url(r'^api/edit_step_save$', api.edit_step_save, name='edit_step_save'),
    url(r'^api/edit_profile_save$', api.edit_profile_save, name='edit_profile_save'),
    url(r'^api/edit_task_save$', api.edit_task_save, name='edit_task_save'),
    url(r'^api/edit_permcard_save$', api.edit_permcard_save, name='edit_permcard_save'),
    url(r'^api/edit_rolecard_save$', api.edit_rolecard_save, name='edit_rolecard_save'),
    url(r'^api/edit_scenario_save$', api.edit_scenario_save, name='edit_scenario_save'),
    
    # create create
    url(r'^api/create_objective_create$', api.create_objective_create, name='create_objective_create'),    
    url(r'^api/create_obstacle_create$', api.create_obstacle_create, name='create_obstacle_create'),
    url(r'^api/create_condition_create$', api.create_condition_create, name='create_condition_create'),
    url(r'^api/create_CC_create$', api.create_CC_create, name='create_CC_create'),
    url(r'^api/create_task_create$', api.create_task_create, name='create_task_create'),
    url(r'^api/create_step_create$', api.create_step_create, name='create_step_create'),
    url(r'^api/create_perm_create$', api.create_perm_create, name='create_perm_create'),
    url(r'^api/create_profile_create$', api.create_profile_create, name='create_profile_create'),
    url(r'^api/create_scenario_create$', api.create_scenario_create, name='create_scenario_create'),
    url(r'^api/create_role_create$', api.create_role_create, name='create_role_create'),
    

    # delete
    url(r'^api/delete_objective$', api.delete_objective, name='delete_objective'),
    url(r'^api/delete_obstacle$', api.delete_obstacle, name='delete_obstacle'),
    url(r'^api/delete_condition$', api.delete_condition, name='delete_condition'),
    url(r'^api/delete_context_constraint$', api.delete_context_constraint, name='delete_context_constraint'),
    url(r'^api/delete_task$', api.delete_task, name='delete_task'),
    url(r'^api/delete_step$', api.delete_step, name='delete_step'),
    url(r'^api/delete_permission$', api.delete_permission, name='delete_permission'),
    url(r'^api/delete_profile$', api.delete_profile, name='delete_profile'),
    url(r'^api/delete_scenario$', api.delete_scenario, name='delete_scenario'),
    url(r'^api/delete_role$', api.delete_role, name='delete_role'),
    
    #url(r'^api/add_derived_abstract_context_condition_to_obstacle$', api.add_derived_abstract_context_condition_to_obstacle, name='add_derived_abstract_context_condition_to_obstacle'),
    url(r'^api/link_condition_to_context_constraint$', api.link_condition_to_context_constraint, name='link_condition_to_context_constraint'),
    url(r'^api/unlink_condition_from_context_constraint$', api.unlink_condition_from_context_constraint, name='unlink_condition_from_context_constraint'),

    # getters
    url(r'^api/get_condition_list$', api.get_condition_list, name='get_condition_list'),
    url(r'^api/get_scenario_list$', api.get_scenario_list, name='get_scenario_list'),
    url(r'^api/get_step_list$', api.get_step_list, name='get_step_list'),
    url(r'^api/get_task_list$', api.get_task_list, name='get_task_list'),
    url(r'^api/get_role_list$', api.get_role_list, name='get_role_list'),
    url(r'^api/get_condition_list$', api.get_condition_list, name='get_condition_list'),
    url(r'^api/get_context_constraint_list$', api.get_context_constraint_list, name='get_context_constraint_list'),
    url(r'^api/get_permission_list$', api.get_permission_list, name='get_permission_list'),
    
    #PRA
    url(r'^api/get_all_directly_assigned_perms$', api.get_all_directly_assigned_perms, name='get_all_directly_assigned_perms'),
    url(r'^api/get_all_transitively_assigned_perms$', api.get_all_transitively_assigned_perms, name='get_all_transitively_assigned_perms'),
    url(r'^api/assign_permission$', api.assign_permission, name='assign_permission'),
    url(r'^api/revoke_permission$', api.revoke_permission, name='revoke_permission'),
    
    
    # for perm
    url(r'^api/get_context_constraints$', api.get_context_constraints, name='get_context_constraints'),
    url(r'^api/get_ssd_perm_constraints$', api.get_ssd_perm_constraints, name='get_ssd_perm_constraints'),
    
    # for role
    url(r'^api/get_direct_ssd_role_constraints$', api.get_direct_ssd_role_constraints, name='get_direct_ssd_role_constraints'),
    url(r'^api/get_transitive_ssd_role_constraints$', api.get_transitive_ssd_role_constraints, name='get_transitive_ssd_role_constraints'),
    url(r'^api/get_inherited_ssd_role_constraints$', api.get_inherited_ssd_role_constraints, name='get_inherited_ssd_role_constraints'),
    
    # RRA
    url(r'^api/add_junior_role_relation$', api.add_junior_role_relation, name='add_junior_role_relation'),
    url(r'^api/remove_junior_role_relation$', api.remove_junior_role_relation, name='remove_junior_role_relation'),
    url(r'^api/add_senior_role_relation$', api.add_senior_role_relation, name='add_senior_role_relation'),
    url(r'^api/remove_senior_role_relation$', api.remove_senior_role_relation, name='remove_senior_role_relation'),
    
    url(r'^api/get_direct_junior_roles$', api.get_direct_junior_roles, name='get_direct_junior_roles'),
    url(r'^api/get_direct_senior_roles$', api.get_direct_senior_roles, name='get_direct_senior_roles'),
    url(r'^api/get_transitive_junior_roles$', api.get_transitive_junior_roles, name='get_transitive_junior_roles'),
    url(r'^api/get_transitive_senior_roles$', api.get_transitive_senior_roles, name='get_transitive_senior_roles'),
    
    
    url(r'^api/get_all_conditions$', api.get_all_conditions, name='get_all_conditions'),
    
    (r'^accounts/', include('registration.backends.simple.urls')),
)

