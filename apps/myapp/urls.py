from django.urls import path
from . import views
urlpatterns = [
    path('list/',views.StudentList.as_view()),
    path('update/<int:id>/',views.StudentData.as_view()),

    path('register/',views.UserRegisterApi.as_view()),
    path('login/',views.LoginApi.as_view()),
    path('logout/',views.LogoutApi.as_view()),

]
