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
OBJECT_TYPE_PERMISSION = 7
OBJECT_TYPE_TASK = 8


OBJECT_TYPE_ROLE = 55
OBJECT_TYPE_STEP = 65
OBJECT_TYPE_SCENARIO = 75
#OBJECT_TYPE_CONTEXTCONSTRAINT = 9


def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

# get all available conditions 
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

@login_required
def dashboard(request):
    user = request.user
    object_type = request.GET.get('object_type', 1) # default to Objective tab
    object_type = int(object_type)
    
    print '--------object_type  is ', object_type
    

    # if this is a POST request we need to process the data
    if request.method == 'POST':
        
        object_type = request.POST.get('object_type', None)
        object_type = int(object_type)
        print 'object type is ', object_type
        
        # TODO: handle each object_type       
        
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objective_id = request.POST.get('id', None)
            objective_name = request.POST.get('name', None)
            objective_type = request.POST.get('type', None)
            condition_names = request.POST.getlist('conditions[]', None)
            mode = request.POST.get('mode', None)
            mode = int(mode)
            if objective_id != '':
                objective_id = int(objective_id)
            
            objective_created = False
            if mode == CREATE_NEW:
                
                # use objective name as an exact lookup
                objective, objective_created = Objective.objects.get_or_create(name__exact=objective_name, user__exact=user, defaults={'name':objective_name,'type': objective_type, 'user':user})
                if objective_created:
                    objective.save()
                                    
                for condition_name in condition_names:
                    condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=True, user=user)
                    
                    if condition_created:
                        condition.save()
                    
                    objective.conditions.add(condition)
                
            # edit mode
            else:
                objective, objective_created = Objective.objects.get_or_create(id__exact=objective_id, user__exact=user, defaults={'name':objective_name,'type': objective_type, 'user':user})
                if not objective_created:
                    objective.name = objective_name
                    objective.type = objective_type
                    objective.save()
                    
                    # remove conditions then add
                    conditions = objective.conditions.all()
                    for condition in conditions:
                        objective.conditions.remove(condition)

                    for condition_name in condition_names:
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=True, user=user)
                        if condition_created:
                            condition.save()
                            
                        objective.conditions.add(condition)
            data = {}
            data['created'] = str(objective_created).lower()
            data['objective_name'] = objective_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
                                        
        elif object_type == OBJECT_TYPE_OBSTACLE:
            
            obstacle_id = request.POST.get('id', None)
            obstacle_name = request.POST.get('name', None)
            obstacle_type = request.POST.get('type', None)
            condition_names = request.POST.getlist('conditions[]', None)
            
            mode = request.POST.get('mode', None)
            mode = int(mode)
            
            if obstacle_id != '':
                obstacle_id = int(obstacle_id)
                
            obstacle_created = False
                        
            if mode == CREATE_NEW:
                # use obstacle name as an exact lookup
                obstacle, obstacle_created = Obstacle.objects.get_or_create(name__exact=obstacle_name, user__exact=user, defaults={'name':obstacle_name,'type': obstacle_type, 'user':user})

                if obstacle_created:
                    obstacle.save()
                                    
                for condition_name in condition_names:
                    condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=True, user=user)
                    if condition_created:
                        condition.save()
                        
                    obstacle.conditions.add(condition)
            # edit mode
            else:
                obstacle, obstacle_created = Obstacle.objects.get_or_create(id__exact=obstacle_id, user__exact=user, defaults={'name':obstacle_name,'type': obstacle_type, 'user':user})

                if not obstacle_created:
                    obstacle.name = obstacle_name
                    obstacle.type = obstacle_type
                    obstacle.save()
                    
                    # remove conditions then add
                    conditions = obstacle.conditions.all()
                    
                    for condition in conditions:
                        obstacle.conditions.remove(condition)
                    
                    for condition_name in condition_names:
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=True, user=user)
                        if condition_created:
                            condition.save()
                        obstacle.conditions.add(condition)

            data = {}
            data['created'] = str(obstacle_created).lower()
            data['obstacle_name'] = obstacle_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
            
        elif object_type == OBJECT_TYPE_CONDITION:
            
            condition_id = request.POST.get('id', None)
            condition_name = request.POST.get('name', None)
            mode = request.POST.get('mode', None)
            mode = int(mode)
            
            if condition_id != '':
                condition_id = int(condition_id)
                
            condition_created = False
                        
            if mode == CREATE_NEW:
                # use condition name as an exact lookup
                condition, condition_created = Condition.objects.get_or_create(name__exact=condition_name, user__exact=user, defaults={'name':condition_name, 'user':user})

                if condition_created:
                    condition.save()                                    
            # edit mode
            else:
                condition, condition_created = Condition.objects.get_or_create(id__exact=condition_id, user__exact=user, defaults={'name':condition_name, 'user':user})

                if not condition_created:
                    condition.name = condition_name
                    condition.save()
                    
            data = {}
            data['created'] = str(condition_created).lower()
            data['condition_name'] = condition_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        elif object_type == OBJECT_TYPE_CONTEXT_CONSTRAINT:
            constraint_id = request.POST.get('id', None)
            constraint_name = request.POST.get('name', None)
            condition_names = request.POST.getlist('conditions[]', None)

            mode = request.POST.get('mode', None)
            mode = int(mode)
            if constraint_id:
                constraint_id = int(constraint_id)
            constraint_created = False
            if mode == CREATE_NEW:
                # use constraint name as an exact lookup
                constraint, constraint_created = ContextConstraint.objects.get_or_create(name__exact=constraint_name, user__exact=user, defaults={'name':constraint_name, 'user':user})
                if constraint_created:
                    constraint.save()       
                    
                for condition_name in condition_names:
                    condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=False, user=user)
                    
                    if condition_created:
                        condition.save()
                    
                    constraint.conditions.add(condition)
                                                 
            # edit mode
            else:
                constraint, constraint_created = ContextConstraint.objects.get_or_create(id__exact=constraint_id, user__exact=user, defaults={'name':constraint_name, 'user':user})

                if not constraint_created:
                    constraint.name = constraint_name
                    constraint.save()

                    # remove conditions then add
                    conditions = constraint.conditions.all()
                    
                    for condition in conditions:
                        constraint.conditions.remove(condition)
                    
                    for condition_name in condition_names:
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=False, user=user)
                        if condition_created:
                            condition.save()
                        constraint.conditions.add(condition)
            data = {}
            data['created'] = str(constraint_created).lower()
            data['constraint_name'] = constraint_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
                        
        elif object_type == OBJECT_TYPE_PERMISSION:
            print 'A'
            permission_id = request.POST.get('id', None)
            operation_name = request.POST.get('operation_name', None)
            object_name = request.POST.get('object_name', None)
            print 'A1'
            permission_name = operation_name + '_' + object_name
            print 'A2'
            mode = request.POST.get('mode', None)
            
            mode = int(mode)
            print 'A3'
            if permission_id:
                permission_id = int(permission_id)
            print 'A4'
            permission_created = False
            print 'A4a'
            if mode == CREATE_NEW:
                print 'A4b'
                # use permission name as an exact lookup
                print 'permission_name ', permission_name
                print 'operation_name ', operation_name
                print 'object_name ', object_name
                try:
                    permission, permission_created = Permission.objects.get_or_create(name__exact=permission_name, user__exact=user, defaults={'name':permission_name, 'operation':operation_name, 'object':object_name, 'user':user, 'mincardinality':0, 'maxcardinality':0})
                    print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                except: # catch *all* exceptions
                    print 'Error!!!!!!!!!!!!!!!!!!!!!!!!!'
                    e = sys.exc_info()[0]
                    print "<p>Error: %s</p>" % e
                    #write_to_page( "<p>Error: %s</p>" % e )
                
                print 'A5'
                if permission_created:
                    print 'A6'
                    permission.save()    
                    print 'A7'   
                                                                     
            # edit mode - none for permissions
            else:
                pass
                    
            data = {}
            data['created'] = str(permission_created).lower()
            data['permission_name'] = permission_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
            
        elif object_type == OBJECT_TYPE_TASK:
            print 'A'
            task_id = request.POST.get('id', None)
            task_name = request.POST.get('name', None)
            scenarios = request.POST.getlist('scenarios[]', None)

            mode = request.POST.get('mode', None)
            mode = int(mode)
            print 'A1'
            if task_id:
                task_id = int(task_id)
                
            task_created = False
            if mode == CREATE_NEW:
                print 'A2'
                # use constraint name as an exact lookup
                task, task_created = Task.objects.get_or_create(name__exact=task_name, user__exact=user, defaults={'name':task_name, 'user':user})
                print 'A3'
                if task_created:
                    print 'A4'
                    task.save()       
                    print 'A5'
                    
                for i in scenarios:
                    scenario, scenario_created = Scenario.objects.get_or_create(name=i.name, user=user)
                    
                    if scenario_created:
                        scenario.save()
                    
                    task.scenarios.add(scenario)
                print 'A6'
            # edit mode
            else:
                constraint, constraint_created = ContextConstraint.objects.get_or_create(id__exact=constraint_id, user__exact=user, defaults={'name':constraint_name, 'user':user})

                if not constraint_created:
                    constraint.name = constraint_name
                    constraint.save()

                    # remove conditions then add
                    conditions = constraint.conditions.all()
                    
                    for condition in conditions:
                        constraint.conditions.remove(condition)
                    
                    for condition_name in condition_names:
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, is_abstract=False, user=user)
                        if condition_created:
                            condition.save()
                        constraint.conditions.add(condition)
            data = {}
            data['created'] = str(task_created).lower()
            data['task_name'] = task_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
                                
    # if a GET (or any other method)
    else:    
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objectives = Objective.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'objectives':objectives}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_OBSTACLE:
            obstacles = Obstacle.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'obstacles':obstacles}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_CONDITION:
            conditions = Condition.objects.all().filter(user=user).filter(is_abstract=False)
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

def delete_permission(request):
    user = request.user
    print 'A'
    data = {}
    if request.method == 'POST':      
        print 'A1'
        permission_id = request.POST.get('permission_id', None)
        print 'A2'
        if permission_id:
            print 'A3'
            o = Permission.objects.get(id=permission_id, user=user)
            print 'A4'
            o.delete()
            print 'A5'
            data['deleted'] = 'true'
            data['permission_id'] = permission_id
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
