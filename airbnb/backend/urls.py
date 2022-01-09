from django.conf.urls import url, include,re_path
from . import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
    url(r'display_city$',views.display_city,),
    url(r'avg_score$',views.avg_score,),
    url(r'top_score_neighborhood$',views.top_score_neighborhood,),
    url(r'per_price', views.per_price,),
    url(r'popular_description', views.popular_description,),
    url(r'predict_price', views.predict_price,),
    url(r'avg_score$', views.avg_score,),
    url(r'predict_ratio$', views.predict_ratio,)

]