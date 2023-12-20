from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=100)
    skill_description = models.TextField()

    def __str__(self):
        return self.skill_name


class Talent(models.Model):
    full_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)
    skills = models.ManyToManyField(Skill)
    address = models.CharField(max_length=200)
    profile = models.CharField(max_length=1000, default=None)
    resume = models.CharField(max_length=1000, default=None)

    def __str__(self):
        return self.full_name
