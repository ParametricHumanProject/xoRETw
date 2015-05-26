from django.db import models

# Create your models here.

class Step(models.Model):
    name = models.CharField(max_length=50)
    step = models.ManyToManyField('self')

class Condition(models.Model):
    name = models.CharField(max_length=50)

class Scenario(models.Model):
    name = models.CharField(max_length=50)
    step = models.ManyToManyField(Step)

class Task(models.Model):
    name = models.CharField(max_length=50)
    scenario = models.ManyToManyField(Scenario)

class Objective(models.Model):
    name = models.CharField(max_length=50)
    step = models.ManyToManyField(Step)
    objective = models.ManyToManyField('self')
    scenario = models.ManyToManyField(Scenario)
    
class Obstacle(models.Model):
    name = models.CharField(max_length=50)
    objective = models.ManyToManyField(Objective)

class ContextConstraint(models.Model):
    name = models.CharField(max_length=50)
    condition = models.ManyToManyField(Condition)
    obstacle = models.ManyToManyField(Obstacle)
    objective = models.ManyToManyField(Objective)

class WorkProfile(models.Model):
    name = models.CharField(max_length=50)
    task = models.ManyToManyField(Task)
    
class Role(models.Model):
    name = models.CharField(max_length=50)
    role = models.ManyToManyField('self')

class Permission(models.Model):
    name = models.CharField(max_length=50)
    step = models.OneToOneField(Step)
    role = models.ManyToManyField(Role)
    context_constraint = models.ManyToManyField(ContextConstraint)
    

