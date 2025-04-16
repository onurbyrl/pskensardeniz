from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Intervention(models.Model):
    title = models.CharField(max_length=124, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='intervention_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title) if self.title else "Unnamed Intervention"
    

class Message(models.Model):
    name = models.CharField(max_length=124, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=70, null=True, blank=True)
    message = models.TextField(max_length=210)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.subject
    

class Article(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    text = RichTextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else "Unnamed Article"