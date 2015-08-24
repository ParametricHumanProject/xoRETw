from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

import sys
import json

from .models import Objective
from .models import Obstacle
from .models import Condition
from .models import Step
from .models import Scenario
from .models import Task
from .models import WorkProfile
from .models import ContextConstraint
from .models import Role
from .models import Permission

import Manager

def exist_role(request):
    user = request.user
    name = request.GET.get('name', None)
    data = {}
    error_message = ''
    try:
        data['exists'] = Manager.existRole(name, user)
        
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    
    
def edit_scenario_init(request):
    user = request.user
    
    data = {}
    
    if request.method == 'GET':        
        name = request.GET.get('name', None)
        if name:
            scenario = Scenario.objects.get(name=name, user=user)
            data['graph_dot'] = scenario.graph
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    
def edit_objective_init(request):
    user = request.user
    objective = None
    if request.method == 'GET':        
        objective_name = request.GET.get('objective_name', None)
        if objective_name:
            objective = Objective.objects.get(name=objective_name, user=user)
    
    data = {}
    data['id'] = objective.id
    data['type'] = objective.type
    data['abstract_context_condition_list'] = []

    for abstract_context_condition in objective.abstract_context_conditions.all():
        data['abstract_context_condition_list'].append(abstract_context_condition.name)
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def edit_task_save(request):
    user = request.user

    name = request.POST.get('name', None)
    obj = Task.objects.get(name=name, user=user)
    
    obj.name = name
    obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_profile_save(request):
    user = request.user

    name = request.POST.get('name', None)
    obj = WorkProfile.objects.get(name=name, user=user)
    
    obj.name = name
    obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_objective_save(request):
    user = request.user

    objective_id = request.POST.get('id', None)
    objective_name = request.POST.get('name', None)
    objective_type = request.POST.get('type', None)
    objective = Objective.objects.get(id=objective_id, user=user)
    
    objective.name = objective_name
    objective.type = objective_type
    objective.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_scenario_save(request):
    user = request.user
    
    name = request.POST.get('name', None)
    graph_dot = request.POST.get('graph_dot', None)
    scenario_id = request.POST.get('id', None)
    
    scenario_obj = Scenario.objects.get(name=scenario_id, user=user)
    
    scenario_obj.name = name
    scenario_obj.graph = graph_dot
    scenario_obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_role_create(request):
    user = request.user
    
    name = request.POST.get('name', None)
    junior = request.POST.getlist('junior[]', None)
    senior = request.POST.getlist('senior[]', None)

    data = {}
    error_message = ''
    try:
        success = Manager.createRole(name, junior, senior, user)
        
        if success:
            data['success'] = str(success).lower()
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except Exception as e:
        error_message = str(e)
        print 'ERROR - ', error_message
        data['success'] = str(False).lower()
        data['error_message'] = error_message
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_objective_create(request):
    user = request.user
    objective_name = request.POST.get('name', None)
    objective_type = request.POST.get('type', None)

    data = {}
    error_message = ''
    try:
        success = Manager.createObjective(objective_name, objective_type, user)

        if success:
            data['success'] = str(success).lower()
            data['objective_name'] = objective_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def set_ssd_role_constraint(request):
    print 'set_ssd_role_constraint'
    user = request.user
    role = request.POST.get('role', None)
    mutlexcl = request.POST.get('mutlexcl', None)

    print request
    print 'role is ', role
    print 'mutlexcl is ', mutlexcl
    
    data = {}
    error_message = ''
    try:
        success = Manager.setSSDRoleConstraint(role, mutlexcl, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def set_ssd_perm_constraint(request):
    print 'set_ssd_perm_constraint'
    user = request.user
    perm = request.POST.get('perm', None)
    mutlexcl = request.POST.get('mutlexcl', None)
    
    data = {}
    error_message = ''
    try:
        print '1'
        success = Manager.setSSDPermConstraint(perm, mutlexcl, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def link_context_constraints_to_perm(request):
    user = request.user
    ccs = request.POST.getlist('ccs[]', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.linkContextConstraintsToPerm(ccs, name, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def add_scenarios_to_task(request):
    user = request.user
    scenarios = request.POST.getlist('scenarios[]', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.addScenariosToTask(scenarios, name, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def add_tasks_to_work_profile(request):
    user = request.user
    tasks = request.POST.getlist('tasks[]', None)
    #tasks = request.POST.get('tasks', None)
    name = request.POST.get('name', None)

    print 'tasks are ', tasks
    data = {}
    error_message = ''
    try:
        success = Manager.addTasksToWorkProfile(tasks, name, user)
        
        if success:
            data['success'] = str(success).lower()
            #data['objective_name'] = name

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def add_derived_abstract_context_condition_to_objective(request):
    user = request.user
    abstract_context_condition = request.POST.get('abstract_context_condition', None)
    objective_name = request.POST.get('objective_name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.addDerivedAbstractContextConditionToObjective(abstract_context_condition, objective_name, user)
        if success:
            data['success'] = str(success).lower()
            data['objective_name'] = objective_name

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_objective(request):    

    user = request.user
    objective_name = request.POST.get('name', None)

    Manager.deleteObjective(objective_name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def unset_ssd_role_constraint(request):
    print 'unset_ssd_role_constraint'
    
    user = request.user
    role = request.POST.get('role', None)
    mutlexcl = request.POST.get('mutlexcl', None)
    
    print 'role is ', role
    print 'mutlexcl is ', mutlexcl

    #delete the mutual exclusion constraint from both roles
    Manager.unsetSSDRoleConstraint(role, mutlexcl, user)
    Manager.unsetSSDRoleConstraint(mutlexcl, role, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def unset_ssd_perm_constraint(request):
    user = request.user
    perm = request.POST.get('perm', None)
    mutlexcl = request.POST.get('mutlexcl', None)

    Manager.unsetSSDPermConstraint(perm, mutlexcl, user)
    Manager.unsetSSDPermConstraint(mutlexcl, perm, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def unlink_context_constraints_from_perm(request):
    user = request.user
    name = request.POST.get('name', None)

    Manager.unlinkContextConstraintsFromPerm(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def clear_scenario_list_of_task(request):
    user = request.user
    name = request.POST.get('name', None)

    Manager.clearScenarioListOfTask(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def clear_task_list_of_work_profile(request):
    user = request.user
    name = request.POST.get('name', None)

    Manager.clearTaskListOfWorkProfile(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def clear_derived_condition_list_of_objective(request):
    user = request.user
    objective_name = request.POST.get('name', None)

    Manager.clearDerivedConditionListOfObjective(objective_name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')



#============================

def edit_obstacle_init(request):
    user = request.user
    obstacle = None
    if request.method == 'GET':        
        obstacle_name = request.GET.get('name', None)
        if obstacle_name:
            obstacle = Obstacle.objects.get(name=obstacle_name, user=user)
    
    data = {}
    data['id'] = obstacle.id
    data['type'] = obstacle.type
    data['abstract_context_condition_list'] = []
    for abstract_context_condition in obstacle.abstract_context_conditions.all():
        data['abstract_context_condition_list'].append(abstract_context_condition.name)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_obstacle_save(request):
    user = request.user

    id = request.POST.get('id', None)
    name = request.POST.get('name', None)
    type = request.POST.get('type', None)
    obstacle = Obstacle.objects.get(id=id, user=user)
    
    obstacle.name = name
    obstacle.type = type
    obstacle.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    
def edit_step_save(request):
    user = request.user

    name = request.POST.get('name', None)
    actor = request.POST.get('actor', None)
    action = request.POST.get('action', None)
    target = request.POST.get('target', None)
    
    obj = Step.objects.get(name=name, user=user)
    
    name = actor + '_' + action + '_' + target
    
    obj.name = name
    obj.actor = actor
    obj.action = action
    obj.target = target
    obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_obstacle_create(request):
    user = request.user
    name = request.POST.get('name', None)
    type = request.POST.get('type', None)

    data = {}
    error_message = ''
    try:
        success = Manager.createObstacle(name, type, user)

        if success:

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def add_derived_abstract_context_condition_to_obstacle(request):
    user = request.user
    abstract_context_condition = request.POST.get('abstract_context_condition', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.addDerivedAbstractContextConditionToObstacle(abstract_context_condition, name, user)
        if success:

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_obstacle(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteObstacle(name, user)

    data = {}
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def clear_derived_condition_list_of_obstacle(request):
    user = request.user
    name = request.POST.get('name', None)

    Manager.clearDerivedConditionListOfObstacle(name, user)

    data = {}
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')    


#============================


def create_condition_create(request):
    
    user = request.user
    name = request.POST.get('name', None)
    
    data = {}
    error_message = ''
    try:
        
        success = Manager.createCondition(name, user)

        if success:
            
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_condition(request):    

    user = request.user
    condition_name = request.POST.get('name', None)

    Manager.deleteCondition(condition_name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_condition_init(request):
    user = request.user
    condition = None
    if request.method == 'GET':        
        objective_name = request.GET.get('name', None)
        if objective_name:
            objective = Objective.objects.get(name=objective_name, user=user)
    
    data = {}
    data['id'] = objective.id
    data['type'] = objective.type
    data['abstract_context_condition_list'] = []

    for abstract_context_condition in objective.abstract_context_conditions.all():
        data['abstract_context_condition_list'].append(abstract_context_condition.name)
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def create_CC_create(request):
    user = request.user
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.createContextConstraint(name, user)
        if success:
            data['success'] = str(success).lower()
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_task_create(request):
    user = request.user
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.createTask(name, user)

        if success:
            data['success'] = str(success).lower()
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def delete_context_constraint(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteContextConstraint(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_task(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteTask(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_step(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteStep(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def link_condition_to_context_constraint(request):
    user = request.user
    condition = request.POST.get('condition', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.linkConditionToContextConstraint(condition, name, user)
        if success:

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def unlink_condition_from_context_constraint(request):
    user = request.user
    condition = request.POST.get('condition', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.unlinkConditionFromContextConstraint(condition, name, user)
        if success:

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    createRole
def add_derived_abstract_context_condition_to_obstacle(request):
    user = request.user
    abstract_context_condition = request.POST.get('abstract_context_condition', None)
    name = request.POST.get('name', None)

    data = {}
    error_message = ''
    try:
        success = Manager.addDerivedAbstractContextConditionToObstacle(abstract_context_condition, name, user)
        if success:

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_step_create(request):
    
    user = request.user
    actor = request.POST.get('actor', None)
    action = request.POST.get('action', None)
    target = request.POST.get('target', None)
    
    data = {}
    error_message = ''
    try:
        name, success = Manager.createStep(actor, action, target, user)
        
        if success:
            data['success'] = str(success).lower()
            data['name'] = name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def edit_task_init(request):
    user = request.user

    task = None
    if request.method == 'GET':        
        name = request.GET.get('name', None)            
        task = Task.objects.get(name=name, user=user)
    
    data = {}
    data['scenarios'] = []
    
    for scenario in task.scenarios.all():
        data['scenarios'].append(scenario.name)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_profile_init(request):
    user = request.user

    profile = None
    if request.method == 'GET':        
        name = request.GET.get('name', None)            
        profile = WorkProfile.objects.get(name=name, user=user)
    
    data = {}
    data['tasks'] = []
    
    for task in profile.tasks.all():
        data['tasks'].append(task.name)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_step_init(request):
    user = request.user
    
    obj = None
    
    if request.method == 'GET':        
        name = request.GET.get('name', None)

        if name:
            obj = Step.objects.get(name=name, user=user)
    
    data = {}
    data['actor'] = obj.actor
    data['action'] = obj.action
    data['target'] = obj.target
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_rolecard_init(request):
    user = request.user
    name = request.GET.get('name', None)
    data = {}
    
    obj = None
    obj = Role.objects.get(name=name, user=user)
    
    data['mincardinality'] = obj.mincardinality
    data['maxcardinality'] = obj.maxcardinality
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_permcard_init(request):
    user = request.user
    
    obj = None
    
    if request.method == 'GET':        
        name = request.GET.get('name', None)

        if name:
            obj = Permission.objects.get(name=name, user=user)
    
    data = {}
    data['mincardinality'] = obj.mincardinality
    data['maxcardinality'] = obj.maxcardinality
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_perm_cc_mgmt_init(request):
    user = request.user

    perm = None
    if request.method == 'GET':        
        name = request.GET.get('name', None)            
        perm = Permission.objects.get(name=name, user=user)
    
    data = {}
    data['ccs'] = []
    
    for cc in perm.context_constraints.all():
        data['ccs'].append(cc.name)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

#=======================================================================
# getters
#=======================================================================

def get_permission_list(request):
    print '11'
    user = request.user
    perm_list = Manager.getPermissionList(user)
    print '22'
    data = {}
    data['perm_list'] = []
    for perm in perm_list:
        data['perm_list'].append(perm.name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_context_constraint_list(request):
    user = request.user
    cclist = Manager.getContextConstraintList(user)
    data = {}
    data['cclist'] = []
    for cc in cclist:
        data['cclist'].append(cc.name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_condition_list(request):
    user = request.user
    condition_list = Manager.getConditionList(user)
    data = {}
    data['condition_list'] = []
    for condition in condition_list:
        data['condition_list'].append(condition.name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def get_task_list(request):
    print 'get_task_list - api'
    user = request.user
    print 'a'
    task_list = Manager.getTaskList(user)
    print 'b'
    data = {}
    data['task_list'] = []

    for task in task_list:
        print 'c'
        data['task_list'].append(task.name)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_scenario_list(request):
    user = request.user
    scenario_list = Manager.getScenarioList(user)
    data = {}
    data['scenario_list'] = []
    for scenario in scenario_list:
        data['scenario_list'].append(scenario.name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_step_list(request):
    user = request.user
    step_list = Manager.getStepList(user)

    data = {}
    data['step_list'] = []

    for step in step_list:
        data['step_list'].append(step.name)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_role_list(request):
    user = request.user
    role_list = Manager.getRoleList(user)

    data = {}
    data['role_list'] = []

    for role in role_list:
        data['role_list'].append(role)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_all_conditions(request):
    print 'A1'
    user = request.user
    name = request.GET.get('name', None)
    condition_list = Manager.getAllConditions(name, user)
    
    print 'A4'    
    data = {}
    data['condition_list'] = []
    print 'A5'
    print 'condition_list is ', condition_list
    for condition in condition_list:
        print 'A6'
        data['condition_list'].append(condition.name)
    print 'A7'    
    json_data = json.dumps(data)
    print 'A8'
    return HttpResponse(json_data, content_type='application/json')


def get_ssd_perm_constraints(request):
    user = request.user
    name = request.GET.get('name', None)
    dmeps = Manager.getSSDPermConstraints(name, user)
    
    data = {}
    data['dmeps'] = []
    for dmep in dmeps:
        data['dmeps'].append(dmep)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_context_constraints(request):
    user = request.user
    name = request.GET.get('name', None)
    ccs = Manager.getContextConstraints(name, user)

    data = {}
    data['ccs'] = []
    for cc in ccs:
        data['ccs'].append(cc.name)
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_scenario_create(request):
                                     
    user = request.user
    
    name = request.POST.get('name', None)
    graph_dot = request.POST.get('graph_dot', None)
    
    data = {}
    error_message = ''
    try:
        success = Manager.createScenario(name, graph_dot, user)

        if success:
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def create_profile_create(request):
    user = request.user
    
    name = request.POST.get('name', None)
    
    data = {}
    error_message = ''
    try:
        success = Manager.createProfile(name, user)

        if success:
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def create_perm_create(request):
    user = request.user
    
    perm_operation = request.POST.get('opentry', None)
    perm_object = request.POST.get('obentry', None)
    
    data = {}
    error_message = ''
    try:
        success = Manager.createPermission(perm_operation, perm_object, user)

        if success:
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
    
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_role(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteRole(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_scenario(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteScenario(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_profile(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deleteProfile(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_permission(request):    

    user = request.user
    name = request.POST.get('name', None)

    Manager.deletePermission(name, user)

    data = {}
    data['success'] = str(True).lower()
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_rolecard_save(request):
    user = request.user
        
    name = request.POST.get('name', None)
    min_card = request.POST.get('min', None)
    max_card = request.POST.get('max', None)
        
    obj = Role.objects.get(name=name, user=user)
    
    obj.mincardinality = min_card
    obj.maxcardinality = max_card
    
    obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_permcard_save(request):
    user = request.user
        
    name = request.POST.get('name', None)
    min_card = request.POST.get('min', None)
    max_card = request.POST.get('max', None)
    obj = Permission.objects.get(name=name, user=user)
    
    obj.mincardinality = min_card
    obj.maxcardinality = max_card
    
    obj.save()
    
    data = {}
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def get_all_directly_assigned_perms(request):
    user = request.user
    name = request.GET.get('name', None)

    dp = Manager.getAllDirectlyAssignedPerms(name, user)
    
    data = {}
    data['dp'] = []

    for i in dp:
        data['dp'].append(i)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_all_transitively_assigned_perms(request):
    user = request.user
    name = request.GET.get('name', None)

    tp = Manager.getAllTransitivelyAssignedPerms(name, user)
    
    data = {}
    data['tp'] = []

    for i in tp:
        data['tp'].append(i)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_direct_ssd_role_constraints(request):
    user = request.user
    name = request.GET.get('name', None)

    dmer = Manager.getDirectSSDRoleConstraints(name, user)
    
    data = {}
    data['dmer'] = []

    for i in dmer:
        data['dmer'].append(i)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    

def get_transitive_ssd_role_constraints(request):
    user = request.user
    name = request.GET.get('name', None)

    tssdrc = Manager.getTransitiveSSDRoleConstraints(name, user)
    
    data = {}
    data['tssdrc'] = []

    for i in tssdrc:
        data['tssdrc'].append(i)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_inherited_ssd_role_constraints(request):
    user = request.user
    name = request.GET.get('name', None)

    issdc = Manager.getInheritedSSDRoleConstraints(name, user)
    
    data = {}
    data['issdc'] = []

    for i in issdc:
        data['issdc'].append(i)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    

def assign_permission(request):
    print 'assign_permission'
    
    user = request.user
    role_name = request.POST.get('role', None)
    perm_name = request.POST.get('perm', None)

    print 'role_name is ', role_name
    print 'perm_name is ', perm_name
    
    data = {}
    error_message = ''
    try:
        success = Manager.permRoleAssign(perm_name, role_name, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    

def revoke_permission(request):
    print 'revoke_permission'
    
    user = request.user
    role_name = request.POST.get('role', None)
    perm_name = request.POST.get('perm', None)

    print 'role_name is ', role_name
    print 'perm_name is ', perm_name
    
    data = {}
    error_message = ''
    try:
        success = Manager.permRoleRevoke(perm_name, role_name, user)
        
        if success:
            data['success'] = str(success).lower()

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    except:
        error_message = sys.exc_info()[1]
        print "Error: %s" % error_message
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
