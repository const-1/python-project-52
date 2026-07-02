from django.contrib import admin
from django.urls import path, include
from . import views
from users.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('users/', include('users.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('statuses/', include('statuses.urls', namespace='statuses')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('labels/', include('labels.urls', namespace='labels')),
]

