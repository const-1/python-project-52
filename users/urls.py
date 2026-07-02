from django.urls import path
from . import views

urlpatterns = [
    # Список всех пользователей
    path('', views.UserListView.as_view(), name='users_list'),

    # Регистрация нового пользователя
    path('create/', views.UserCreateView.as_view(), name='user_create'),

    # Редактирование профиля пользователя
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),

    # Удаление пользователя
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
