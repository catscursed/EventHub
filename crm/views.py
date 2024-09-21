from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render
from product.models import Order


@user_passes_test(lambda user: user.is_admin or user.status == 3, login_url='index')  # доступ есть только у админа
# и бухгалтера
def order_list_view(request):
    orders = Order.objects.all().order_by('-id')  # -id для того чтобы в таблице сверху самые последние покупки

    income = orders.aggregate(total=Sum('total_price'))['total']  # подс

    return render(
        request=request,
        template_name='crm/order_list.html',
        context={
            'orders': orders,
            'income': income
        }
    )
