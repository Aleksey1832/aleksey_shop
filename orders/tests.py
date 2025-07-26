from django.test import TestCase

# Create your tests here.
# from django.test import TestCase, override_settings
# from django.core import mail
# from unittest.mock import patch, MagicMock, ANY # ANY полезен, когда точное значение аргумента не важно
#
# from orders.models import Order
# from orders.tasks import sent_email_after_order_created, order_created
#
# # Мы используем override_settings, чтобы:
# # 1. CELERY_TASK_ALWAYS_EAGER = True: Задачи Celery будут выполняться синхронно, немедленно,
# #    чтобы мы могли проверить их результат прямо в тесте, без запуска worker-а.
# # 2. EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend': Django будет сохранять
# #    все отправленные письма в список mail.outbox, вместо того чтобы отправлять их по-настоящему.
# @override_settings(
#     CELERY_TASK_ALWAYS_EAGER=True,
#     EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
# )
# class CeleryTaskTests(TestCase):
#     def setUp(self):
#         # Создаем тестовый заказ, который будет использоваться в задачах
#         self.order = Order.objects.create(
#             customer_name='Тестовый Клиент',
#             customer_email='test@example.com',
#             total_price=123.45,
#             # Добавьте сюда другие поля, которые нужны для создания вашего заказа
#             # Например: address='123 Test St', city='Testville', postal_code='12345'
#         )
#
#     def test_sent_email_after_order_created_task(self):
#         """
#         Тестирует задачу sent_email_after_order_created,
#         которая отправляет простое письмо.
#         """
#         # Вызываем задачу Celery, она выполнится синхронно
#         # из-за CELERY_TASK_ALWAYS_EAGER
#         sent_email_after_order_created(self.order.id)
#
#         # Проверяем, что было отправлено одно письмо
#         self.assertEqual(len(mail.outbox), 1)
#         email = mail.outbox[0]
#
#         # Проверяем содержимое письма
#         self.assertEqual(
#             email.subject, f"Ваш заказ #{self.order.id} успешно оформлен!"
#         )
#         self.assertIn(f"Уважаемый(ая) {self.order.customer_name}", email.body)
#         self.assertEqual(email.to, [self.order.customer_email])
#         self.assertEqual(
#             email.from_email, 'alekseykhitrov@gmail.com'
#         ) # Убедитесь, что это соответствует вашему DEFAULT_FROM_EMAIL
# from django.test import TestCase, override_settings
# from django.core import mail
# from unittest.mock import patch, MagicMock, ANY # ANY полезен, когда точное значение аргумента не важно
#
# from orders.models import Order
# from orders.tasks import sent_email_after_order_created, order_created
#
# # Мы используем override_settings, чтобы:
# # 1. CELERY_TASK_ALWAYS_EAGER = True: Задачи Celery будут выполняться синхронно, немедленно,
# #    чтобы мы могли проверить их результат прямо в тесте, без запуска worker-а.
# # 2. EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend': Django будет сохранять
# #    все отправленные письма в список mail.outbox, вместо того чтобы отправлять их по-настоящему.
# @override_settings(
#     CELERY_TASK_ALWAYS_EAGER=True,
#     EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
# )
# class CeleryTaskTests(TestCase):
#     def setUp(self):
#         # Создаем тестовый заказ, который будет использоваться в задачах
#         self.order = Order.objects.create(
#             customer_name='Тестовый Клиент',
#             customer_email='test@example.com',
#             total_price=123.45,
#             # Добавьте сюда другие поля, которые нужны для создания вашего заказа
#             # Например: address='123 Test St', city='Testville', postal_code='12345'
#         )
#
#     def test_sent_email_after_order_created_task(self):
#         """
#         Тестирует задачу sent_email_after_order_created,
#         которая отправляет простое письмо.
#         """
#         # Вызываем задачу Celery, она выполнится синхронно
#         # из-за CELERY_TASK_ALWAYS_EAGER
#         sent_email_after_order_created(self.order.id)
#
#         # Проверяем, что было отправлено одно письмо
#         self.assertEqual(len(mail.outbox), 1)
#         email = mail.outbox[0]
#
#         # Проверяем содержимое письма
#         self.assertEqual(
#             email.subject, f"Ваш заказ #{self.order.id} успешно оформлен!"
#         )
#         self.assertIn(f"Уважаемый(ая) {self.order.customer_name}", email.body)
#         self.assertEqual(email.to, [self.order.customer_email])
#         self.assertEqual(
#             email.from_email, 'alekseykhitrov@gmail.com'
#         ) # Убедитесь, что это соответствует вашему DEFAULT_FROM_EMAIL