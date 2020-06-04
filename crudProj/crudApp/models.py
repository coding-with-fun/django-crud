from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class ProjectType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class ProjectTag(models.Model):
    tag_name = models.CharField(max_length=15)

    class Meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name


class Project(models.Model):
    title = models.CharField(max_length=200, null=False)
    slug = models.CharField(max_length=200, null=False, unique=True)
    project_image = models.ImageField(upload_to='images/', default='images/project_sample.jpg')
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=False)
    project_tags = models.ManyToManyField(ProjectTag)
    project_body = models.TextField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_edit', kwargs={'slug': self.slug})
