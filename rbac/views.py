from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
OBJECT_TYPE_PERMISSION = 4
OBJECT_TYPE_ROLE = 5
OBJECT_TYPE_STEP = 6
OBJECT_TYPE_SCENARIO = 7
OBJECT_TYPE_TASK = 8
OBJECT_TYPE_CONTEXTCONSTRAINT = 9


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
    

    # if this is a POST request we need to process the data
    if request.method == 'POST':
        
        object_type = request.POST.get('object_type', None)
        object_type = int(object_type)
        
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
