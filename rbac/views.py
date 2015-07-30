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
            
            print 'OBJECT_TYPE_TASK'
            task_id = request.POST.get('id', None)
            task_name = request.POST.get('name', None)
            scenario_names = request.POST.getlist('scenarios[]', None)
            #condition_names = request.POST.getlist('conditions[]', None)

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
                    
                for scenario_name in scenario_names:
                    print 'scenario_name is ', scenario_name
                    
                    try:
                        scenario, scenario_created = Scenario.objects.get_or_create(name__exact=scenario_name, user__exact=user)
                    except: # catch *all* exceptions
                        print 'Error!!!!!!!!!!!!!!!!!!!!!!!!!'
                        e = sys.exc_info()[0]
                        print "<p>Error: %s</p>" % e
                        #write_to_page( "<p>Error: %s</p>" % e )
                    
                    print '7'
                    if scenario_created:
                        print 'created'
                        scenario.save()
                    print 'adddd'
                    task.scenarios.add(scenario)
                print 'A6'
            # edit mode
            else:
                print 'B1'
                task, task_created = Task.objects.get_or_create(id__exact=task_id, user__exact=user, defaults={'name':task_name, 'user':user})
                print 'B2'
                if not task_created:
                    task.name = task_name
                    task.save()
                    print 'B3'
                    # remove conditions then add
                    scenarios = task.scenarios.all()
                    print 'B4'
                    for scenario in scenarios:
                        task.scenarios.remove(scenario)
                    print 'B5'
                    print 'scenario_names is ', scenario_names
                    for scenario_name in scenario_names:
                        print 'scenario_name'
                        scenario, scenario_created = Scenario.objects.get_or_create(name=scenario_name, user=user)
                        print 'A7'
                        if not scenario_created:
                            print 'A8'
                            scenario.save()
                            print 'A9'
                        task.scenarios.add(scenario)
                    print 'B7'
            data = {}
            data['created'] = str(task_created).lower()
            data['task_name'] = task_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
            
        elif object_type == OBJECT_TYPE_STEP:
            print '11'
            step_id = request.POST.get('id', None)
            actor = request.POST.get('actor', None)
            action = request.POST.get('action', None)
            target = request.POST.get('target', None)
            print '22'
            step_name = actor + '_' + action + '_' + target
            mode = request.POST.get('mode', None)
            
            mode = int(mode)
            
            if step_id:
                step_id = int(step_id)
                
            step_created = False
            
            if mode == CREATE_NEW:
                print 'mode create new step'
                # use step name as an exact lookup
                #print 'permission_name ', step_name
                #print 'operation_name ', operation_name
                #print 'object_name ', object_name
                try:
                    print '33'
                    step, step_created = Step.objects.get_or_create(name__exact=step_name, user__exact=user, defaults={'name':step_name, 'actor':actor, 'action':action, 'target':target, 'user':user})
        
                except: # catch *all* exceptions
                    print 'Error!!!!!!!!!!!!!!!!!!!!!!!!!'
                    e = sys.exc_info()[0]
                    print "<p>Error: %s</p>" % e
                    #write_to_page( "<p>Error: %s</p>" % e )
                
                print 'A5'
                print 'step_created is ', step_created
                if step_created:
                    print 'A6'
                    step.save()    
                    print 'A7'   
                                                                     
            # TODO: edit mode
            #else:
            #    pass
            print 'bbb'
            data = {}
            data['created'] = str(step_created).lower()
            print "data['created'] ", data['created']
            data['step_name'] = step_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
            
        elif object_type == OBJECT_TYPE_SCENARIO:
            scenario_id = request.POST.get('id', None)
            scenario_name = request.POST.get('name', None)
            scenario_graph_dot = request.POST.get('graph_dot', None)
            print 'scenario_graph_dot is ', scenario_graph_dot
            mode = request.POST.get('mode', None)

            mode = int(mode)

            if scenario_id != '':
                scenario_id = int(scenario_id)
            
            scenario_created = False
                        
            if mode == CREATE_NEW:
                
                # use scenario name as an exact lookup
                scenario, scenario_created = Scenario.objects.get_or_create(name__exact=scenario_name, user__exact=user, defaults={'name':scenario_name, 'graph':scenario_graph_dot, 'user':user})
                
                if scenario_created:
                    scenario.save()
                                    
            # edit mode
            else:
                print '7'
                scenario, scenario_created = Scenario.objects.get_or_create(id__exact=scenario_id, user__exact=user, defaults={'name':scenario_name, 'graph':scenario_graph_dot, 'user':user})

                # should already exist since we're doing an update
                if not scenario_created:
                    scenario.name = scenario_name
                    scenario.graph = scenario_graph_dot
                    scenario.save()
                    
            data = {}
            data['created'] = str(scenario_created).lower()
            data['scenario_name'] = scenario_name
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        elif object_type == OBJECT_TYPE_ROLE:
            print '1'
            
            role_id = request.POST.get('id', None)
            role_name = request.POST.get('name', None)
            junior_role_names = request.POST.getlist('junior_roles[]', None)
            senior_role_names = request.POST.getlist('senior_roles[]', None)
                        
            mode = request.POST.get('mode', None)
            mode = int(mode)
            
            if role_id:
                role_id = int(role_id)
            
            print '4'
            role_created = False
                        
            if mode == CREATE_NEW:
                # use role name as an exact lookup
                            
                try:
                    print '6'
                    role, role_created = Role.objects.get_or_create(name__exact=role_name, user__exact=user, defaults={'name':role_name, 'user':user})
                    print '7'
                except: # catch *all* exceptions
                    print 'Error!!!!!!!!!!!!!!!!!!!!!!!!!'
                    e = sys.exc_info()[0]
                    print "<p>Error: %s</p>" % e                
                
                
                #role, role_created = Role.objects.get_or_create(name__exact=role_name, user__exact=user, defaults={'name':role_name, 'user':user})
                print '8'
                if role_created:
                    print '9'
                    role.save()
                    print '10'
                
                print 'a'
                for junior_role_name in junior_role_names:
                    print 'b'
                    junior_role, junior_role_created = Role.objects.get_or_create(name=junior_role_name, user=user)
                    print 'c'
                    
                    if junior_role_created:
                        print 'd'
                        junior_role.save()
                    print 'e'
                    role.junior_roles.add(junior_role)
                    print 'f'

                for senior_role_name in senior_role_names:
                    print 'b'
                    senior_role, senior_role_created = Role.objects.get_or_create(name=senior_role_name, user=user)
                    print 'c'
                    
                    if senior_role_created:
                        print 'd'
                        senior_role.save()
                    print 'e'
                    role.senior_roles.add(senior_role)
                    print 'f'
                                    
            # edit mode
            else: # TODO:
                print '7'
                scenario, scenario_created = Scenario.objects.get_or_create(id__exact=scenario_id, user__exact=user, defaults={'name':scenario_name, 'graph':scenario_graph_dot, 'user':user})

                # should already exist since we're doing an update
                if not scenario_created:
                    scenario.name = scenario_name
                    scenario.graph = scenario_graph_dot
                    scenario.save()

            print 'g'
            data = {}
            data['created'] = str(role_created).lower()
            data['role_created'] = role_created
            print 'h'
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
 
        elif object_type == PERM_CARDINALITY_CONSTRAINTS:
            perm_id = request.POST.get('id', None)
            mincardinality = request.POST.get('mincardinality', None)
            maxcardinality = request.POST.get('maxcardinality', None)
            
            perm_id = int(perm_id)
            perm, perm_created = Permission.objects.get_or_create(id__exact=perm_id, user__exact=user)

            # permission should already exist since we're doing an update
            if not perm_created:
                perm.mincardinality = mincardinality
                perm.maxcardinality = maxcardinality
                perm.save()
                
            data = {}
            data['success'] = True
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')

        elif object_type == ROLE_CARDINALITY_CONSTRAINTS:
            role_id = request.POST.get('id', None)
            mincardinality = request.POST.get('mincardinality', None)
            maxcardinality = request.POST.get('maxcardinality', None)
            role_id = int(role_id)
            role, role_created = Role.objects.get_or_create(id__exact=role_id, user__exact=user)

            # role should already exist since we're doing an update
            if not role_created:
                role.mincardinality = mincardinality
                role.maxcardinality = maxcardinality
                role.save()

            data = {}
            data['success'] = True
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
            
        elif object_type == PERM_CONTEXT_CONSTRAINTS:
            perm_id = request.POST.get('id', None)
            context_constraint_names = request.POST.getlist('context_constraints[]', None)
            print 'perm_id is ', perm_id
            perm_id = int(perm_id)
            perm, perm_created = Permission.objects.get_or_create(id__exact=perm_id, user__exact=user)

            # permission should already exist since we're doing an update
            #if not perm_created:
            #    perm.save()

            
            print 'context_constraint_names ', context_constraint_names
            #perm_id = int(perm_id)
            print 'A3'
            #perm_id = int(perm_id)
            #perm, perm_created = Permission.objects.get_or_create(id__exact=perm_id, user__exact=user)

            print 'A4'
            # permission should already exist since we're doing an update
            if not perm_created:
                print 'A5'
                # get all context constraints linked to this permission
                context_constraints = perm.context_constraints.all()
                print 'A6'
                # remove all context_constraints linked to this permission
                for context_constraint in context_constraints:
                    perm.context_constraints.remove(context_constraint)
                print 'A7'    
                for context_constraint_name in context_constraint_names:
                    context_constraint, context_constraint_created = ContextConstraint.objects.get_or_create(name=context_constraint_name, user=user)
                    print 'A8'                        
                    perm.context_constraints.add(context_constraint)

                print '5'

            print '6'
            data = {}
            data['success'] = True
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
        elif object_type == OBJECT_TYPE_STEP:
            steps = Step.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'steps':steps}, context_instance=RequestContext(request))
        elif object_type == OBJECT_TYPE_SCENARIO:
            scenarios = Scenario.objects.all().filter(user=user)
            return render_to_response('dashboard.html', {'object_type':object_type, 'scenarios':scenarios}, context_instance=RequestContext(request))
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

def delete_permission(request):
    user = request.user
    data = {}
    if request.method == 'POST':      
        permission_id = request.POST.get('permission_id', None)
        if permission_id:
            o = Permission.objects.get(id=permission_id, user=user)
            o.delete()
            data['deleted'] = 'true'
            data['permission_id'] = permission_id
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
    
