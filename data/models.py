from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import json
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created     = models.DateTimeField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.created = timezone.now()
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('find:workflow_list_by_category',
                       args=[self.slug])

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class WorkFlow(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, default="")
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    versionInit = models.CharField(max_length=16) # create for this version
    versionEnd = models.CharField(max_length=16, default="-1", blank=True) # last valid version
    category = models.ManyToManyField(Category)
    client_ip = models.GenericIPAddressField(null=True, blank=True) # sender IP
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=True)
    keywords = models.CharField(max_length=256, default="")
    json = models.TextField()
    created     = models.DateTimeField(editable=False, blank=True, null=True)
    modified    = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def addView(self):
        self.views += 1

    def addLikes(self):
        self.likes += 1

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.slug = slugify(self.name)
        self.modified = timezone.now()
        self.parseJson(self.json)
        return super(WorkFlow, self).save(*args, **kwargs)

    def parseJson(self, jsonString):
        # TODO: check here we are using a correct JSON
        protocols = json.loads(jsonString)
        for protocol in protocols:
            try:
                obj = Protocol.objects.get(slug=slugify(protocol['object.className']))
            except Protocol.DoesNotExist:
                obj = Protocol(name=protocol['object.className'])
                obj.save()


    def get_absolute_url(self):
        return reverse('find:workflow_detail',
                        args=[self.id, self.slug])

#class KeyWord(models.Model):
#    keyword = models.CharField(max_length=32)
#    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
#
#    def __str__(self):
#        return "%s (%s)"%(self.keyword, self.workflow.name)

class Protocol(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created     = models.DateTimeField(editable=False, blank=True, null=True)
    timesUsed   = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.created = timezone.now()
        super(Protocol, self).save(*args, **kwargs)
