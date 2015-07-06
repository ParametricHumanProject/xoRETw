from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Condition(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    is_abstract = models.BooleanField(default=False)

class Step(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    step = models.ManyToManyField('self')

class Scenario(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
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

    steps = models.ManyToManyField(Step)
    objective = models.ManyToManyField('self')
    scenarios = models.ManyToManyField(Scenario)

    
class Obstacle(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    conditions = models.ManyToManyField(Condition)
    objective = models.ManyToManyField(Objective)


# done
class ContextConstraint(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    conditions = models.ManyToManyField(Condition)
    
# done    
class Role(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    role = models.ManyToManyField('self')
    work_profile = models.OneToOneField(WorkProfile)

# done
class Permission(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    operation = models.CharField(max_length=50, unique=True)
    object = models.CharField(max_length=50, unique=True)
    step = models.OneToOneField(Step, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    context_constraints = models.ManyToManyField(ContextConstraint)
    mincardinality = models.IntegerField(default=0)  # same as blank=True, null=True
    maxcardinality = models.IntegerField(default=0)  # same as blank=True, null=True    


