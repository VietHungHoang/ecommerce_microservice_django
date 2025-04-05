# customers/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Customer, Address
from .serializers import CustomerSerializer, AddressSerializer, AddressCreateUpdateSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phép xem hoặc chỉnh sửa Customers.
    """
    queryset = Customer.objects.filter(is_active=True) # Chỉ lấy customer active
    serializer_class = CustomerSerializer
    lookup_field = 'id' # Sử dụng UUID làm khóa tra cứu

    # Có thể thêm các action tùy chỉnh ở đây nếu cần
    # Ví dụ: @action(detail=True, methods=['post']) ...

class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint cho phép xem hoặc chỉnh sửa Addresses.

    Lưu ý: Endpoint này hiện tại cho phép truy cập TẤT CẢ địa chỉ.
    Trong môi trường thực tế, bạn cần giới hạn quyền truy cập
    để người dùng chỉ thấy/sửa địa chỉ của chính họ (thường thông qua authentication/permissions).
    """
    queryset = Address.objects.all()
    lookup_field = 'id'

    # Sử dụng serializer khác nhau cho các hành động khác nhau
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AddressCreateUpdateSerializer
        return AddressSerializer # Sử dụng serializer gốc cho list/retrieve

    # Ghi đè phương thức create để sử dụng AddressCreateUpdateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        # Trả về dữ liệu bằng AddressSerializer (không có customer_id)
        read_serializer = AddressSerializer(address)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Ghi đè phương thức update để sử dụng AddressCreateUpdateSerializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        # Trả về dữ liệu bằng AddressSerializer
        read_serializer = AddressSerializer(address)
        return Response(read_serializer.data)

# === Cách tiếp cận thay thế: Quản lý Address như một nested resource của Customer ===
# Bạn có thể bỏ AddressViewSet ở trên và thêm các action vào CustomerViewSet như sau:
# (Yêu cầu cài đặt drf-nested-routers hoặc định nghĩa route thủ công)

# class CustomerViewSet(viewsets.ModelViewSet):
#     # ... (code CustomerViewSet như trên) ...

#     @action(detail=True, methods=['get', 'post'], url_path='addresses', serializer_class=AddressSerializer)
#     def addresses(self, request, id=None):
#         customer = self.get_object()
#         if request.method == 'GET':
#             addresses = Address.objects.filter(customer=customer)
#             serializer = AddressSerializer(addresses, many=True)
#             return Response(serializer.data)
#         elif request.method == 'POST':
#             # Sử dụng AddressCreateUpdateSerializer nhưng không cần customer_id vì đã có từ URL
#             serializer = AddressCreateUpdateSerializer(data=request.data, context={'customer': customer})
#             serializer.is_valid(raise_exception=True)
#             # Cần sửa đổi AddressCreateUpdateSerializer để nhận 'customer' từ context thay vì 'customer_id'
#             serializer.save() # Nên save customer trực tiếp
#             read_serializer = AddressSerializer(serializer.instance)
#             return Response(read_serializer.data, status=status.HTTP_201_CREATED)

#     @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path='addresses/(?P<address_id>[^/.]+)', serializer_class=AddressSerializer)
#     def address_detail(self, request, id=None, address_id=None):
#         customer = self.get_object()
#         address = get_object_or_404(Address, pk=address_id, customer=customer) # Đảm bảo address thuộc customer

#         if request.method == 'GET':
#             serializer = AddressSerializer(address)
#             return Response(serializer.data)
#         elif request.method in ['PUT', 'PATCH']:
#             partial = request.method == 'PATCH'
#             serializer = AddressCreateUpdateSerializer(address, data=request.data, partial=partial, context={'customer': customer})
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             read_serializer = AddressSerializer(serializer.instance)
#             return Response(read_serializer.data)
#         elif request.method == 'DELETE':
#             address.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

# -> Để đơn giản, chúng ta sẽ dùng AddressViewSet riêng biệt trước.