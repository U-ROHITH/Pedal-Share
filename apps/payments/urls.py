from django.urls import path
from apps.payments import views

app_name = 'payments'

urlpatterns = [
    path('wallet/', views.wallet, name='wallet'),
    path('topup/', views.topup_wallet, name='topup_wallet'),
    path('payment-gateway/<int:transaction_id>/', views.payment_gateway, name='payment_gateway'),
    path('process-payment/<int:transaction_id>/', views.process_payment, name='process_payment'),
    path('checkout/<int:booking_id>/', views.booking_checkout, name='checkout'),
    path('pay-with-wallet/<int:booking_id>/', views.pay_with_wallet, name='pay_with_wallet'),
]
