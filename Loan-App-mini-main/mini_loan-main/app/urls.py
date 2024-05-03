from django.urls import path
from . import views

urlpatterns = [
    path('create_loan/', views.create_loan, name='create_loan'),
    path('approve_loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('change_loan_status/<int:loan_id>',views.change_loan_status, name='change_loan_status'),
    path('view_loans/', views.view_loans, name='loan_view'),
    path('add_repayment/<int:loan_id>/', views.add_repayment, name='add_repayment'),
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
