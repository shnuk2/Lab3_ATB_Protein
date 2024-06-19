from django.test import TestCase  # Импортируем класс TestCase из Django для создания тестов
from shop.models import Product, Cart, CartItem  # Импортируем модели Product, Cart и CartItem из приложения shop

# Класс для тестирования модели Product
class ProductModelTest(TestCase):
    # Метод setUp вызывается перед каждым тестом для создания тестового окружения
    def setUp(self):
        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name="Test Product",  # Устанавливаем имя продукта
            description="This is a test product",  # Устанавливаем описание продукта
            price=99.99,  # Устанавливаем цену продукта
            image="products/test.png",  # Устанавливаем путь к изображению продукта
            rating=4,  # Новое поле для рейтинга, устанавливаем значение 4
            specifications="Test specifications"  # Новое поле для спецификаций, устанавливаем тестовые спецификации
        )

    # Тест для проверки правильности создания продукта
    def test_product_creation(self):
        # Проверяем, что имя продукта установлено правильно
        self.assertEqual(self.product.name, "Test Product")
        # Проверяем, что описание продукта установлено правильно
        self.assertEqual(self.product.description, "This is a test product")
        # Проверяем, что цена продукта установлена правильно
        self.assertEqual(self.product.price, 99.99)
        # Проверяем, что путь к изображению продукта установлен правильно
        self.assertEqual(self.product.image, "products/test.png")
        # Проверяем, что рейтинг продукта установлен правильно
        self.assertEqual(self.product.rating, 4)
        # Проверяем, что спецификации продукта установлены правильно
        self.assertEqual(self.product.specifications, "Test specifications")

    # Тест для проверки строкового представления продукта
    def test_product_str(self):
        # Проверяем, что строковое представление продукта равно его имени
        self.assertEqual(str(self.product), "Test Product")

# Класс для тестирования модели Cart
class CartModelTest(TestCase):
    # Метод setUp вызывается перед каждым тестом для создания тестового окружения
    def setUp(self):
        # Создаем тестовую корзину
        self.cart = Cart.objects.create(cart_id="test_cart")

    # Тест для проверки правильности создания корзины
    def test_cart_creation(self):
        # Проверяем, что идентификатор корзины установлен правильно
        self.assertEqual(self.cart.cart_id, "test_cart")

    # Тест для проверки строкового представления корзины
    def test_cart_str(self):
        # Проверяем, что строковое представление корзины равно ее идентификатору
        self.assertEqual(str(self.cart), "test_cart")

# Класс для тестирования модели CartItem
class CartItemModelTest(TestCase):
    # Метод setUp вызывается перед каждым тестом для создания тестового окружения
    def setUp(self):
        # Создаем продукт для тестирования
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.0  # Устанавливаем цену продукта
        )
        # Создаем корзину для тестирования
        self.cart = Cart.objects.create(cart_id="test_cart")

        # Создаем элемент корзины для тестирования
        self.cart_item = CartItem.objects.create(
            product=self.product,  # Устанавливаем продукт для элемента корзины
            cart=self.cart,  # Устанавливаем корзину для элемента корзины
            quantity=1  # Устанавливаем количество элемента корзины
        )
    
    # Тест для проверки правильности создания элемента корзины
    def test_cart_item_creation(self):
        # Проверяем, что продукт в элементе корзины установлен правильно
        self.assertEqual(self.cart_item.product, self.product)
        # Проверяем, что корзина в элементе корзины установлена правильно
        self.assertEqual(self.cart_item.cart, self.cart)
        # Проверяем, что количество элемента корзины установлено правильно
        self.assertEqual(self.cart_item.quantity, 1)
        # Проверяем, что элемент корзины активен
        self.assertTrue(self.cart_item.is_active)

    # Тест для проверки подсчета подытога элемента корзины
    def test_cart_item_sub_total(self):
        # Проверяем, что подытог элемента корзины вычисляется правильно
        self.assertEqual(self.cart_item.sub_total(), self.product.price * self.cart_item.quantity)

    # Тест для проверки строкового представления элемента корзины
    def test_cart_item_str(self):
        # Ожидаемое строковое представление элемента корзины — это название продукта
        expected_str = self.cart_item.product.name
        # Проверяем, что строковое представление элемента корзины соответствует ожиданиям
        self.assertEqual(str(self.cart_item), expected_str)