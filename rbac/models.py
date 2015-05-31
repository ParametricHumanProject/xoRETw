from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Step(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    step = models.ManyToManyField('self')

class Condition(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)

class Scenario(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    step = models.ManyToManyField(Step)

class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    scenario = models.ManyToManyField(Scenario)

class Objective(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    conditions = models.ManyToManyField(Condition)

    #step = models.ManyToManyField(Step)
    #objective = models.ManyToManyField('self')
    #scenarios = models.ManyToManyField(Scenario)

    
class Obstacle(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    objective = models.ManyToManyField(Objective)

class ContextConstraint(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    condition = models.ManyToManyField(Condition)
    obstacle = models.ManyToManyField(Obstacle)
    objective = models.ManyToManyField(Objective)

class WorkProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    task = models.ManyToManyField(Task)
    
class Role(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    role = models.ManyToManyField('self')

class Permission(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    step = models.OneToOneField(Step)
    role = models.ManyToManyField(Role)
    context_constraint = models.ManyToManyField(ContextConstraint)
    

