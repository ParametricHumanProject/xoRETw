from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Condition(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)

class AbstractContextCondition(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)

class Step(models.Model):
    user = models.ForeignKey(User)
    actor = models.CharField(max_length=50, unique=True)
    action = models.CharField(max_length=50, unique=True)
    target = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200, unique=True)
    step = models.ManyToManyField('self')

class Scenario(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    graph = models.TextField(blank=True)
    steps = models.ManyToManyField(Step)

class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    scenarios = models.ManyToManyField(Scenario)

class WorkProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField(Task)

class Objective(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    conditions = models.ManyToManyField(Condition)
    abstract_context_conditions = models.ManyToManyField(AbstractContextCondition)
    
    steps = models.ManyToManyField(Step)
    objective = models.ManyToManyField('self')
    scenarios = models.ManyToManyField(Scenario)

class Obstacle(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    
    conditions = models.ManyToManyField(Condition)
    abstract_context_conditions = models.ManyToManyField(AbstractContextCondition)
    
    objective = models.ManyToManyField(Objective)

class ContextConstraint(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    conditions = models.ManyToManyField(Condition)

class Permission(models.Model):
    user = models.ForeignKey(User)
    
    name = models.CharField(max_length=50, unique=True)
    perm_operation = models.CharField(max_length=50, unique=True)
    perm_object = models.CharField(max_length=50, unique=True)
    
    step = models.OneToOneField(Step, null=True, blank=True)

    context_constraints = models.ManyToManyField(ContextConstraint)
    ssd_constraints = models.ManyToManyField('self')
    
    mincardinality = models.IntegerField(default=0)  # same as blank=True, null=True
    maxcardinality = models.IntegerField(default=0)  # same as blank=True, null=True    
        
class Role(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    
    junior_roles = models.ForeignKey('self', related_name='junior', null=True, blank=True)
    senior_roles = models.ForeignKey('self', related_name='senior', null=True, blank=True)
    ssd_constraints = models.ManyToManyField('self', null=True, blank=True)
    
    permissions = models.ManyToManyField(Permission, null=True, blank=True)
    
    work_profile = models.OneToOneField(WorkProfile, null=True, blank=True)
    
    mincardinality = models.IntegerField(default=0)  # same as blank=True, null=True
    maxcardinality = models.IntegerField(default=0)  # same as blank=True, null=True    





