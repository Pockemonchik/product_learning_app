from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from config.settings import *
from .permissions import *
from .serializers import *
from .models import *
from .services import subscribe_to_product


class ProductsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с продуктами.
    """

    queryset = Product.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        elif self.action == "create":
            permission_classes += [IsTeacherPermission]
        elif self.action == "update":
            permission_classes += [IsPoductOwnerPermission]
        elif self.detail == True and self.request.method == "GET":
            permission_classes += [
                IsPoductOwnerPermission | IsStudentInProrductPermission
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            serializer_class = ProductListSerializer
        elif self.action == "create":
            serializer_class = CreateProductSerializer
        elif self.action == "update":
            serializer_class = UpdateProductSerializer
        elif self.detail == True and self.request.method == "GET":
            serializer_class = ProductWithLessonsSerializer
        else:
            serializer_class = None
        return serializer_class

    @action(detail=True, methods=["post"], permission_classes=[IsStudentPermission])
    def subscribe(self, request, pk=None):
        try:
            res = subscribe_to_product(product_id=pk, student=request.user.student)
            return Response(data=res, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=ProductStatsSerializer,
    )
    def stats(self, request, pk=None):
        try:
            products = Product.objects.all()
            serializer = ProductStatsSerializer(products, many=True)
            return Response(data=serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
