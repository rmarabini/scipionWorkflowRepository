from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created     = models.DateTimeField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.created = timezone.now()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class WorkFlow(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    versionInit = models.CharField(max_length=16)
    versionEnd = models.CharField(max_length=16, default="-1", blank=True)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, null=True, blank=True)
    json = models.TextField()
    created     = models.DateTimeField(editable=False, blank=True, null=True)
    modified    = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.slug = slugify(self.name)
        self.modified = timezone.now()
        return super(WorkFlow, self).save(*args, **kwargs)


class KeyWord(models.Model):
    keyword = models.CharField(max_length=32)
    workflow = models.ForeignKey(WorkFlow)

    def __str__(self):
        return "%s (%s)"%(self.keyword, self.workflow.name)

class Protocol(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created     = models.DateTimeField(editable=False, blank=True, null=True)
    timesUsed   = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.created = timezone.now()
        super(Protocol, self).save(*args, **kwargs)
