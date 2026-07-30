# Nova — Student Command Center

Streamlit agent đọc các file trong `data/discord-pack`, gọi Gemini để trích xuất việc cần làm, rồi áp guard đối chiếu đoạn trích nguồn trước khi hiển thị.

## Chạy local trên Windows

```powershell
1. cd codebase
2. python -m venv .venv
3. .venv\Scripts\Activate
4. python -m pip install -r requirements.txt
5. cp .env.example .env
6. # Điền GOOGLE_API_KEY trong .env
7. streamlit run app.py
```

Nếu PowerShell chặn việc kích hoạt môi trường ảo, chỉ áp dụng cho cửa sổ hiện tại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Điều kiện môi trường

- `APP_ENV`: `development` hoặc `production` (mặc định: `development`).
- `GEMINI_MODEL`: model Gemini để phân tích (mặc định `gemini-3.6-flash`).
- `APP_DATA_MODE`: `live` để quét `data/discord-pack`; `mock` chỉ cho chế độ minh hoạ.
- `.env` và `.streamlit/secrets.toml` không được commit.
