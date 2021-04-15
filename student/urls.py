from django.urls import path
from .views import signup,login,logout

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
   

]