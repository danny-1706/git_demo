# FastAPI Demo Web

Dự án mẫu xây dựng ứng dụng web API bằng FastAPI với đầy đủ các phương thức HTTP và tính năng cơ bản:
- **GET**: Lấy danh sách (Query parameters: phân trang `skip`, `limit`, tìm kiếm `search`) và chi tiết theo ID (Path parameters).
- **POST**: Thêm dữ liệu mới với Request Body và kiểm tra định dạng qua Pydantic (`ItemCreate`).
- **PUT**: Cập nhật thông tin bản ghi theo ID (`ItemUpdate`).
- **DELETE**: Xóa bản ghi (trả về HTTP 204 No Content).
- Tự động sinh tài liệu OpenAPI / Swagger UI tại `/docs` và ReDoc tại `/redoc`.

---

## 🛠 Hướng dẫn cài đặt & chạy dự án

### 1. Tạo môi trường ảo (Virtual Environment)
```bash
python -m venv venv
```

Kích hoạt môi trường ảo:
- Trên **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- Trên **Windows (cmd)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- Trên **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Chạy server phát triển (Development Server)
```bash
uvicorn main:app --reload
```

Server sẽ chạy mặc định tại: `http://127.0.0.1:8000`

---

## 📌 Các đường dẫn chính (Endpoints)

| Phương thức | Đường dẫn | Chức năng |
|---|---|---|
| `GET` | `/` | Giao diện HTML trang chủ chào mừng |
| `GET` | `/items` | Danh sách sản phẩm (có query `skip`, `limit`, `search`) |
| `GET` | `/items/{item_id}` | Lấy chi tiết sản phẩm theo `item_id` |
| `POST` | `/items` | Thêm mới 1 sản phẩm |
| `PUT` | `/items/{item_id}` | Cập nhật thông tin sản phẩm |
| `DELETE` | `/items/{item_id}` | Xóa sản phẩm theo ID |
| `GET` | `/docs` | Tài liệu API tương tác Swagger UI |
| `GET` | `/redoc` | Tài liệu API ReDoc |
