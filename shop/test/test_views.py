from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from shop.models import Product, Cart, CartItem

from shop.views import remove_item_cart


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Create a session
        self.session = self.client.session
        self.session['cart_id'] = 'test_cart_id'
        self.session.save()

        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            image='products/test.jpg'
        )

        # Create a cart
        self.cart = Cart.objects.create(cart_id='test_cart_id')

        # Create a cart item
        self.cart_item = CartItem.objects.create(product=self.product, cart=self.cart, quantity=1)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_service_view(self):
        response = self.client.get(reverse('service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/service.html')

    def test_shop_single_view(self):
        response = self.client.get(reverse('shop_single', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_single/shop_single.html')
        self.assertContains(response, self.product.name)

    def test_shop_view(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop.html')
        self.assertContains(response, self.product.name)

    def test_order_view(self):
        response = self.client.get(reverse('order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order.html')

    def test_cart_str_method(self):
        """Test string representation of cart"""
        cart = Cart.objects.create(cart_id='test_cart_id')
        self.assertEqual(str(cart), 'test_cart_id')

    def test_cart_view(self):
        """Test cart view"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')