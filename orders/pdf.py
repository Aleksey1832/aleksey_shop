import os
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf(order):
    font_path = os.path.join(settings.BASE_DIR, settings.PDF_ORDER_FONT)
    buffer = BytesIO()

    try:
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        pdf = canvas.Canvas(buffer)

        # оформление pdf-документа
        pdf.setFont('Arial', 14)
        pdf.drawString(100, 750, 'Детали заказа:')
        pdf.drawString(100, 730, f'Заказ № {order.id}')
        pdf.drawString(100, 710, f'Клиент: {order.first_name} {order.last_name}')
        pdf.drawString(100, 690, f'Сумма: {order.get_total_cost():.2f} руб.')
        pdf.save()
        buffer.seek(0)
        print("ok")
        # return buffer
        return buffer.getvalue()

    except FileNotFoundError:
        return f'Шрифт {font_path} не найден'

    except Exception as e:
        return f'Ошибка при генерации PDF: {e}'

    finally:
        buffer.close()
