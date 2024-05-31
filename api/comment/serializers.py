from rest_framework import serializers

from common.comment.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'guid', 'user', 'product', 'content']

    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')

        if Comment.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already commented on this product.")
        return data

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError('Content cannot be empty')
        return value


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'guid', 'user', 'content']

