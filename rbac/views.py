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
OBJECT_TYPE_PERMISSION = 4
OBJECT_TYPE_ROLE = 5
OBJECT_TYPE_STEP = 6
OBJECT_TYPE_SCENARIO = 7
OBJECT_TYPE_TASK = 8
OBJECT_TYPE_CONTEXTCONSTRAINT = 9


def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

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
        print 'object type is ', object_type
        
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
                    condition, condition_created = Condition.objects.get_or_create(name=condition_name, user=user)
                    
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
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, user=user)
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
            
            print 'obstacle_id ', obstacle_id
            print 'obstacle_name ', obstacle_name
            print 'obstacle_type ', obstacle_type
            print 'mode ', mode
            
            if mode == CREATE_NEW:
                print 'createing new obstacle'
                # use obstacle name as an exact lookup
                obstacle, obstacle_created = Obstacle.objects.get_or_create(name__exact=obstacle_name, user__exact=user, defaults={'name':obstacle_name,'type': obstacle_type, 'user':user})

                print 'A'
                if obstacle_created:
                    print 'A saving'
                    obstacle.save()
                                    
                print 'B0 condition_names', condition_names
                for condition_name in condition_names:
                    print 'condition_name i s ', condition_name
                    condition, condition_created = Condition.objects.get_or_create(name=condition_name, user=user)
                    print 'BB'
                    if condition_created:
                        print 'saving condition'
                        condition.save()
                        print 'condition saved'
                        
                    print 'C'
                    obstacle.conditions.add(condition)
                    print 'success'
                    
                print 'BZZZZ'
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
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, user=user)
                        if condition_created:
                            condition.save()
                        obstacle.conditions.add(condition)

            print 'C'
            data = {}
            print 'obstacle_created ', obstacle_created
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
            
            print 'condition_id ', condition_id
            print 'condition_name ', condition_name
            print 'mode ', mode
            
            if mode == CREATE_NEW:
                print 'creating new condition'
                # use condition name as an exact lookup
                condition, condition_created = Condition.objects.get_or_create(name__exact=condition_name, user__exact=user, defaults={'name':condition_name, 'user':user})

                print 'A'
                if condition_created:
                    print 'A saving'
                    condition.save()                                    
            # edit mode
            else:
                print 'hello'
                condition, condition_created = Condition.objects.get_or_create(id__exact=condition_id, user__exact=user, defaults={'name':condition_name, 'user':user})

                if not condition_created:
                    condition.name = condition_name
                    condition.save()
                    
            print 'C'
            data = {}
            print 'condition_created ', condition_created
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
            print 'get conditions'
            conditions = Condition.objects.all().filter(user=user)
            print 'conditions ', conditions
            print 'type of ', type(object_type)
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
    print 'v1'
    # if this is a POST request we need to process the data
    if request.method == 'GET':        
        print 'v2'
        objective_id = request.GET.get('objective_id', None)
        print 'v3'
        if objective_id:
            print 'v4'
            objective = Objective.objects.get(id=objective_id, user=user)
    print 'v5'
    # get name, type and conditions
    data = {}
    print 'v6'
    #data['objective_id'] = objective.name
    data['name'] = objective.name
    data['type'] = objective.type
    data['conditions'] = []

    print 'v7'
    for condition in objective.conditions.all():
        print 'v8'
        print 'condition ', condition.name
        data['conditions'].append(condition.name)
        print 'v9'
        
    print 'v10'
    json_data = json.dumps(data)
    print 'json_data ', json_data
    print 'v11'
    return HttpResponse(json_data, content_type='application/json')

def delete_obstacle(request):
    print 'A'
    user = request.user

    data = {}
    print 'A1'    
    if request.method == 'POST':      
        print 'A2'
        obstacle_id = request.POST.get('obstacle_id', None)
        print 'A3'
        print 'obstacle_id ', obstacle_id
        if obstacle_id:
            print 'A4'
            o = Obstacle.objects.get(id=obstacle_id, user=user)
            print 'A5'
            o.delete()
            print 'A6'
            data['deleted'] = 'true'
            data['obstacle_id'] = obstacle_id
            print 'A7'
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def edit_obstacle(request):
    user = request.user
    print 'aaa'
    # if this is a POST request we need to process the data
    if request.method == 'GET':   
        print 'aaa 0'     
        obstacle_id = request.GET.get('obstacle_id', None)
        print 'aaa1'
        
        if obstacle_id:
            print 'aaa2'
            obstacle = Obstacle.objects.get(id=obstacle_id, user=user)
    print 'aaa3'
    # get name, type and conditions
    data = {}
    
    data['name'] = obstacle.name
    data['type'] = obstacle.type
    data['conditions'] = []
    print '5'
    for condition in obstacle.conditions.all():
        print '6'
        print ' condition ', condition
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
    print 'aaa'
    # if this is a POST request we need to process the data
    if request.method == 'GET':   
        print 'aaa 0'     
        condition_id = request.GET.get('condition_id', None)
        print 'aaa1'
        
        if condition_id:
            print 'aaa2'
            condition = Condition.objects.get(id=condition_id, user=user)
    print 'aaa3'
    # get name, type and conditions
    data = {}
    
    data['name'] = condition.name
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
