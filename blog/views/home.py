from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.views.generic import ListView
PER_PAGE = 9



# Class Based view da função home 
class PostListView(ListView):
    model =Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'page_obj'
    ordering = '-id'
    paginate_by = PER_PAGE 
    queryset = Post.objects.get_published()#Faz a mesma coisa do metodo abaixo  
    # def get_queryset(self):
    #      queryset = super().get_queryset()
    #      queryset = queryset.filter(is_published= True)

    #      return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context.update(
            {
                'title' : 'Home'
            }
        )
        return context
# Function Based view da class PostListView - as duas fazem as mesmas coisas
# def home(request):
#     posts= Post.objects.get_published()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#         }
#     )

def created_by(request, author_pk):
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published()\
        .filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )
def tag(request, slug):
    posts = Post.objects.get_published()\
        .filter(tag__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


class SearchListView(PostListView):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self._search_value = ''
        

    def setup(self, request, *args, **kwargs):
        self.search_value =request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value= self.search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
        )[:PER_PAGE] 
    
    def get_context_data(self, **kwargs):
        ctx= super().get_context_data(**kwargs)
        search_value = self.search_value
        ctx.update({
                'search_value' : search_value
             })
        return ctx
        
    def get(self, request, *args, **kwargs):
        if self.search_value == '':
            redirect('blog:home')
        return super().get(request, *args, **kwargs)
    
# def search(request):
#     search_value =request.GET.get('search', '').strip()
#     posts = (Post.objects.get_published()\
#         .filter(
#             Q(title__icontains=search_value) |
#             Q(excerpt__icontains=search_value) |
#             Q(content__icontains=search_value) 
#         )[:PER_PAGE]
#     )


#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value' : search
#         }
#     )

def page(request, slug):
    post = (
        Page.objects.filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': post
        }
    )


def post(request, slug):
    post = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
    )
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )