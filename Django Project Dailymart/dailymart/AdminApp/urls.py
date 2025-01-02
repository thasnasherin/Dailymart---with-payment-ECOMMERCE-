from django.urls import path
from . import views

urlpatterns = [
    path('adminindex',views.adminindex,name = 'adminindex'),
    path('addcategory',views.addcategory,name = 'addcategory'),
    path('addcat',views.addcat,name = 'addcat'),
    path('addproducts',views.addproducts,name = 'addproducts'),
    path('addpro',views.addpro,name = 'addpro'),
    path('viewcategory',views.viewcategory,name = 'viewcategory'),
    path('viewproducts',views.viewproducts,name = 'viewproducts'),
    path('viewuser',views.viewuser,name = 'viewuser'),
    path('viewcontact',views.viewcontact,name = 'viewcontact'),
    path('vieworders',views.vieworders,name = 'vieworders'),
    path('delproducts/<int:id>',views.delproducts,name = 'delproducts'),
    path('delcat/<int:id>',views.delcat,name = 'delcat'),
    path('editcat/<int:id>',views.editcat,name = 'editcat'),
    path('editproducts/<int:id>',views.editproducts,name = 'editproducts'),
    path('updateproduct/<int:id>',views.updateproduct,name = 'updateproduct'),
    path('accept/<int:id>',views.accept,name = 'accept'),
    path('reject/<int:id>',views.reject,name = 'reject'),
    path('updatecat/<int:id>',views.updatecat,name = 'updatecat'),
    path('delmessage/<int:id>',views.delmessage,name = 'delmessage'),
    
]