from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def index(request):
	print 'hellow'
	return render_to_response('/home/iancrrn/xoRETw/templates/index.html', {}, context_instance=RequestContext(request))
