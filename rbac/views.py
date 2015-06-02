from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from .models import Objective
from .models import Condition

# constants
CREATE_NEW = 1
OBJECT_TYPE_OBJECTIVE = 1


def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

@login_required
def dashboard(request):
    user = request.user
    object_type = request.GET.get('object_type', 1) # default Objective tab
    object_type = int(object_type)

    # if this is a POST request we need to process the data
    if request.method == 'POST':
        
        objective_id = request.POST.get('id', None)
        objective_name = request.POST.get('name', None)
        objective_type = request.POST.get('type', None)
        condition_names = request.POST.getlist('conditions[]', None)
        mode = request.POST.get('mode', None)
        mode = int(mode)
        
        #objective_id = int(objective_id)
        if objective_id != '':
            objective_id = int(objective_id)
            
        print 'mode is ', mode
        
        # TODO: handle each object_type        
        if object_type == OBJECT_TYPE_OBJECTIVE:
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
                        #remove(other_model_object)#condition.delete()
                    
                    for condition_name in condition_names:
                        condition, condition_created = Condition.objects.get_or_create(name=condition_name, user=user)
                        if condition_created:
                            condition.save()
                        objective.conditions.add(condition)
                                        
            data = {}
            data['created'] = str(objective_created).lower()
            data['objective_name'] = objective_name
            json_data = json.dumps(data)
            print 'returned objective_created is ', objective_created
            return HttpResponse(json_data, content_type='application/json')
        
    # if a GET (or any other method)
    else:    
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objectives = Objective.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'objectives':objectives}, context_instance=RequestContext(request))
            
    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))


def delete_objective(request):
    user = request.user

    data = {}
        
    if request.method == 'POST':      
        objective_id = request.POST.get('objective_id', None)
        
        if objective_id:
            o = Objective.objects.get(id=objective_id, user=user)
            o.delete()
            data['deleted'] = 'True'
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
    
    for i in objective.conditions.all():
        data['conditions'].append(i.name)
    
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
