from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('test_1',views.test_1,name='test_1'),
    path('details',views.details,name='details'),
    path('main_page',views.main_page,name='main_page'),
    path('add_post_1',views.add_post_1,name='add_post_1'),
    path('add_post_1_post',views.add_post_1_post,name='add_post_1_post'),
    path('search_fri',views.search_fri,name='search_fri'),
    path('add_friend',views.add_friend,name='add_friend'),
    path('add_request',views.add_request,name='add_request'),
    path('search_word',views.search_word,name='search_word'),
    path('add_post_2',views.add_post_2,name='add_post_2'),
    path('add_post_3',views.add_post_3,name='add_post_3'),
    path('show_post_2/<str:idd>',views.show_post_2,name='show_post_2'),
    path('show_post_3/<str:idd>',views.show_post_3,name='show_post_3'),
    path('add_like_p1/<id>',views.add_like_p1,name='add_like_p1'),
]
