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
        
        objective_name = request.POST.get('name', None)
        objective_type = request.POST.get('type', None)
        condition_names = request.POST.getlist('conditions[]', None)
        mode = request.POST.get('mode', None)
        mode = int(mode)
        
        # TODO: handle each object_type        
        if object_type == OBJECT_TYPE_OBJECTIVE:
            if mode == CREATE_NEW:
                try:
                    objective, created = Objective.objects.get_or_create(name=objective_name, type=objective_type, user=user)
                except Exception, e:
                    print 'error exists already'
                    data = {}
                    data['created'] = 'False'
                    data['objective_name'] = objective_name
                    json_data = json.dumps(data)
                    return HttpResponse(json_data, content_type='application/json')
                
                if created:
                    objective.save()
                                    
                for condition_name in condition_names:
                    condition, created = Condition.objects.get_or_create(name=condition_name, user=user)
                    
                    if created:
                        condition.save()
                        
                    objective.conditions.add(condition)
                
            # edit mode
            else:
                pass

            data = {}
            data['created'] = 'True'
            data['objective_name'] = objective_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
    # if a GET (or any other method)
    else:    
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objectives = Objective.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'objectives':objectives}, context_instance=RequestContext(request))
            
    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))

def delete_objective(request):
    user = request.user
    
    # if this is a POST request we need to process the data
    if request.method == 'POST':      
        print 'hellopw deltee'  
        objective_id = request.POST.get('objective_id', None)
        print 'objective_id is ', objective_id
        
        response = json.dumps('{"message":"FAIL to deltet"}')
        if objective_id:
            response = json.dumps('{"message":"DELETED"}')
            o = Objective.objects.get(id=objective_id, user=user)
            o.delete()
    
    return HttpResponse(response, content_type='application/json')


def edit_objective(request):
    user = request.user
    
    # if this is a POST request we need to process the data
    if request.method == 'GET':        
        objective_id = request.GET.get('objective_id', None)
        print 'edit objective id ', objective_id
        
        if objective_id:
            o = Objective.objects.get(id=objective_id, user=user)
    
    response = json.dumps('{"message":"Edit data"}')
    return HttpResponse(response, content_type='application/json')
