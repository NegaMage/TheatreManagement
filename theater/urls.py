from django.urls import path
from . import views

app_name='theater'

urlpatterns = [
    path('', views.movies_list, name="movies_list"),
    path('<slug:name>/<slug:title>/', views.show_view, name="show_view"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('purchase/', views.purchase, name="purchase"),

]
