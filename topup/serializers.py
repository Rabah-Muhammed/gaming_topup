from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TopUpProduct, Game, TopUpOrder, UserProfile, PaymentTransaction
import uuid



class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    preferred_game = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(), required=False, write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'date_of_birth', 'preferred_game']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data.pop('phone_number')
        dob = validated_data.pop('date_of_birth')
        preferred_game = validated_data.pop('preferred_game', None)

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            phone_number=phone,
            date_of_birth=dob,
            preferred_game=preferred_game
        )
        return user

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "message": "User registered successfully"
        }



class TopUpOrderSerializer(serializers.Serializer):
    gamename = serializers.CharField()
    game_id = serializers.CharField()
    product_name = serializers.CharField()
    product_id = serializers.IntegerField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        try:
            game = Game.objects.get(name=data['gamename'], game_id=data['game_id'], is_active=True)
        except Game.DoesNotExist:
            raise serializers.ValidationError("Game not found or inactive.")

        try:
            product = TopUpProduct.objects.get(
                id=data['product_id'],
                name=data['product_name'],
                game=game,
                price=data['product_price']
            )
        except TopUpProduct.DoesNotExist:
            raise serializers.ValidationError("Product not found or doesn't match the game.")

        data['product'] = product
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        order = TopUpOrder.objects.create(
            user_email=user.email,
            product=validated_data['product']
        )

        PaymentTransaction.objects.create(
            topup_order=order,
            transaction_id=str(uuid.uuid4()),
            provider="SimulatedProvider"
        )

        return order