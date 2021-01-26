from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from .forms import CreateUserForm,UserUpdateForm, ProfileUpdateForm,PostForm,RatingsForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView
from .models import Post,Profile,Rating
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

@login_required(login_url='login')
def index(request):
    context ={
        'posts': Post.objects.all()
    }
    return render(request, 'index.html' , context)


def ratings(request):
    ratings = Rate.objects.all()
    rate_params = {
        'ratings': ratings
    }

    return render('projects.html', rate_params)


# <app>/<model>_<viewtype>.html
class PostListView(ListView):
    model = Post    
    template_name = 'index.html'   
    context_object_name = 'posts'
    ordering = ['-date']


class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','description', 'projects','url']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@csrf_exempt
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form =CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
            
                messages.success(request,'Account was created successfully')
                return redirect('login')
        context = {'form': form}
        return render(request,'registration/register.html',  context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username ,password=password)
            
            if user is not None:   
                login(request, user)
               
        context={}
        return render(request,'registration/login.html',  context)

def logoutUser(request):
    logout(request)
    return redirect('login')    


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


@login_required(login_url='login')
def projects(request, post):   
    posts = Posts.objects.get(title=post)
    
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rate.objects.filter(post=post)

            design_ratings = [i.design for i in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [i.usability for i in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [i.content for i in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()

    else:
        form = RatingsForm()
    context = {
        'posts': posts,
        'rating_form': form

    }
    return render(request, 'projects.html', context)

def search_project(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Post.objects.filter(title__icontains=title).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image"  