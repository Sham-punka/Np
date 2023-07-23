from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category, Subscription
from django.db.models import Exists, OuterRef
from datetime import datetime
from .filters import NewsFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'newses.html'
    context_object_name = 'newses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        context['is_authent'] = self.request.user.is_authenticated
        return context



class NewsDeta(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NEWS'
        return super().form_valid(form)




class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'newses'
    ordering = '-dateCreation'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_authent'] = self.request.user.is_authenticated
        context['is_author'] = self.request.user.groups.filter(name='Authors').exists()
        context['time_now'] = datetime.utcnow()
        return context

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'ARTICLE'
        return super().form_valid(form)



# Представление удаляющее Post.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    template_name = 'news_update.html'
    form_class = PostForm

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    template_name = 'article_update.html'
    form_class = PostForm

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

