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
        print 'request is ', request
        name = request.POST.get('name', None)
        #conditions = request.POST.get('conditions[]', None)
        conditions = request.POST.getlist('conditions[]', None)
        print 'name is ', name
        print 'conditions is ', conditions
        
        response = json.dumps('{"message":"Ok"}')
        return HttpResponse(response, content_type='application/json')
    # if a GET (or any other method) we'll create a blank form
    else:
        print 'user_id = request.user.id is ', user_id
        print 'object_type ', object_type
        
        
        #option = int(request.GET.get('object', 0))
        #return render_to_response('dashboard.html', {}, context_instance=RequestContext(request))
    
    return render_to_response('dashboard.html', {'object_type':object_type}, context_instance=RequestContext(request))


