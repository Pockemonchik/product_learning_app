from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    """Модель преподавателя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    balance = models.IntegerField(default=0, verbose_name="Баланс преподавателя")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["-id"]

    def __str__(self):
        return str(self.user.username)


class Product(models.Model):
    """Модель продукта по которму обучаются"""

    creator = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Создатель продукта",
    )
    name = models.CharField(max_length=150, verbose_name="Название продукта")
    start_date = models.DateField(
        null=True, blank=True, verbose_name="Дата старта продукта"
    )
    stop_date = models.DateField(
        null=True, blank=True, verbose_name="Дата остановки продукта"
    )
    price = models.IntegerField(default=0, verbose_name="Стоимость продукта")

    max_group_size = models.IntegerField(
        default=5, verbose_name="Максимум студентов в группе"
    )
    min_group_size = models.IntegerField(
        default=1, verbose_name="Минимум студентов в группе"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Student(models.Model):
    """Модель студента"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, verbose_name="Баланс студента")
    products = models.ManyToManyField(
        Product,
        related_name="products",
        verbose_name="Продукты студента",
        blank=True,
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["-id"]

    def __str__(self):
        return str(self.user.username)


class Lesson(models.Model):
    """Модель урока по продукту"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Продукт урока",
    )
    theme = models.CharField(max_length=150, verbose_name="Тема урока")
    video_url = models.URLField(max_length=150, verbose_name="Ссылка на видео урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["-id"]

    def __str__(self):
        return f"Урок {str(self.theme)} продукта {self.product.name}"


class StudentGroup(models.Model):
    """Модель группы студентов на продукте"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_groups",verbose_name="Продукт группы"
    )
    name = models.CharField(max_length=150, verbose_name="Название группы")

    students = models.ManyToManyField(
        Student,
        related_name="groups",
        verbose_name="Студенты в группе",
        blank=True,
    )

    class Meta:
        verbose_name = "Группа студентов"
        verbose_name_plural = "Группы студентов"
        ordering = ["-id"]

    def __str__(self):
        return f"Группа {str(self.name)} продукта {self.product.name}"
