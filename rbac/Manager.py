import sys

from .models import Objective
from .models import Obstacle
from .models import AbstractContextCondition
from .models import Condition
from .models import Step
from .models import Scenario
from .models import Task
from .models import WorkProfile
from .models import ContextConstraint
from .models import Permission
from .models import Role

from Error import xoRETwError

    


def getAllDirectlyAssignedPerms(role, user):
    pass

def getAllTransitivelyAssignedPerms(role, user):
    pass
    
def getAllPerms(role, user):
    all_perms = getAllDirectlyAssignedPerms(role, user)
    transitive_perms = getAllTransitivelyAssignedPerms(role, user)
    if transitive_perms:
        for perm in transitive_perms:
            if perm not in all_perms:
                all_perms.append(perm)
    return all_perms

#done    
def existRole(role_name, user):
    try:
        print 'e3'
        print 'role_name is ', role_name
        role = Role.objects.get(name=role_name, user=user)
        print 'e4'
    except Role.DoesNotExist:
        print 'e5 - Role.DoesNotExist'
        return 0
    print 'e6'
    return 1      
      
#done
def getAllSeniorRoles(role_name, user):
    print 'call to getAllSeniorRoles'
    print 'role_name i s ', role_name
    
    role = Role.objects.get(name=role_name, user=user)
    print 'role is ', role
    print 'role name is ', role.name
    
    print 'getting role.senior_roles.all()'
    senior_roles = role.senior_roles
    
    print 'senior_roles is ', senior_roles
    if senior_roles:
        print 'senior_roles.name', senior_roles.name
        
    seniors = []
    print 'seniors is ', seniors
    print 'GG2'
    
    if senior_roles:
        print 'hellow', dir(senior_roles)
        for sr in senior_roles:
            print 'GG3'
            print sr.name
            seniors.append(sr.name)

    print 'seniors is ', seniors
    if seniors:
        print 'GG5'
        for sr in seniors:
            print 'GG6'
            next_level = getAllSeniorRoles(sr, user)
            for r in next_level:
                if r not in seniors:
                    seniors.append(r)
    return seniors

#done
def getAllJuniorRoles(role_name, user):
    print 'getAllJuniorRoles'
    role = Role.objects.get(name=role_name, user=user)
    print 'zz'
    junior_roles = role.junior_roles
    print 'zz2'
    juniors = []
    
    if junior_roles:
        for jr in junior_roles:
            print jr.name
            juniors.append(jr.name)
    
    if juniors:
        for jr in juniors:
            next_level = getAllJuniorRoles(jr, user)
            for r in next_level:
                if r not in juniors:
                    juniors.append(r)
    return juniors
    
#done
def getInheritedSSDRoleConstraints(role_name, user):
    junior_roles = getAllJuniorRoles(role_name, user)
    inherited = []
    if junior_roles:
        for r in junior_roles:
            # get inherited role constraints
            issdrc = getSSDRoleConstraints(r, user)

            if issdrc:
                inherited = inherited + issdrc
        
    return inherited
    
#done
def getTransitiveSSDRoleConstraints(role_name, user):
    direct = getDirectSSDRoleConstraints(role_name, user)
    transitive = []

    if direct:
        for r in direct:
            senior_roles = getAllSeniorRoles(r, user)
            if senior_roles:
                transitive  = transitive + senior_roles
    return transitive
    
#done    
def getDirectSSDRoleConstraints(role, user):
    role_obj = Role.objects.get(name=role, user=user)
    ssd_constraints = role_obj.ssd_constraints.all()

    ssd_role_constraints = []
    for r in ssd_constraints:
        ssd_role_constraints.append(r.name)
        
    return ssd_role_constraints

#done    
def getSSDRoleConstraints(role, user):
    direct = getDirectSSDRoleConstraints(role, user)
    transitive = getTransitiveSSDRoleConstraints(role, user)
    inherited = getInheritedSSDRoleConstraints(role, user)
    
    return direct + transitive + inherited
    
#done    
def hasSSDRoleConstraintTo(role, r, user):
    mutlExclRoles = getSSDRoleConstraints(role, user)
    if mutlExclRoles:
        for mutlExclRole in mutlExclRoles:
            if r == mutlExclRole:
                return 1
    return 0

#    
def hasSSDPermConstraintTo(role, r, user):
    own = getAllPerms(role, user)
    other = getAllPerms(r, user)
    for p in own:
        for op in other:
            if isStaticallyMutualExclusive(p, op, user):
                return 1
    return 0

#        
def isStaticallyMutualExclusive(role, r, user):
    if hasSSDRoleConstraintTo(role, r, user):
        return 1
    #if hasSSDPermConstraintTo(role, r, user):
    #    return 1
    return 0

#done    
def ssdConstraintsAllowSeniorRole(role, senior, user):   
    allseniors = getAllSeniorRoles(senior, user)
    for r in allseniors:
        if isStaticallyMutualExclusive(role, r, user):
            return 0
    return 1

#done        
def createRole(name, junior_roles, senior_roles, user):
    print 'B'
    """
    if junior_roles:
        print 'Ba'
        # now check if two or more of the intended juniorRoles are defined as 
        # mutual exclusive or own mutual exclusive permissions
        for r1 in junior_roles:
            for r2 in junior_roles:
                print 'C'
                if r1 != r2:
                    print 'isStaticallyMutualExclusive'
                    if isStaticallyMutualExclusive(r1, r2, user):
                        e = "Error: at least two of the intended junior-roles of " + name + " are mutual exclusive." + r1 + " and " + r2 + " are mutually exclusive or own permissions that are mutual exclusive."
                        raise xoRETwError(e)
    
    if junior_roles and senior_roles:
        for sr in senior_roles:
            for jr in junior_roles:
                print 'ssdConstraintsAllowSeniorRole'
                if not ssdConstraintsAllowSeniorRole(jr, sr, user):
                    e = "FAILED, " + jr + " and " + sr + " are statically mutual exclusive. Therefore, " + sr + " cannot be defined as (transitive) senior-role of " + jr + ". Creation of role " + name + " failed."
                    raise xoRETwError(e)
    """
    
    # create the new role
    try:
        print 'D'
        role_obj, created = Role.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
        print 'E'
    except Exception as e:
        error_message = str(e)
        raise xoRETwError(error_message)
    print 'F'    
    if created:
        print 'G'
        role_obj.save()
    
    """
    # save junior roles to this role
    if junior_roles:
        print 'H'
        for jr in junior_roles:
            print 'I'
            print 'junior role is ', jr
            obj, created = Role.objects.get_or_create(name=jr, user=user)
            print 'J'
            if created:
                print 'K'
                obj.save()
            print '12'
            role_obj.junior.add(obj)
            print '12A'

    # save senior_roles to this role    
    if senior_roles:
        print 'save senior_roles to this role'
        for sr in senior_roles:
            print 'sr is ', sr
            obj, created = Role.objects.get_or_create(name=sr, user=user)
            print 'after'
            if created:
                print 'created true'
                obj.save()
                
            role_obj.senior.add(obj)
        
    # remove all redundant superclass-relations
    # my updateRoleHierarchy
    """
    return 1

def createScenario(name, graph_dot, user):
    # use scenario name as an exact lookup
    try:
        obj, created = Scenario.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'graph':graph_dot, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if created:
        obj.save()
        return 1
        
    return 0
    
def createContextConstraint(name, user):
    
    # use context constraint name as an exact lookup
    try:
        obj, created = ContextConstraint.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()
        return 1
        
    return 0

def createStep(actor, action, target, user):
    
    name = actor + '_' + action + '_' + target
    
    # use step name as an exact lookup
    try:
        obj, created = Step.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'actor':actor, 'action':action, 'target':target, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()
        return name, 1
        
    return name, 0

def createTask(name, user):
    
    # use task name as an exact lookup
    try:
        obj, created = Task.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()
        return 1
        
    return 0

def createObjective(objective_name, objective_type, user):

    # use objective name as an exact lookup
    try:
        obj, created = Objective.objects.get_or_create(name__exact=objective_name, user__exact=user, defaults={'name':objective_name,'type': objective_type, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()   
        return 1

def deleteObjective(objective_name, user):
    objective = Objective.objects.get(name=objective_name, user=user)
    objective.delete()
    return 1

def linkConditionToContextConstraint(condition, name, user):
    # use CC_condition name as an exact lookup
    print '1'
    try:
        print 'name is ', name
        CC = ContextConstraint.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    print '2'    
    if CC:
        print '3'
        obj, created = Condition.objects.get_or_create(name=condition, user=user)
        print '4'
        if created:
            obj.save()
        print '5'    
        CC.conditions.add(obj)
        print '6'
        return 1

def unlinkConditionFromContextConstraint(condition, name, user):
    # use CC_condition name as an exact lookup
    try:
        CC = ContextConstraint.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    if CC:
        obj, created = Condition.objects.get_or_create(name=condition, user=user)
        if not created:
            CC.conditions.remove(obj)
            return 1
    return 0

# a role cannot be defined as mutual exclusive to one of its junior-roles
# or one of its senior-roles. Furthermore two roles that have a common
# senior-role must not be defined as mutual exclusive.
# role and mutlexcl are role names respectively (e.g. "Student" or "Professor")
def setSSDRoleConstraint(role, mutlexcl, user):
    return 0

def setSSDPermConstraint(perm, mutlexcl, user):
    if not permAssignedToSameRole(perm, mutlexcl, user):
        try:
            perm_obj = Permission.objects.get(name=perm, user=user)
        except:
            e = sys.exc_info()[0]
            raise xoRETwError(e)
        
        if perm_obj:
            try:
                mutlexcl_obj, created = Permission.objects.get_or_create(name__exact=mutlexcl, user__exact=user)
            except:
                e = sys.exc_info()[0]
                raise xoRETwError(e)
        
            if created:
                print 'Error - should not have been created here.'

            perm_obj.ssd_constraints.add(mutlexcl_obj)
            

        try:
            mutlexcl_obj = Permission.objects.get(name=mutlexcl, user=user)
        except:
            e = sys.exc_info()[0]
            raise xoRETwError(e)
        
        if mutlexcl_obj:
            try:
                perm_obj, created = Permission.objects.get_or_create(name__exact=perm, user__exact=user)
            except:
                e = sys.exc_info()[0]
                raise xoRETwError(e)
        
            if created:
                print 'Error - should not have been created here.'

            mutlexcl_obj.ssd_constraints.add(perm_obj)
            
            return 1
            
    return 0

def transitivelyOwnsPerm(role, perm, user):
    return 0
    
def directlyOwnsPerm(role, perm, user):
    
    permissions = role.permissions.all()
    print '############ permissions: ', permissions
    for permission in permissions:
        print 'permission.name is ', permission.name
        if permission.name == perm:
            return 1
    return 0

def ownsPerm(role, perm, user):
    if directlyOwnsPerm(role, perm, user) or transitivelyOwnsPerm(role, perm, user):
        return 1
    return 0
    
def permAssignedToSameRole(perm1, perm2, user):
    print 'perm1 is ', perm1
    print 'perm2 is ', perm2
    
    role_list = getRoleList(user)  
    owners = []

    for role in role_list:
        if ownsPerm(role, perm1, user) and ownsPerm(role, perm2, user):
            owners.append(role)
    if owners:
        return 1
    
    return 0


def linkContextConstraintsToPerm(ccs, name, user):
    
    try:
        perm = Permission.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if perm:
        for cc in ccs:
            try:
                obj, created = ContextConstraint.objects.get_or_create(name__exact=cc, user__exact=user)
            except:
                e = sys.exc_info()[0]
                print "<p>Error: %s</p>" % e
                
            if created:
                obj.save()
            
            perm.context_constraints.add(obj)
        
        return 1

def addScenariosToTask(scenarios, name, user):
    # use task name as an exact lookup
    try:
        task = Task.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if task:
        for scenario in scenarios:
            try:
                obj, created = Scenario.objects.get_or_create(name__exact=scenario, user__exact=user)
            except:
                e = sys.exc_info()[0]
                print "<p>Error: %s</p>" % e
                
            if created:
                obj.save()
            
            task.scenarios.add(obj)
        
        return 1

def addTasksToWorkProfile(tasks, name, user):
    # use profile name as an exact lookup
    try:
        profile = WorkProfile.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if profile:
        for task in tasks:
            try:
                obj, created = Task.objects.get_or_create(name__exact=task, user__exact=user)
            except:
                e = sys.exc_info()[0]
                print "<p>Error: %s</p>" % e
            if created:
                obj.save()
            
            profile.tasks.add(obj)
        
        #obj, created = Task.objects.get_or_create(name=task, user=user)
                    
        #if created:
        #    obj.save()
            
        #profile.tasks.add(obj)
        
        return 1

def addDerivedAbstractContextConditionToObjective(abstract_context_condition, objective_name, user):
    # use objective name as an exact lookup
    try:
        objective = Objective.objects.get(name=objective_name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if objective:
        obj, created = AbstractContextCondition.objects.get_or_create(name=abstract_context_condition, user=user)
                    
        if created:
            obj.save()
            
        objective.abstract_context_conditions.add(obj)
        
        return 1
    
def clearDerivedConditionListOfObjective(name, user):
    
    objective = Objective.objects.get(name=name, user=user)
    
    # remove derived_conditions
    derived_conditions = objective.abstract_context_conditions.all()
    
    for derived_condition in derived_conditions:
        objective.abstract_context_conditions.remove(derived_condition)

    return 1
    
def unsetSSDRoleConstraint(role, mutlexcl, user):
    
    role_obj = Role.objects.get(name=role, user=user)
    mutlexcl_obj = Role.objects.get(name=mutlexcl, user=user)
    
    role_obj.ssd_constraints.remove(mutlexcl_obj)
    
    return 1

def unsetSSDPermConstraint(perm, mutlexcl, user):
    
    perm_obj = Permission.objects.get(name=perm, user=user)
    mutlexcl_obj = Permission.objects.get(name=mutlexcl, user=user)
    
    perm_obj.ssd_constraints.remove(mutlexcl_obj)
    
    return 1
    
def unlinkContextConstraintsFromPerm(name, user):
    
    obj = Permission.objects.get(name=name, user=user)
    
    ccs = obj.context_constraints.all()

    # remove all context constraints    
    for cc in ccs:
        obj.context_constraints.remove(cc)

    return 1

def clearScenarioListOfTask(name, user):
    
    obj = Task.objects.get(name=name, user=user)
    
    scenarios = obj.scenarios.all()

    # remove all scenarios    
    for scenario in scenarios:
        obj.scenarios.remove(scenario)

    return 1

def clearTaskListOfWorkProfile(name, user):
    
    profile = WorkProfile.objects.get(name=name, user=user)
    
    # remove tasks
    tasks = profile.tasks.all()
    
    for task in tasks:
        profile.tasks.remove(task)

    return 1

#=====================================================

def createObstacle(name, type, user):
    # use obstacle name as an exact lookup
    try:
        obj, created = Obstacle.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name,'type':type, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()   
        return 1

def deleteObstacle(name, user):
    print 'name is ', name
    print 'deleteObstacle 1'
    obj = Obstacle.objects.get(name=name, user=user)
    print 'deleteObstacle 2'
    obj.delete()
    print 'deleteObstacle 3'
    return 1
    
def addDerivedAbstractContextConditionToObstacle(abstract_context_condition, name, user):
    
    # use objective name as an exact lookup
    try:
        obstacle = Obstacle.objects.get(name=name, user=user)
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    if obstacle:
        obj, created = AbstractContextCondition.objects.get_or_create(name=abstract_context_condition, user=user)
                    
        if created:
            obj.save()
            
        obstacle.abstract_context_conditions.add(obj)
        
        return 1
    
def clearDerivedConditionListOfObstacle(name, user):
    
    obstacle = Obstacle.objects.get(name=name, user=user)
    
    # remove derived_conditions
    derived_conditions = obstacle.abstract_context_conditions.all()
    
    for derived_condition in derived_conditions:
        obstacle.abstract_context_conditions.remove(derived_condition)

    return 1

#==========================================


def createCondition(name, user):
    
    # use the condition name as an exact lookup
    try:
        obj, created = Condition.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()   
        return 1

def deleteCondition(name, user):
    obj = Condition.objects.get(name=name, user=user)
    obj.delete()
    return 1

def deleteStep(name, user):
    obj = Step.objects.get(name=name, user=user)
    obj.delete()
    return 1

def deletePermission(name, user):
    obj = Permission.objects.get(name=name, user=user)
    obj.delete()
    return 1

def deleteContextConstraint(name, user):
    obj = ContextConstraint.objects.get(name=name, user=user)
    obj.delete()
    return 1

def deleteTask(name, user):
    obj = Task.objects.get(name=name, user=user)
    obj.delete()
    return 1

def deleteProfile(name, user):
    obj = WorkProfile.objects.get(name=name, user=user)
    obj.delete()
    return 1
    
def deleteScenario(name, user):
    print 'name is ', name
    obj = Scenario.objects.get(name=name, user=user)
    print '2'
    obj.delete()
    print '3'
    return 1

def deleteRole(name, user):
    print 'role name is ', name
    obj = Role.objects.get(name=name, user=user)
    obj.delete()
    print 'delete success!!!!!!!!!!!!'
    return 1

def createProfile(name, user):
        
    # use the permission name as an exact lookup
    try:
        obj, created = WorkProfile.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()   
        return 1

def createPermission(perm_operation, perm_object, user):
    
    name = perm_operation + '_' + perm_object
    
    # use the permission name as an exact lookup
    try:
        obj, created = Permission.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'perm_operation':perm_operation, 'perm_object':perm_object, 'user':user})
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
    
    if created:
        obj.save()   
        return 1

def getPermissionList(user):
    return Permission.objects.filter(user=user)

def getContextConstraintList(user):
    return ContextConstraint.objects.filter(user=user)

def getConditionList(user):
    return Condition.objects.filter(user=user)

def getScenarioList(user):
    return Scenario.objects.filter(user=user)

def getStepList(user):
    return Step.objects.filter(user=user)

def getTaskList(user):
    return Task.objects.filter(user=user)

def getRoleList(user):
    return Role.objects.filter(user=user)

def getContextConstraints(name, user):
    perm = Permission.objects.get(name=name, user=user)
    return perm.context_constraints.all()

def getSSDPermConstraints(name, user):
    perm = Permission.objects.get(name=name, user=user)
    return perm.ssd_constraints.all()

def getAllConditions(name, user):
    CC = ContextConstraint.objects.get(name=name, user=user)
    return CC.conditions.all()
