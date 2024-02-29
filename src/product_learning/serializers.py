from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


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
        fields = ("id","name","lessons",)



class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("creator",)

    def create(self, validated_data):
        print("user.teacher", self.context["request"])
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
