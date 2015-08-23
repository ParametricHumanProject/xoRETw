from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Condition(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)

class AbstractContextCondition(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)

class Step(models.Model):
    user    = models.ForeignKey(User)
    name    = name = models.TextField(unique=True)

    actor   = models.TextField()
    action  = models.TextField()
    target  = models.TextField()

class Scenario(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    graph = models.TextField()

class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    
    scenarios = models.ManyToManyField(Scenario)

class WorkProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    
    tasks = models.ManyToManyField(Task)

class Objective(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    objective_type = models.TextField(blank=True)
    
    conditions = models.ManyToManyField(Condition)
    abstract_context_conditions = models.ManyToManyField(AbstractContextCondition)
    
    steps = models.ManyToManyField(Step)
    objective = models.ManyToManyField('self')
    scenarios = models.ManyToManyField(Scenario)

class Obstacle(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    obstacle_type = models.TextField(blank=True)
    
    conditions = models.ManyToManyField(Condition)
    abstract_context_conditions = models.ManyToManyField(AbstractContextCondition)
    
    objective = models.ManyToManyField(Objective, blank=True)

class ContextConstraint(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    conditions = models.ManyToManyField(Condition, blank=True)

class Permission(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    
    perm_operation = models.TextField(blank=True)
    perm_object = models.TextField(blank=True)
    
    #step = models.OneToOneField(Step, blank=True)

    context_constraints = models.ManyToManyField(ContextConstraint, blank=True)
    
    ssd_constraints = models.TextField(blank=True)
    
    mincardinality = models.IntegerField(default=0)  # same as blank=True, null=True
    maxcardinality = models.IntegerField(default=0)  # same as blank=True, null=True    
        
class Role(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(unique=True)
    
    junior_roles = models.TextField()
    senior_roles = models.TextField()
    ssd_constraints = models.TextField()
    
    permissions = models.TextField()
    
    work_profile = models.OneToOneField(WorkProfile, null=True)
    
    mincardinality = models.IntegerField(default=0)  # same as blank=True, null=True
    maxcardinality = models.IntegerField(default=0)  # same as blank=True, null=True    





