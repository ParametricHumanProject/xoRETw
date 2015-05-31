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
        conditions = request.POST.getlist('conditions[]', None)
        mode = request.POST.get('mode', None)
        mode = int(mode)
        
        # TODO: handle each object_type        
        if object_type == OBJECT_TYPE_OBJECTIVE:
            if mode == CREATE_NEW:
                
                objective = Objective(name=objective_name, type=objective_type, user=user)
                objective.save()
                for condition in conditions:
                    c = Condition(name=condition, user=user)
                    c.save()
                    objective.conditions.add(c)
                
            # edit mode
            else:
                pass
                
            response = json.dumps('{"message":"Ok"}')
            return HttpResponse(response, content_type='application/json')
        
    # if a GET (or any other method)
    else:    
        if object_type == OBJECT_TYPE_OBJECTIVE:
            objectives = Objective.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'objectives':objectives}, context_instance=RequestContext(request))
            
    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))


