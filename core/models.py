from django.db import models
from django.utils.text import slugify


class Application(models.Model):
    title = models.CharField(max_length=124, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title) if self.title else "Unnamed Application"
    

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