from rest_framework import serializers
from django.db.models import Avg, Count
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductStatsSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    fullness_percent = serializers.SerializerMethodField()
    purchase_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("name", "student_count", "fullness_percent", "purchase_percent")

    def get_student_count(self, obj):
        return obj.students.count()

    def get_fullness_percent(self, obj):
        average_student_in_group = (
            obj.product_groups.all()
            .annotate(students_count=Count("students"))
            .aggregate(Avg("students_count", default=0))
        )["students_count__avg"]
        return average_student_in_group / obj.max_group_size * 100

    def get_purchase_percent(self, obj):
        return obj.students.count() / Student.objects.count() * 100


class ProductListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("name", "creator", "start_date", "stop_date", "price", "lesson_count")

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class ProductWithLessonsSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "lessons",
        )


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("creator",)

    def create(self, validated_data):
        product = Product.objects.create(
            creator=self.context["request"].user.teacher, **validated_data
        )
        return product


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("creator",)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
