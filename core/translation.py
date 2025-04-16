from modeltranslation.translator import register, TranslationOptions
from .models import Intervention, Article

@register(Intervention)
class ApplicationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'text')