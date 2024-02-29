from .models import *
from django.db.models import Count


def add_student_to_product(student: Student, product: Product):
    if student.products.filter(id=product.id).exists():
        raise Exception("Вы уже подписаны на этот курс")
    if student.balance < product.price:
        raise Exception("Недостаточно средств для подписки на выбранный курс")
    student.products.add(product)


def reshuffle_product_groups():
    """Перетасовка студентов в группах, если курс не начат еще"""


def subscribe_to_product(product_id: int, student: Student):
    """Алгоритм подписки студента на продукт
    Получить группы по курсу, если нето то создать
    получить макс мин челов в группе
    """
    product = Product.objects.get(id=product_id)
    success_responce = {"data": f"Вы успешно подписались на продукт {product.name}!"}
    add_student_to_product(student=student, product=product)
    product_groups = (
        product.product_groups.all()
        .annotate(students_count=Count("students"))
        .order_by("students_count")
    )
    if not product_groups: # создание первой группы 
        new_group = StudentGroup.objects.create(name="Группа 1", product=product)
        new_group.students.add(student)
        return success_responce
    for i, group in enumerate(product_groups): # распределение по умолчанию
        if group.students_count < product.max_group_size:
            group.students.add(student)
            return success_responce
        elif group.students_count == product.max_group_size:
            new_group = StudentGroup.objects.create(name=f"Группа {i}", product=product)
            new_group.students.add(student)
            return success_responce
