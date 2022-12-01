
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('first_app.urls')),
    # path('/', include('first_app.urls')),
]
