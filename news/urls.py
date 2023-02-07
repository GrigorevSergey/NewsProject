from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView, add_subscribe, \
        del_subscribe

urlpatterns = [
        path('', PostList.as_view()),
        path('<int:pk>', PostDetail.as_view(), name='post_detail'),
        path('search', PostSearch.as_view()),
        path('add', PostAdd.as_view(), name='post_add'),
        path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
        path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
        path('categories/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
        path('categories/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),

]