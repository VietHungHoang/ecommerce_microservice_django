# customers/serializers.py
from rest_framework import serializers
from .models import Customer, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = '__all__' # Bao gồm cả customer id
        exclude = ('customer',) # Loại trừ trường customer vì nó sẽ được xử lý ở CustomerSerializer hoặc qua URL

class CustomerSerializer(serializers.ModelSerializer):
    # Sử dụng nested serializer để hiển thị địa chỉ khi đọc thông tin customer
    # Chỉ đọc (read_only=True) vì việc tạo/cập nhật địa chỉ nên qua endpoint riêng của Address
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number',
                  'is_active', 'created_at', 'updated_at', 'addresses', 'password']
        read_only_fields = ('id', 'created_at', 'updated_at', 'addresses')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}} # Không hiển thị password khi đọc, chỉ cho ghi
        }

    def create(self, validated_data):
        # Hash password before creating customer
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer

    def update(self, instance, validated_data):
        # Hash password nếu nó được cung cấp trong request update
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        # Cập nhật các trường khác như bình thường
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# Serializer riêng cho việc tạo/cập nhật Address, yêu cầu customer_id
class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    customer_id = serializers.UUIDField(write_only=True) # Nhận customer_id khi tạo/update

    class Meta:
        model = Address
        fields = ['id', 'customer_id', 'street_address', 'city', 'state',
                  'postal_code', 'country', 'is_default_shipping', 'is_default_billing']
        read_only_fields = ('id',)

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"customer_id": "Customer not found."})

        # Xử lý logic đặt địa chỉ mặc định (ví dụ)
        if validated_data.get('is_default_shipping'):
            Address.objects.filter(customer=customer, is_default_shipping=True).update(is_default_shipping=False)
        if validated_data.get('is_default_billing'):
            Address.objects.filter(customer=customer, is_default_billing=True).update(is_default_billing=False)

        address = Address.objects.create(customer=customer, **validated_data)
        return address

    def update(self, instance, validated_data):
         # Lấy customer từ instance, không cần customer_id trong payload khi update
        customer = instance.customer
        validated_data.pop('customer_id', None) # Bỏ qua customer_id nếu có trong payload

        # Xử lý logic đặt địa chỉ mặc định khi update
        if validated_data.get('is_default_shipping') and not instance.is_default_shipping:
            Address.objects.filter(customer=customer, is_default_shipping=True).exclude(pk=instance.pk).update(is_default_shipping=False)
        if validated_data.get('is_default_billing') and not instance.is_default_billing:
            Address.objects.filter(customer=customer, is_default_billing=True).exclude(pk=instance.pk).update(is_default_billing=False)

        return super().update(instance, validated_data)