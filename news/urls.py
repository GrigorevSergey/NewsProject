from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView, CategorylistView, \
    subscribe
from django.views.decorators.cache import cache_page
urlpatterns = (
    path('', cache_page(60)(PostList.as_view())),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view()),
    path('add', PostAdd.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategorylistView, name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

)
