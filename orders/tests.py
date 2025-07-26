from django.test import TestCase

# Create your tests here.
# from django.test import TestCase, override_settings
# from django.core import mail
# from unittest.mock import patch, MagicMock, ANY # ANY �������, ����� ������ �������� ��������� �� �����
#
# from orders.models import Order
# from orders.tasks import sent_email_after_order_created, order_created
#
# # �� ���������� override_settings, �����:
# # 1. CELERY_TASK_ALWAYS_EAGER = True: ������ Celery ����� ����������� ���������, ����������,
# #    ����� �� ����� ��������� �� ��������� ����� � �����, ��� ������� worker-�.
# # 2. EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend': Django ����� ���������
# #    ��� ������������ ������ � ������ mail.outbox, ������ ���� ����� ���������� �� ��-����������.
# @override_settings(
#     CELERY_TASK_ALWAYS_EAGER=True,
#     EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
# )
# class CeleryTaskTests(TestCase):
#     def setUp(self):
#         # ������� �������� �����, ������� ����� �������������� � �������
#         self.order = Order.objects.create(
#             customer_name='�������� ������',
#             customer_email='test@example.com',
#             total_price=123.45,
#             # �������� ���� ������ ����, ������� ����� ��� �������� ������ ������
#             # ��������: address='123 Test St', city='Testville', postal_code='12345'
#         )
#
#     def test_sent_email_after_order_created_task(self):
#         """
#         ��������� ������ sent_email_after_order_created,
#         ������� ���������� ������� ������.
#         """
#         # �������� ������ Celery, ��� ���������� ���������
#         # ��-�� CELERY_TASK_ALWAYS_EAGER
#         sent_email_after_order_created(self.order.id)
#
#         # ���������, ��� ���� ���������� ���� ������
#         self.assertEqual(len(mail.outbox), 1)
#         email = mail.outbox[0]
#
#         # ��������� ���������� ������
#         self.assertEqual(
#             email.subject, f"��� ����� #{self.order.id} ������� ��������!"
#         )
#         self.assertIn(f"���������(��) {self.order.customer_name}", email.body)
#         self.assertEqual(email.to, [self.order.customer_email])
#         self.assertEqual(
#             email.from_email, 'alekseykhitrov@gmail.com'
#         ) # ���������, ��� ��� ������������� ������ DEFAULT_FROM_EMAIL
# from django.test import TestCase, override_settings
# from django.core import mail
# from unittest.mock import patch, MagicMock, ANY # ANY �������, ����� ������ �������� ��������� �� �����
#
# from orders.models import Order
# from orders.tasks import sent_email_after_order_created, order_created
#
# # �� ���������� override_settings, �����:
# # 1. CELERY_TASK_ALWAYS_EAGER = True: ������ Celery ����� ����������� ���������, ����������,
# #    ����� �� ����� ��������� �� ��������� ����� � �����, ��� ������� worker-�.
# # 2. EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend': Django ����� ���������
# #    ��� ������������ ������ � ������ mail.outbox, ������ ���� ����� ���������� �� ��-����������.
# @override_settings(
#     CELERY_TASK_ALWAYS_EAGER=True,
#     EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
# )
# class CeleryTaskTests(TestCase):
#     def setUp(self):
#         # ������� �������� �����, ������� ����� �������������� � �������
#         self.order = Order.objects.create(
#             customer_name='�������� ������',
#             customer_email='test@example.com',
#             total_price=123.45,
#             # �������� ���� ������ ����, ������� ����� ��� �������� ������ ������
#             # ��������: address='123 Test St', city='Testville', postal_code='12345'
#         )
#
#     def test_sent_email_after_order_created_task(self):
#         """
#         ��������� ������ sent_email_after_order_created,
#         ������� ���������� ������� ������.
#         """
#         # �������� ������ Celery, ��� ���������� ���������
#         # ��-�� CELERY_TASK_ALWAYS_EAGER
#         sent_email_after_order_created(self.order.id)
#
#         # ���������, ��� ���� ���������� ���� ������
#         self.assertEqual(len(mail.outbox), 1)
#         email = mail.outbox[0]
#
#         # ��������� ���������� ������
#         self.assertEqual(
#             email.subject, f"��� ����� #{self.order.id} ������� ��������!"
#         )
#         self.assertIn(f"���������(��) {self.order.customer_name}", email.body)
#         self.assertEqual(email.to, [self.order.customer_email])
#         self.assertEqual(
#             email.from_email, 'alekseykhitrov@gmail.com'
#         ) # ���������, ��� ��� ������������� ������ DEFAULT_FROM_EMAIL