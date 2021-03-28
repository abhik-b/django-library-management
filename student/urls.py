from django.urls import path
from .views import signup,home,login,logout

urlpatterns = [
    path('',home),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
   

]