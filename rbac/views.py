from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))

@login_required
def dashboard(request):
    user_id = request.user.id
    object_type = int(request.GET.get('object_type', 1))

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        objective_name = request.POST.get('name', None)
        objective_type = request.POST.get('type', None)
        conditions = request.POST.getlist('conditions[]', None)
        
        print 'objective_name is ', objective_name
        print 'objective_type is ', objective_type
        print 'conditions are ', conditions
        
        response = json.dumps('{"message":"Ok"}')
        
        return HttpResponse(response, content_type='application/json')
    # if a GET (or any other method) we'll create a blank form
    else:
        print 'user_id = request.user.id is ', user_id
        print 'object_type ', object_type
        
    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))


