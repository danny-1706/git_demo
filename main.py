from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Demo Web",
    description="Ứng dụng FastAPI cơ bản minh họa đầy đủ các phương thức HTTP (GET, POST, PUT, DELETE)",
    version="1.0.0"
)

# ----------------- Models -----------------
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Tên sản phẩm")
    description: Optional[str] = Field(None, max_length=300, description="Mô tả chi tiết")
    price: float = Field(..., gt=0, description="Giá sản phẩm (phải lớn hơn 0)")
    is_available: bool = Field(True, description="Trạng thái còn hàng hay không")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None

class Item(ItemBase):
    id: int

# In-memory database (dữ liệu mẫu)
fake_db: dict[int, Item] = {
    1: Item(id=1, name="Bàn phím cơ", description="Bàn phím cơ switch blue", price=750000.0, is_available=True),
    2: Item(id=2, name="Chuột không dây", description="Chuột công thái học", price=450000.0, is_available=True),
    3: Item(id=3, name="Màn hình 24 inch", description="Tấm nền IPS 144Hz", price=3200000.0, is_available=False),
}

# ----------------- Routes / Endpoints -----------------

@app.get("/", response_class=HTMLResponse, tags=["General"])
def read_root():
    """Trang chủ hiển thị giao diện chào mừng & link tới tài liệu Swagger UI."""
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>FastAPI Demo Web</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #009688; }
            .btn { display: inline-block; padding: 10px 18px; margin: 5px; background: #009688; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
            .btn:hover { background: #00796b; }
            ul { background: #f5f5f5; padding: 20px 35px; border-radius: 8px; }
            code { background: #e0e0e0; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🚀 FastAPI Demo Web Application</h1>
        <p>Ứng dụng đã khởi chạy thành công với đầy đủ các phương thức CRUD cơ bản!</p>
        
        <h3>Các phương thức có sẵn:</h3>
        <ul>
            <li><code>GET /items</code> - Lấy danh sách sản phẩm (hỗ trợ phân trang & tìm kiếm)</li>
            <li><code>GET /items/{id}</code> - Lấy chi tiết một sản phẩm theo ID</li>
            <li><code>POST /items</code> - Thêm sản phẩm mới</li>
            <li><code>PUT /items/{id}</code> - Cập nhật thông tin sản phẩm</li>
            <li><code>DELETE /items/{id}</code> - Xóa sản phẩm</li>
        </ul>

        <p>
            <a class="btn" href="/docs" target="_blank">Xem Swagger UI (/docs)</a>
            <a class="btn" href="/redoc" target="_blank" style="background: #2b7bb9;">Xem ReDoc (/redoc)</a>
        </p>
    </body>
    </html>
    """

# 1. GET (Read all) - kèm Query Parameters
@app.get("/items", response_model=List[Item], tags=["Items"])
def get_items(
    skip: int = Query(0, ge=0, description="Bỏ qua số lượng bản ghi"),
    limit: int = Query(10, ge=1, le=50, description="Giới hạn số lượng bản ghi trả về"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên sản phẩm")
):
    """Lấy danh sách các sản phẩm kèm bộ lọc tìm kiếm và phân trang."""
    items = list(fake_db.values())
    if search:
        items = [item for item in items if search.lower() in item.name.lower()]
    return items[skip : skip + limit]

# 2. GET (Read one) - kèm Path Parameter
@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(
    item_id: int = Path(..., ge=1, description="ID của sản phẩm cần lấy")
):
    """Lấy thông tin chi tiết một sản phẩm theo ID."""
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Không tìm thấy sản phẩm có ID = {item_id}"
        )
    return fake_db[item_id]

# 3. POST (Create) - nhận dữ liệu từ Request Body
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item_data: ItemCreate):
    """Tạo mới một sản phẩm."""
    new_id = max(fake_db.keys(), default=0) + 1
    new_item = Item(id=new_id, **item_data.model_dump())
    fake_db[new_id] = new_item
    return new_item

# 4. PUT (Update) - cập nhật toàn bộ hoặc từng phần thông tin
@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(
    item_id: int = Path(..., ge=1, description="ID sản phẩm cần sửa"),
    item_data: ItemUpdate = ...
):
    """Cập nhật thông tin của một sản phẩm."""
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm có ID = {item_id}"
        )
    
    current_item = fake_db[item_id]
    update_data = item_data.model_dump(exclude_unset=True)
    updated_item = current_item.model_copy(update=update_data)
    
    fake_db[item_id] = updated_item
    return updated_item

# 5. DELETE (Delete) - xóa một bản ghi
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def delete_item(
    item_id: int = Path(..., ge=1, description="ID của sản phẩm cần xóa")
):
    """Xóa một sản phẩm theo ID."""
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm có ID = {item_id}"
        )
    del fake_db[item_id]
    return None
