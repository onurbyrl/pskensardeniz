from modeltranslation.translator import register, TranslationOptions
from .models import Application

@register(Application)
class ApplicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
