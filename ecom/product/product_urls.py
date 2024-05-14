from product import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("add/", views.add_product),
    path("show/", views.show_product),
    path("delete/<id>", views.delete_product),
    path("update/<id>", views.update_product),
    
     
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

