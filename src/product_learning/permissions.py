from rest_framework import permissions
from .models import *


class IsStudentPermission(permissions.BasePermission):
    """
    Проверяет студент ли пользователь
    """

    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsTeacherPermission(permissions.BasePermission):
    """
    Проверяет преподавтель ли пользователь
    """

    def has_permission(self, request, view):
        print(self, view)
        return Teacher.objects.filter(user=request.user).exists()


class IsPoductOwnerPermission(permissions.BasePermission):
    """
    Проверяет что пользователь создатель курса
    """

    def has_permission(self, request, view):
        teacher = Teacher.objects.filter(
            user=request.user
        ).first()
        if not teacher:
            return False
        return Product.objects.filter(
            creator=request.user.teacher, id=view.kwargs["pk"]
        ).exists()


class IsStudentInProrductPermission(permissions.BasePermission):
    """
    Проверяет что студент имеет доступ к продукту
    """

    def has_permission(self, request, view):
        student = Student.objects.filter(
            user=request.user
        ).first()
        if not student:
            return False
        return Student.objects.filter(
            user=request.user, products__in=[view.kwargs["pk"]]
        ).exists()
