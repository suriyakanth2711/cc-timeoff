import uuid
from django.db import models


class PolicyModel(models.Model):
    organization = models.CharField(max_length=255)
    leave_type =  models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    num_of_leaves =  models.IntegerField()
    carry_forward = models.IntegerField()
    enchashment = models.IntegerField()
    max_num_cont_leaves = models.IntegerField()
    last_udpated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'leave_type','designation'], name='unique_policy')
        ]


    def __str__(self):
        return self.organization + self.designation


class LeaveModel(models.Model):
    employee_ID = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    leave_type =  models.CharField(max_length=255)
    applied_on =  models.DateTimeField(auto_now=True)
    status =  models.CharField(max_length=255)
    
    def __str__(self):
        return self.employee_ID 
