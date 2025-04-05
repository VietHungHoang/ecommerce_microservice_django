# Sử dụng base image Python chính thức.
FROM python:3.10-slim

# Đặt các biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1 # Ngăn Python ghi file .pyc
ENV PYTHONUNBUFFERED 1       # Đảm bảo output của Python được ghi trực tiếp ra terminal mà không cần buffer

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu có, ví dụ: build-essential libpq-dev cho psycopg2)
# psycopg2-binary thường không cần, nhưng nếu gặp lỗi, hãy uncomment dòng dưới
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Cài đặt dependencies
# Copy file requirements trước để tận dụng Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn ứng dụng vào thư mục làm việc
COPY . .

# (Tùy chọn) Thu thập static files nếu ứng dụng Django của bạn có phục vụ static files trực tiếp
# RUN python manage.py collectstatic --noinput

# Expose port mà ứng dụng sẽ chạy bên trong container
EXPOSE 8000

# Lệnh để chạy ứng dụng khi container khởi động
# Sử dụng Gunicorn cho production. Có thể thay bằng 'python manage.py runserver 0.0.0.0:8000' để debug.
CMD ["gunicorn", "customer_service.wsgi:application", "--bind", "0.0.0.0:8000"]