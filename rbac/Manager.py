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


def getAllDirectlyAssignedPerms(role_name, user):
    print 'getAllDirectlyAssignedPerms'
    role_obj = Role.objects.get(name=role_name, user=user)
    
    direct = []
    
    if role_obj.permissions:
        direct = role_obj.permissions.split(',')
        
    return direct

def getAllTransitivelyAssignedPerms(role_name, user):
    junior_roles = getAllJuniorRoles(role_name, user)
    transitive_perms = []
    jr_direct_perms = []
    
    if junior_roles:
        for role in junior_roles:
            jr_direct_perms = getAllDirectlyAssignedPerms(role, user)
            if jr_direct_perms:
                for p in jr_direct_perms:
                    if p not in transitive_perms:
                        transitive_perms.append(p)
                        
    return transitive_perms

    
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
    print 'getAllSeniorRoles'
    print 'role_name is ', role_name 
    role_obj = Role.objects.get(name=role_name, user=user)
    print '11'
    senior_roles = role_obj.senior_roles
    print 'role_obj.senior_roles ', role_obj.senior_roles
    print 'type(senior_roles): ', type(senior_roles)
    
    senior = []
    
    if senior_roles:
        senior = senior_roles.split(',')
    
    if senior:
        for sr in senior:
            next_level = getAllSeniorRoles(sr, user)
            for r in next_level:
                if r not in senior:
                    senior.append(r)
                    
    return senior

#done
def getAllJuniorRoles(role_name, user):
        
    print 'getAllJuniorRoles'
    
    role = Role.objects.get(name=role_name, user=user)
    junior_roles = role.junior_roles
    
    junior = []
    
    if junior_roles:
        junior = junior_roles.split(',')
    
    if junior:
        for jr in junior:
            next_level = getAllJuniorRoles(jr, user)
            for r in next_level:
                if r not in junior:
                    junior.append(r)
    
    return junior
    
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
    print 'getTransitiveSSDRoleConstraints'
    
    direct = getDirectSSDRoleConstraints(role_name, user)
    print '1 direct ', direct
    transitive = []

    if direct:
        for r in direct:
            senior_roles = getAllSeniorRoles(r, user)
            if senior_roles:
                transitive  = transitive + senior_roles
    return transitive
    
#done    
def getDirectSSDRoleConstraints(role_name, user):
    
    print 'getDirectSSDRoleConstraints'
    role_obj = Role.objects.get(name=role_name, user=user)
    print 'role_obj.ssd_constraints ', role_obj.ssd_constraints
    direct = []
    
    # empty string
    if role_obj.ssd_constraints:
        print 'not empty'
        direct = role_obj.ssd_constraints.split(',')
    
    print 'type(direct)', type(direct)
    print 'direct', direct
    return direct

#done    
def getSSDRoleConstraints(role, user):
    print 'getSSDRoleConstraints'
    direct = getDirectSSDRoleConstraints(role, user)
    transitive = getTransitiveSSDRoleConstraints(role, user)
    inherited = getInheritedSSDRoleConstraints(role, user)
    
    return direct + transitive + inherited
    
#done    
def hasSSDRoleConstraintTo(role, r, user):
    print 'hasSSDRoleConstraintTo'
    mutlExclRoles = getSSDRoleConstraints(role, user)
    if mutlExclRoles:
        for mutlExclRole in mutlExclRoles:
            if r == mutlExclRole:
                return 1
    return 0

#done
def hasSSDPermConstraintTo(role, r, user):
    own = getAllPerms(role, user)
    other = getAllPerms(r, user)
    for p in own:
        for op in other:
            if isStaticallyMutualExclusivePerm(p, op, user):
                return 1
    return 0

#done
def isStaticallyMutualExclusivePerm(perm_name, p, user):

    perm_obj = Permission.objects.get(name=perm_name, user=user)
    
    ssd_constraints = []
    
    if perm_obj.ssd_constraints:
        ssd_constraints = perm_obj.ssd_constraints.split(',')
        for i in ssd_constraints:
            if i == p:
                return 1
    
    return 0

#done        
def isStaticallyMutualExclusive(role, r, user):
    print 'isStaticallyMutualExclusive'
    if hasSSDRoleConstraintTo(role, r, user):
        return 1
    if hasSSDPermConstraintTo(role, r, user):
        return 1
    return 0

#done    
def ssdConstraintsAllowSeniorRole(role, senior, user):
    print 'ssdConstraintsAllowSeniorRole'
    allseniors = getAllSeniorRoles(senior, user)
    print 'allseniors ', allseniors
    for r in allseniors:
        if isStaticallyMutualExclusive(role, r, user):
            print 'return 0'
            return 0
    print 'return 1'
    return 1

#done        
def createRole(name, junior_roles, senior_roles, user):
    
    print '1'
    if junior_roles:
        
        # now check if two or more of the intended juniorRoles are defined as 
        # mutual exclusive or own mutual exclusive permissions
        
        for r1 in junior_roles:
            for r2 in junior_roles:
                if r1 != r2:
                    print 'r1 is ', r1
                    print 'r2 is ', r2
                    if isStaticallyMutualExclusive(r1, r2, user):
                        e = "Error: at least two of the intended junior-roles of " + name + " are mutual exclusive." + r1 + " and " + r2 + " are mutually exclusive or own permissions that are mutual exclusive."
                        raise xoRETwError(e)
    
    print '------2------'
    
    
    if junior_roles and senior_roles:
        for sr in senior_roles:
            for jr in junior_roles:
                if not ssdConstraintsAllowSeniorRole(jr, sr, user):
                    e = "FAILED, " + jr + " and " + sr + " are statically mutual exclusive. Therefore, " + sr + " cannot be defined as (transitive) senior-role of " + jr + ". Creation of role " + name + " failed."
                    raise xoRETwError(e)
    
    print '------3------'
    
    # create the new role
    try:
        role_obj, created = Role.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
    except Exception as e:
        error_message = str(e)
        raise xoRETwError(error_message)
    if created:
        role_obj.save()
        
    print '------4------'
    
    # save junior roles to this role
    junior = []
    if junior_roles:
        for jr in junior_roles:
            obj, created = Role.objects.get_or_create(name=jr, user=user)
            if created:
                obj.save()
                
            junior.append(jr)
        
        print 'junior is ', junior
        role_obj.junior_roles = ",".join(junior)
        role_obj.save()
        
        # save senior_roles to this role
        senior = []
        print 'senior_roles is ', senior_roles
        if senior_roles:
            for sr in senior_roles:
                print 'sr is ', sr
                obj, created = Role.objects.get_or_create(name=sr, user=user)
                if created:
                    print 'created - senior'
                    obj.save()

                senior.append(sr)
            
        print '1 senior is ', senior
        s = ",".join(senior)
        print 's is ', s
        role_obj.senior_roles = s
        role_obj.save()
           
    # remove all redundant superclass-relations
    # my updateRoleHierarchy
    
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

#done
def possessCommonSeniorRole(role_name1, role_name2, user):
    r1SeniorRoles = getAllSeniorRoles(role_name1, user)
    r2SeniorRoles = getAllSeniorRoles(role_name2, user)
    
    for sr2 in r2SeniorRoles:
        if sr2 in r1SeniorRoles:
            return 1
    return 0    

def setSSDConstraint(role_name, mutlexcl_name, user):
    return 1
    
"""
Role instproc setSSDConstraint {role} {
  my instvar ssdconstraints
  set name [self]
  if {![string equal $name $role]} {
    if {![my hasSSDRoleConstraintTo $role]} {
      set ssdconstraints($role) 1
      my log NORMAL "[self] [self proc]: defined <<$role>> as (statically) mutual exclusive."
      return 1
    } else {
      my log INFO "[self] [self proc] INFO, role: <<$role>> is already (statically)\
                       mutual exclusive to <<[self]>>. Note\
                       that SSD Constraints are inherited via a role-hierarchy."
      return 0
    }
  } else {
    my log FAILED "[self] [self proc] FAILED, a role cannot be mutual exclusive to itself."
    return 0
  }
}
"""

"""
# role is fully-qualified name of a runtime-role-object (e.g. re::roles::MyRole)
Role instproc unsetSSDConstraint {role} {
  my instvar ssdconstraints
  if {[info exists ssdconstraints($role)]} {
    unset ssdconstraints($role)
    my log NORMAL "[self] [self proc]: deleted mutual exclusion constraint to <<$role>>."
    return 1
  } else {
    my log FAILED "[self] [self proc] FAILED, role: <<$role>> is not mutual exclusive\
                       to <<[my name]>>"
    return 0
  }
}
"""

# a role cannot be defined as mutual exclusive to one of its junior-roles
# or one of its senior-roles. Furthermore two roles that have a common
# senior-role must not be defined as mutual exclusive.
# role and mutlexcl are role names respectively (e.g. "Student" or "Professor")
def setSSDRoleConstraint(role_name, mutlexcl_name, user):

    if role_name != mutlexcl_name:
        if not possessCommonSeniorRole(role_name, mutlexcl_name, user):
            juniorRoles = getAllJuniorRoles(role_name, user)
            seniorRoles = getAllSeniorRoles(role_name, user)
            if mutlexcl_name not in seniorRoles:
                if mutlexcl_name not in juniorRoles:
                    success = setSSDConstraint(role_name, mutlexcl_name, user)
                    if success:
                        setSSDConstraint(mutlexcl_name, role_name, user)
                        
                    return success
                else:
                    e = "FAILED, role <<$role>> cannot be mutual exclusive to its junior-role <<$mutlexcl>>."
                    raise xoRETwError(e)                                            
            else:
                e = "FAILED, role <<$role>> cannot be mutual exclusive to its senior-role <<$mutlexcl>>"
                raise xoRETwError(e)                        
        else:
            e = "FAILED, <<$role>> and <<$mutlexcl>> possess a common senior-role."
            raise xoRETwError(e)
    else:
        e = "FAILED, a role cannot be mutual exclusive to itself."
        raise xoRETwError(e)
    return 0

def setSSDPermConstraint(perm_name, mutlexcl_name, user):
    print 'setSSDPermConstraint'
    
    if not permAssignedToSameRole(perm_name, mutlexcl_name, user):
        print 'not permAssignedToSameRole'
        try:
            perm_obj = Permission.objects.get(name=perm_name, user=user)
        except Exception as e:
            error_message = str(e)
            raise xoRETwError(e)
        
        ssd_constraints = []
        
        if perm_obj.ssd_constraints:
            ssd_constraints = perm_obj.ssd_constraints.split(',')
            
        ssd_constraints.append(mutlexcl_name)
        perm_obj.ssd_constraints = ",".join(ssd_constraints)
        perm_obj.save()
            
        try:
            mutlexcl_obj = Permission.objects.get(name=mutlexcl_name, user=user)
        except Exception as e:
            error_message = str(e)
            raise xoRETwError(e)
        
        ssd_constraints = []
        
        if mutlexcl_obj.ssd_constraints:
            ssd_constraints = mutlexcl_obj.ssd_constraints.split(',')
            
        ssd_constraints.append(perm_name)
        mutlexcl_obj.ssd_constraints = ",".join(ssd_constraints)
        mutlexcl_obj.save()
            
        return 1
    else:
        e = "FAILED, at least one role owns both permissions <<$perm>> and <<$mutlexcl>> (directly or transitively). In order to register a mutual exclusion constraint for two permissions they must not be assigned to the same role."        
        raise xoRETwError(e)
        
    return 0

#done
def transitivelyOwnsPerm(role_name, perm, user):
    junior_roles = getAllJuniorRoles(role_name, user)
    for role in junior_roles:
        if directlyOwnsPerm(role_name, perm, user):
            return 1
    return 0

#done    
def directlyOwnsPerm(role_name, perm, user):
    
    role_obj = Role.objects.get(name=role_name, user=user)
    
    permissions = []
    
    if role_obj.permissions:
        permissions = role_obj.permissions.split(',')    
    
    for p in permissions:
        if p == perm:
            return 1
    return 0

def ownsPerm(role_name, perm, user):
    print 'ownsPerm'
    if directlyOwnsPerm(role_name, perm, user) or transitivelyOwnsPerm(role_name, perm, user):
        return 1
    return 0
    
def permAssignedToSameRole(perm1, perm2, user):
    print 'permAssignedToSameRole'
    print 'perm1 is ', perm1
    print 'perm2 is ', perm2
    
    role_list = getRoleList(user)  
    owners = []
    print 'role_list ', role_list
    
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
    print '1'
    name = perm_operation + '_' + perm_object
    print 'name is ', name
    print '2'
    # use the permission name as an exact lookup
    try:
        print '3'
        obj, created = Permission.objects.get_or_create(name__exact=name, user__exact=user, defaults={'name':name, 'user':user})
        print '4'
    except:
        e = sys.exc_info()[0]
        raise xoRETwError(e)
        
    print '5'
    if created:
        print '6'
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
    role_list = Role.objects.filter(user=user)
    roles = []
    
    for r in role_list:
        roles.append(r.name)
        
    return roles

def getContextConstraints(name, user):
    perm = Permission.objects.get(name=name, user=user)
    return perm.context_constraints.all()

def getSSDPermConstraints(name, user):
    print 'getSSDPermConstraints'
    perm_obj = Permission.objects.get(name=name, user=user)
    
    ssd_perm_constraints = []
    if perm_obj.ssd_constraints:
        ssd_perm_constraints = perm_obj.ssd_constraints.split(',')
        
    print 'ssd_perm_constraints: ', ssd_perm_constraints
    return ssd_perm_constraints

def getAllConditions(name, user):
    CC = ContextConstraint.objects.get(name=name, user=user)
    return CC.conditions.all()


"""
  set perm [self]::permissions::[join $perm _]
  set role [self]::roles::$role
  if {[my existRole $role]} {
    if {[my existPermission $perm]} {	   
      if {[my ssdPermConstraintAllowPRA $perm $role]} {
	if {[my permMaxCardinalityAllowAssignment $perm]} {
	  set success [$role assignPerm $perm]
	  if {$success} {
	    my incrPermOwnerQuantity $perm
	    my addTraceRelation Permission [$perm name] assigned-to Role [$role name]
	  }
	  return $success
	} else {
	  my log FAILED "[self] [self proc] FAILED, the permission maximum owner cardinality of\
                             <<[$perm name]>> is already reached. In order to assign permission\
                             <<[$perm name]>> to role: <<[$role name]>> you have to revoke\
                             <<[$perm name]>> from at least one of its current owners first."
	  return 0
	}		    
      } else {
	my log FAILED "[self] [self proc] FAILED, assignment prevented by SSD constraint defined on\
                           permission <<$perm>>. <<$role>> or one of its owners (subjects) possesses\
                           at least one permission that is defined as mutual exclusive to <<$perm>>."
	return 0
      }
    } else {
      my log FAILED "[self] [self proc] FAILED, permission <<$perm>> does not exist."
      return 0
    }
  } else {
    my log FAILED "[self] [self proc] FAILED, role: <<$role>> does not exist."
    return 0
  }
}

# perm is an "action object" pair
Manager instproc permRoleRevoke {perm role} {
  set perm [self]::permissions::[join $perm _]    
  set role [self]::roles::$role
  if {[my existRole $role]} {
    if {[my existPermission $perm]} {
      if {[my permMinCardinalityAllow $perm]} {
	set success [$role revokePerm $perm]
	if {$success} {
	  my decrPermOwnerQuantity $perm
	  my removeTraceRelation Permission [$perm name] assigned-to Role [$role name]
	}
	return $success
      } else {
	my log FAILED "[self] [self proc] FAILED, the permission minimal owner cardinality\
                    of <<[$perm name]>> has already been reached\
             \n --> In order to revoke permission <<$perm>> from role: <<$role>>\
                    you have to assign at least one new owner first."
	return 0
      }
    } else {
      my log FAILED "[self] [self proc] FAILED, permission <<$perm>> does not exist."
      return 0
    }
  } else {
    my log FAILED "[self] [self proc] FAILED, role: <<$role>> does not exist."
    return 0
  }
}

"""
