from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^areas/$',views.AreasView.as_view()),
    url(r'^areas/(?P<pk>\d+)/$', views.RetriveAreasView.as_view()),
    url(r'^addresses/$',views.AddressesView.as_view()),
    url(r'^addresses/(?P<pk>\d+)/$',views.AddressesView.as_view()),
    url(r'^addresses/(?P<pk>\d+)/status/$',views.AddressDefault.as_view()),
    url(r'^addresses/(?P<pk>\d+)/title/$',views.AddressTitle.as_view()),
]