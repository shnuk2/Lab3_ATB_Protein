# views.py
from django.shortcuts import render, get_object_or_404, redirect  # Импортируем функции для рендеринга шаблонов и получения объектов
from django.core.exceptions import ObjectDoesNotExist  # Импортируем исключение для работы с объектами, которые могут не существовать
from .models import Product, Cart, CartItem  # Импортируем модели Product, Cart и CartItem
from django.http import HttpResponse  # Импортируем класс HttpResponse

# Обработчик для главной страницы
def index(request):
    return render(request, 'index/index.html')  # Рендерим шаблон index.html

# Обработчик для страницы "О нас"
def about(request):
    return render(request, 'about/about.html')  # Рендерим шаблон about.html

# Обработчик для страницы контактов
def contact(request):
    return render(request, 'contact/contact.html')  # Рендерим шаблон contact.html

# Обработчик для страницы услуг
def service(request):
    return render(request, 'service/service.html')  # Рендерим шаблон service.html

# Обработчик для страницы с деталями продукта
def shop_single(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID или возвращаем 404
    context = {
        'product': product,  # Передаем продукт в контексте
    }
    return render(request, 'shop_single/shop_single.html', context)  # Рендерим шаблон shop_single.html с контекстом

# Обработчик для страницы магазина
def shop(request):
    query = request.GET.get('query', '')  # Получаем поисковый запрос из GET-параметра
    if query:
        products = Product.objects.filter(name__icontains=query)  # Фильтруем товары по названию
    else:
        products = Product.objects.all()  # Получаем все товары, если поисковый запрос отсутствует
    context = {
        'products': products,  # Передаем товары в контексте
    }
    return render(request, 'shop/shop.html', context)  # Рендерим шаблон shop.html с контекстом

# Вспомогательная функция для получения идентификатора корзины
def _cart_id(request):
    cart = request.session.session_key  # Получаем ключ сессии
    if not cart:
        cart = request.session.create()  # Создаем новый ключ сессии, если его нет
    return cart

# Обработчик для добавления продукта в корзину
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Получаем продукт по ID
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Получаем корзину по идентификатору сессии
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))  # Создаем корзину, если она не существует
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)  # Получаем элемент корзины
        cart_item.quantity += 1  # Увеличиваем количество, если элемент уже есть в корзине
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)  # Создаем элемент корзины, если его нет
        cart_item.save()
    return redirect('cart')  # Перенаправляем на страницу корзины

# Обработчик для удаления одного элемента продукта из корзины
def remove_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Получаем корзину по идентификатору сессии
    except Cart.DoesNotExist:
        cart = None
    
    if cart:
        product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID или возвращаем 404
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)  # Получаем элемент корзины
            if cart_item.quantity > 1:
                cart_item.quantity -= 1  # Уменьшаем количество, если оно больше 1
                cart_item.save()
            else:
                cart_item.delete()  # Удаляем элемент корзины, если количество равно 1
        except CartItem.DoesNotExist:
            pass
    
    return redirect('cart')  # Перенаправляем на страницу корзины

# Обработчик для полного удаления продукта из корзины
def remove_item_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Получаем корзину по идентификатору сессии
    product = get_object_or_404(Product, id=product_id)  # Получаем продукт по ID или возвращаем 404
    cart_item = CartItem.objects.get(product=product, cart=cart)  # Получаем элемент корзины
    cart_item.delete()  # Удаляем элемент корзины
    return redirect('cart')  # Перенаправляем на страницу корзины

# Обработчик для отображения корзины
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Получаем корзину по идентификатору сессии
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Получаем активные элементы корзины
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Подсчитываем общую стоимость
            quantity += cart_item.quantity  # Подсчитываем общее количество
        tax = (2 * total) / 100  # Рассчитываем налог (2% от общей стоимости)
        grand_total = total + tax  # Рассчитываем итоговую сумму
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,  # Общая стоимость
        'quantity': quantity,  # Общее количество
        'cart_items': cart_items,  # Элементы корзины
        'tax': tax,  # Налог
        'grand_total': grand_total  # Итоговая сумма
    }
    return render(request, 'cart/cart.html', context)  # Рендерим шаблон cart.html с контекстом

# Обработчик для страницы заказа
def order(request):
    return render(request, 'order/order.html')  # Рендерим шаблон order.html