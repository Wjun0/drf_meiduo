from django.conf.urls import url


from . import views

urlpatterns = [
    url('^areas/$',views.AreasView.as_view()),
    url(r'^areas/(?P<pk>\d+)/$', views.RetriveAreasView.as_view())
]