from django.db import models
from clients.models import Client
from talents.models import Talent


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    expected_date = models.DateField()
    status = models.CharField(
        choices=(
            ('OPEN', 'Open'),
            ('CLOSED', 'Closed'),
            ('WIP', 'WIP'),
        ),
        max_length=30
    )
    award_points = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} {self.client.full_name}"


class ProjectTalent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # talent = models.ManyToOneRel(Talent, on_delete=models.CASCADE)
    talents = models.ManyToManyField(Talent)

    award_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.project} - {', '.join(str(talent) for talent in self.talents.all())}"
