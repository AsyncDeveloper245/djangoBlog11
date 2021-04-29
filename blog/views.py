from .models import Post, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import ContactForm, LoginForm, CommentForm
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 2


class HomeTemplateView(TemplateView):
    template_name = 'landing.html'
    model = User
    context_object_name = 'user'


def RegistrationFormView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            new_user = User(username=username, password=password, email=email)
            new_user.save()
            return redirect('landing')
    else:
        form = ContactForm()
        return render(request, 'register.html', {'form': form})


def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            else:
                redirect('register')
        else:
            redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def BlogDetailView(request, id):
    post = Post.objects.get(id=id)
    new_comment = None
    comments = post.comments.all()

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form})


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'body', 'author']



class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

@login_required()
def Logout(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        logout(request)
        return redirect('landing')
    return render(request,'logout.html',{'user':user})

