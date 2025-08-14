from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'parent_name']
        extra_kwargs = {'id': {'read_only': True}}

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None