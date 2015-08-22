from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
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

# constants
CREATE_NEW = 1

OBJECT_TYPE_OBJECTIVE = 1
OBJECT_TYPE_OBSTACLE = 2
OBJECT_TYPE_CONDITION = 3
OBJECT_TYPE_CONTEXT_CONSTRAINT = 4
OBJECT_TYPE_STEP = 5
OBJECT_TYPE_SCENARIO = 6
OBJECT_TYPE_PERMISSION = 7
OBJECT_TYPE_TASK = 8
OBJECT_TYPE_WORK_PROFILE = 9
OBJECT_TYPE_ROLE = 10

PERM_CARDINALITY_CONSTRAINTS = 100
ROLE_CARDINALITY_CONSTRAINTS = 101
PERM_CONTEXT_CONSTRAINTS = 102

def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

def get_perm_context_constraints(request):

    user = request.user
    if request.method == 'GET':        
        perm_id = request.GET.get('perm_id', None)
        
        if perm_id:
            perm = Permission.objects.get(id=perm_id, user=user)

    data = {}
    data['available_context_constraints'] = []
    data['perm_context_constraints'] = []

    # get all available context constraints
    context_constraints = ContextConstraint.objects.filter(user=user)
    
    for i in context_constraints:
        context_constraint = {}
        context_constraint['name'] = i.name
        context_constraint['id'] = i.id
        data['available_context_constraints'].append(context_constraint)

    for context_constraint in perm.context_constraints.all():
        data['perm_context_constraints'].append(context_constraint.name)
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_perm_cardinality_constraints(request):

    user = request.user
    print 'A1'
    if request.method == 'GET':        
        print 'A2'
        perm_id = request.GET.get('perm_id', None)
        print 'A3'
        if perm_id:
            print 'A4'
            perm = Permission.objects.get(id=perm_id, user=user)

    print 'A5'
    data = {}
    
    data['mincardinality'] = perm.mincardinality
    data['maxcardinality'] = perm.maxcardinality
    print 'A6'
    print 'mincardinality ', perm.mincardinality
    print 'maxcardinality ', perm.maxcardinality
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def get_role_cardinality_constraints(request):

    user = request.user
    print 'A1'
    if request.method == 'GET':        
        print 'A2'
        role_id = request.GET.get('role_id', None)
        print 'A3'
        if role_id:
            print 'A4'
            role = Role.objects.get(id=role_id, user=user)

    print 'A5'
    data = {}
    
    data['mincardinality'] = role.mincardinality
    data['maxcardinality'] = role.maxcardinality
    print 'A6'
    print 'mincardinality ', role.mincardinality
    print 'maxcardinality ', role.maxcardinality
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
                
# context constraint get all available conditions 
def get_conditions(request):
    user = request.user
    print 'user - get conditions ', user
    
    # get name, type and conditions
    data = {}
    data['conditions'] = []
    
    conditions = Condition.objects.filter(user=user).filter(is_abstract=False)
    print 'conditions/length ', len(conditions)
    
    for i in conditions:
        condition = {}
        condition['name'] = i.name
        condition['id'] = i.id
        data['conditions'].append(condition)
    
    json_data = json.dumps(data)
    print 'json_data ', json_data
    return HttpResponse(json_data, content_type='application/json')

# get all available steps 
def get_steps(request):
    user = request.user
    print 'a'
    # get name, type and conditions
    data = {}
    data['steps'] = []
    print 'b'
    steps = Step.objects.all().filter(user=user)
    print 'c'
    for i in steps:
        print 'get steps - ', i.name
        step = {}
        step['name'] = i.name
        step['id'] = i.id
        data['steps'].append(step)
    
    json_data = json.dumps(data)
    print 'json_data ', json_data
    return HttpResponse(json_data, content_type='application/json')

# get all available scenarios
def get_scenarios(request):
    user = request.user

    # get name, type and conditions
    data = {}
    data['scenarios'] = []
    
    scenarios = Scenario.objects.all().filter(user=user)
    
    for i in scenarios:
        print 'get scenario - ', i.name
        scenario = {}
        scenario['name'] = i.name
        scenario['id'] = i.id
        data['scenarios'].append(scenario)
    
    json_data = json.dumps(data)
    print 'json_data ', json_data
    return HttpResponse(json_data, content_type='application/json')

# get all available roles 
def get_roles(request):
    user = request.user
    print 'user - get roles ', user
    
    # get name, type and conditions
    data = {}
    data['roles'] = []
    
    roles = Role.objects.filter(user=user)
    print 'roles/length ', len(roles)
    
    for i in roles:
        role = {}
        role['name'] = i.name
        role['id'] = i.id
        data['roles'].append(role)
    
    json_data = json.dumps(data)
    print 'json_data ', json_data
    return HttpResponse(json_data, content_type='application/json')
    
@login_required
def dashboard(request):
    user = request.user
    object_type = request.GET.get('object_type', 1) # default to Objective tab
    print 'object_type is ', object_type
    
    object_type = int(object_type)
    
    print 'dashboard'
    print 'request.method ', request.method
    # if this is a POST request we need to process the data
    if request.method == 'POST':
        
        object_type = request.POST.get('object_type', None)
        object_type = int(object_type)
        print 'hellow object type is ', object_type
        
                                
    # if a GET (or any other method)
    else:    
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objectives = Objective.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'objectives':objectives}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_OBSTACLE:
            obstacles = Obstacle.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'obstacles':obstacles}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_CONDITION:
            conditions = Condition.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'conditions':conditions}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_CONTEXT_CONSTRAINT:
            constraints = ContextConstraint.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'constraints':constraints}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_PERMISSION:
            permissions = Permission.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'permissions':permissions}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_TASK:
            tasks = Task.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'tasks':tasks}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_STEP:
            steps = Step.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'steps':steps}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_SCENARIO:
            scenarios = Scenario.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'scenarios':scenarios}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_WORK_PROFILE:
            profiles = WorkProfile.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'profiles':profiles}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_ROLE:
            roles = Role.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'roles':roles}, context_instance=RequestContext(request))

    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))

def delete_objective(request):
    user = request.user

    data = {}
        
    if request.method == 'POST':      
        objective_id = request.POST.get('objective_id', None)
        
        if objective_id:
            o = Objective.objects.get(id=objective_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['objective_id'] = objective_id
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def edit_objective(request):
    user = request.user
    # if this is a POST request we need to process the data
    if request.method == 'GET':        
        objective_id = request.GET.get('objective_id', None)
        if objective_id:
            objective = Objective.objects.get(id=objective_id, user=user)

    # get name, type and conditions
    data = {}
    #data['objective_id'] = objective.name
    data['name'] = objective.name
    data['type'] = objective.type
    data['conditions'] = []

    for condition in objective.conditions.all():
        data['conditions'].append(condition.name)
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_obstacle(request):
    user = request.user

    data = {}
    if request.method == 'POST':      
        obstacle_id = request.POST.get('obstacle_id', None)
        if obstacle_id:
            o = Obstacle.objects.get(id=obstacle_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['obstacle_id'] = obstacle_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def edit_obstacle(request):
    user = request.user
    # if this is a POST request we need to process the data
    if request.method == 'GET':   
        obstacle_id = request.GET.get('obstacle_id', None)
        
        if obstacle_id:
            obstacle = Obstacle.objects.get(id=obstacle_id, user=user)

    # get name, type and conditions
    data = {}
    
    data['name'] = obstacle.name
    data['type'] = obstacle.type
    data['conditions'] = []
    for condition in obstacle.conditions.all():
        data['conditions'].append(condition.name)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_condition(request):
    user = request.user

    data = {}
    if request.method == 'POST':      
        condition_id = request.POST.get('condition_id', None)
        if condition_id:
            o = Condition.objects.get(id=condition_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['condition_id'] = condition_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_condition(request):
    user = request.user
    # if this is a POST request we need to process the data
    if request.method == 'GET':   
        condition_id = request.GET.get('condition_id', None)
        
        if condition_id:
            condition = Condition.objects.get(id=condition_id, user=user)
    # get name, type and conditions
    data = {}
    
    data['name'] = condition.name
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_constraint(request):
    user = request.user

    data = {}
        
    if request.method == 'POST':      
        constraint_id = request.POST.get('constraint_id', None)
        
        if constraint_id:
            o = ContextConstraint.objects.get(id=constraint_id, user=user)
            o.delete()
            
            data['deleted'] = 'true'
            data['objective_id'] = constraint_id
            
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_constraint(request):
    user = request.user
    
    if request.method == 'GET':        
        constraint_id = request.GET.get('constraint_id', None)
        
        if constraint_id:
            constraint = ContextConstraint.objects.get(id=constraint_id, user=user)

    # get name, type and conditions
    data = {}
    data['name'] = constraint.name
    data['conditions'] = []

    for condition in constraint.conditions.all():
        data['conditions'].append(condition.name)
    
    print "constraint.conditions - data ", data
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_task(request):
    user = request.user
    
    if request.method == 'GET':        
        task_id = request.GET.get('task_id', None)
        
        if task_id:
            task = Task.objects.get(id=task_id, user=user)

    # get name, type and conditions
    print 'task.name  is  ', task.name
    data = {}
    data['name'] = task.name
    data['scenarios'] = []

    for scenario in task.scenarios.all():
        data['scenarios'].append(scenario.name)
    
    print "task.scenarios - data ", data
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def edit_scenario(request):
    user = request.user
    
    if request.method == 'GET':        
        scenario_id = request.GET.get('scenario_id', None)
        
        if scenario_id:
            scenario = Scenario.objects.get(id=scenario_id, user=user)

    # get name, type and steps
    data = {}
    data['name'] = scenario.name
    data['graph_dot'] = scenario.graph
    data['steps'] = []

    steps = Step.objects.all().filter(user=user)
    for i in steps:
        step = {}
        step['name'] = i.name
        step['id'] = i.id
        data['steps'].append(step)

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')



def delete_step(request):
    user = request.user
    data = {}
    if request.method == 'POST':      
        step_id = request.POST.get('step_id', None)
        if step_id:
            o = Step.objects.get(id=step_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['step_id'] = step_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_scenario(request):
    user = request.user
    data = {}
    if request.method == 'POST':      
        scenario_id = request.POST.get('scenario_id', None)
        if scenario_id:
            o = Scenario.objects.get(id=scenario_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['scenario_id'] = scenario_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_task(request):
    print 'a'
    user = request.user
    data = {}
    print 'b'
    if request.method == 'POST':      
        print 'c'
        task_id = request.POST.get('task_id', None)
        if task_id:
            print 'd'
            o = Task.objects.get(id=task_id, user=user)
            o.delete()
            print 'e'
            data['deleted'] = 'true'
            data['task_id'] = task_id
            print 'f'
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    
def delete_role(request):
    user = request.user
    data = {}
    if request.method == 'POST':      
        role_id = request.POST.get('role_id', None)
        if role_id:
            o = Role.objects.get(id=role_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['role_id'] = role_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def delete_work_profile(request):
    user = request.user
    data = {}
    if request.method == 'POST':      
        work_profile_id = request.POST.get('work_profile_id', None)
        if work_profile_id:
            o = WorkProfile.objects.get(id=work_profile_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['work_profile_id'] = work_profile_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

def exists_role(request):
    user = request.user
    role_name = request.GET.get('role_name', None)
    
    roles = Role.objects.filter(user=user)
    
    data = {}
    print 'role_name is ', role_name
    data['exists'] = False 
    for role in roles:
        print 'db role.name is ', role.name
        
        if role_name == role.name:
            print 'True rolename exists'
            data['exists'] = True
        
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
    
