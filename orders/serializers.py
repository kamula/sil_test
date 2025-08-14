# orders/serializers.py
from rest_framework import serializers
from products.models import Product
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "price"]
        extra_kwargs = {"id": {"read_only": True}}

    def validate(self, data):
        product = data["product"]
        if str(data["price"]) != str(product.price):
            raise serializers.ValidationError(
                {"price": f"Price must match product price: {product.price}"}
            )
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "items", "total_amount", "created_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "total_amount": {"read_only": True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data["product"]

            if product.stock < item_data["quantity"]:
                raise serializers.ValidationError(
                    {
                        "stock": f"Not enough stock for {product.name}. Available: {product.stock}"
                    }
                )

            product.stock -= item_data["quantity"]
            product.save()

            OrderItem.objects.create(order=order, **item_data)

        return order
