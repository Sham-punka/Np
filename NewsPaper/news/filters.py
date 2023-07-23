from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category


class NewsFilter(FilterSet):
    title = CharFilter(field_name='title', label='Заголовок')
    class Meta:
        model = Post
        fields = [
            'title',
            'categoryType',
            'postAuthor',

        ]
        labels = {
            'categoryType': 'Type',
        }

    postAuthor = CharFilter(
        field_name='postAuthor',
        label='Автор'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Сферы жизни',
        conjoined=True
    )

    added_after = DateTimeFilter(
        label='Дата публикации после',
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%d-%m-%Y',
            attrs={'type': 'datetime-local'},
        ),
    )
