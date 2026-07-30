# Nova — Student Command Center

Prototype Streamlit quản lý công việc học tập bằng dữ liệu giả. Không gọi AI, Discord hay VLearn thật.

## Cấu trúc

```text
codebase/
├── app.py                 # Ứng dụng Streamlit hiện tại
├── requirements.txt       # Thư viện cần cài
├── .env.example           # Mẫu biến môi trường an toàn
├── .streamlit/config.toml # Theme và cổng chạy local
└── legacy_agent/          # Mã agent/eval cũ, tách riêng khỏi prototype
```

## Chạy local trên Windows

```powershell
cd codebase
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Nếu PowerShell chặn việc kích hoạt môi trường ảo, chỉ áp dụng cho cửa sổ hiện tại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Điều kiện môi trường

- `APP_ENV`: `development` hoặc `production` (mặc định: `development`).
- `APP_DATA_MODE`: phải là `mock` vì bản này chỉ sử dụng dữ liệu giả.
- `.env` và `.streamlit/secrets.toml` không được commit.
