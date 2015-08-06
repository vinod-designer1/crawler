from django.db import models

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class URLDataStore(BaseModel):
  url = models.CharField('Url', max_length=500, blank=True, null=True)
  body = models.TextField('body', blank=True, null=True)
  extracted = models.BooleanField('extracted', default=False)

class URLRelationStore(BaseModel):
  parent_url = models.ForeignKey(URLDataStore, primary_key=True, related_name='parent_url')
  child_urls = models.ManyToManyField(URLDataStore, null=True, blank=True, related_name='child_urls')
