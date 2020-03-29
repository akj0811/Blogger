from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Category
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
	context = {'categories': Category.objects.all(), 'posts': Blog.objects.all()}
	return render(request,'home.html', context)

def view_post(request, slug):
	post = get_object_or_404(Blog, slug=slug)
	context = {'post': post}
	return render(request,'view_post.html', context)

def view_category(request,slug):
	category = get_object_or_404(Category, slug=slug)
	context = {'category': category, 'posts': Blog.objects.filter(category=category)}
	return render(request,'view_category.html', context)

@login_required
def dashboard(request):
	user = request.user
	context = {'user': user, 'posts': Blog.objects.filter(author = user)}
	return render(request, 'dashboard.html', context)

def view_logout(request):
	logout(request)
	return render(request, 'logout.html')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields = ['title']
	template_name = 'category_create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Blog
	fields = ['title', 'category', 'content']
	template_name = 'post_form.html'

	def get_context_data(self, **kwargs):          
	    context = super().get_context_data(**kwargs)                     
	    context["categories"] = Category.objects.all()
	    return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Blog
	fields = ['title', 'content']
	template_name = 'post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Blog
	template_name = 'post_confirm_delete.html'
	success_url = '/blog/dashboard'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False