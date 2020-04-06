from django.db import models
from custom_user.models import MyCustomUser


class Ticket(models.Model):
    new = 'nw'
    in_progress = 'nprgs'
    done = 'dn'
    invalid = 'nvld'
    status_choices = [
                      (new, 'New'),
                      (in_progress, 'In Progress'),
                      (done, 'Done'),
                      (invalid, 'Invalid')
                      ]
    title = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    filed_by = models.ForeignKey(
                                 MyCustomUser,
                                 on_delete=models.CASCADE,
                                 related_name='filed_by'
                                 )
    status = models.CharField(
             max_length=5,
             choices=status_choices,
             default=new
            )
    assigned_to = models.ForeignKey(
                                    MyCustomUser,
                                    on_delete=models.CASCADE,
                                    related_name='assigned_to',
                                    null=True,
                                    blank=True,
                                    default=None
                                    )

    completed_by = models.ForeignKey(
                                     MyCustomUser,
                                     on_delete=models.CASCADE,
                                     related_name='completed_by',
                                     null=True,
                                     blank=True,
                                     default=None
                                     )
