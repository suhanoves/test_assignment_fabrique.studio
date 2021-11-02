from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateField('date published')
    expiry_date = models.DateField('expiration date')

    class Meta:
        verbose_name = 'poll'
        verbose_name_plural = 'polls'

        constraints = [
            models.CheckConstraint(
                check=models.Q(expiry_date__gt=models.F('pub_date')),
                name='expiry_date_gt_pub_date'
            )
        ]

    def __str__(self):
        return self.title
