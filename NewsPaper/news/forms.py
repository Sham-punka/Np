from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError
from django_filters import ModelMultipleChoiceFilter


class PostForm(forms.ModelForm):
    author = ModelMultipleChoiceFilter(
        field_name='author__author_id',
        queryset=Author.objects.all(),
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'postCategory',
            'author',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if title is not None and len(title) > 40:
            raise ValidationError({
                'title': 'Название не может превышать 32 символа.'
            })
        if title == text:
            raise ValidationError({
                'text': 'Содержание названия и текста статьи/новости не должно совпадать.'
            })
        return cleaned_data