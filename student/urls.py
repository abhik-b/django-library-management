from django.urls import path
from .views import signup,home,login,logout,uploadfile_view

urlpatterns = [
    path('',home),
    path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('upload/', uploadfile_view),
   

]