from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
	path('',views.home, name='home'),
    path('view/<slug:slug>/', views.view_post ,name='view_post'),
	path('category/<slug:slug>/', views.view_category ,name='view_category'),
	path('signup/', views.signup, name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
	path('logout/',views.view_logout,name='logout'),
	path('dashboard/', views.dashboard ,name='dashboard'),
	path('create_category/', views.CategoryCreateView.as_view(), name='category_create'),
	path('create_post/', views.PostCreateView.as_view(), name='post_create'),
	path('<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
	path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
] 