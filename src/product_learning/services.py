from django.db.models import Count
from datetime import date
from .models import *


def add_student_to_product(student: Student, product: Product):
    """Добавление студента на продукт и списание денег"""
    if student.products.filter(id=product.id).exists():
        raise Exception("Вы уже подписаны на этот курс")
    if student.balance < product.price:
        raise Exception("Недостаточно средств для подписки на выбранный курс")
    student.balance -= product.price
    student.save()
    student.products.add(product)


def subscribe_to_product(product_id: int, student: Student):
    """Алгоритм подписки студента на продукт"""
    product = Product.objects.get(id=product_id)
    success_responce = {"data": f"Вы успешно подписались на продукт {product.name}!"}
    add_student_to_product(student=student, product=product)
    product_groups = (
        product.product_groups.all()
        .annotate(students_count=Count("students"))
        .order_by("students_count")
    )
    if not product_groups:  # создание первой группы
        new_group = StudentGroup.objects.create(name="Группа 1", product=product)
        new_group.students.add(student)
        return success_responce
    if (
        product.min_group_size >= product.max_group_size / 2
        or product.start_date < date.today()
    ):  # распределение по умолчанию если курс начат или равномерно невозможно распределить
        for i, group in enumerate(product_groups):
            if group.students_count < product.max_group_size:
                group.students.add(student)
                return success_responce
            elif group.students_count == product.max_group_size:
                new_group = StudentGroup.objects.create(
                    name=f"Группа {i+1}", product=product
                )
                new_group.students.add(student)
                return success_responce
    else:  # равномерное распределение
        if (
            product_groups.first().students_count + 1
        ) % product.min_group_size == 0 and (
            product_groups.first().students_count + 1
        ) / product.min_group_size > 1:
            new_group = StudentGroup.objects.create(
                name=f"Группа {len(product_groups)+1}", product=product
            )
        else:
            student.groups.add(product_groups.first())
            return success_responce
        for i, group in enumerate(product_groups.all()):
            if i == product.min_group_size:
                break
            for j, old_student in enumerate(group.students.all()):
                if j == product.min_group_size:
                    break
                old_student.groups.add(new_group)
                old_student.groups.remove(group)
        student.groups.add(product_groups.first())
        return success_responce
