# AI Blind Assistant

Ứng dụng hỗ trợ người khiếm thị nhận biết môi trường xung quanh thông qua camera và cảnh báo nguy hiểm bằng giọng nói tiếng Việt.

## 1. Giới thiệu

AI Blind Assistant là dự án ứng dụng trí tuệ nhân tạo nhằm hỗ trợ người khiếm thị nhận biết các đối tượng và chướng ngại vật xuất hiện trong môi trường thực tế.

Hệ thống sử dụng camera để thu nhận hình ảnh, nhận diện đối tượng, ước lượng vị trí và khoảng cách tương đối, đánh giá mức độ nguy hiểm, sau đó phát cảnh báo bằng giọng nói.

## 2. Mục tiêu

- Nhận diện các đối tượng trong môi trường xung quanh.
- Phát hiện những chướng ngại vật có khả năng gây nguy hiểm.
- Xác định vị trí tương đối của đối tượng: bên trái, ở giữa, bên phải.
- Ước lượng khoảng cách tương đối: xa, gần, rất gần.
- Đánh giá mức độ nguy hiểm: thấp, trung bình, cao.
- Phát cảnh báo bằng giọng nói tiếng Việt.

**Lưu ý:** Hệ thống cung cấp thông tin cảnh báo để người dùng tự quyết định hướng di chuyển, không cung cấp chức năng dẫn đường.

## 3. Chức năng chính

### 3.1. Object Detection
- Sử dụng YOLOv8n để nhận diện đối tượng.
- Sử dụng trọng số mô hình đã fine-tune trên dataset SafeWalkBD.

### 3.2. Position Estimation
Xác định vị trí tương đối của đối tượng trong khung hình:
- Bên trái.
- Ở giữa.
- Bên phải.

### 3.3. Distance Estimation
Ước lượng khoảng cách tương đối dựa trên diện tích và chiều cao bounding box so với khung hình:
- Xa.
- Gần.
- Rất gần.

Đây là phương pháp ước lượng theo heuristic, không phải phép đo khoảng cách thực tế bằng mét.

### 3.4. Threat Assessment
Đánh giá mức độ nguy hiểm dựa trên vị trí và khoảng cách tương đối:
- Thấp.
- Trung bình.
- Cao.

### 3.5. Temporal Filtering
Lọc kết quả nhận diện qua nhiều frame nhằm hạn chế cảnh báo không ổn định.

### 3.6. Voice Alert
- Sử dụng giọng nói tiếng Việt.
- Quản lý thứ tự ưu tiên cảnh báo.
- Hạn chế phát cảnh báo lặp lại quá thường xuyên.
- Cho phép cảnh báo nguy hiểm cao hơn ngắt cảnh báo có mức độ thấp hơn.

## 4. Quy trình hoạt động

Camera → Object Detection → Position Estimation → Distance Estimation → Threat Assessment → Temporal Filtering → AlertManager → Voice Alert.

## 5. Công nghệ sử dụng

| Công nghệ | Mục đích |
|---|---|
| Python | Ngôn ngữ lập trình chính |
| PyTorch | Nền tảng học sâu |
| Ultralytics YOLOv8 | Nhận diện đối tượng |
| OpenCV | Xử lý hình ảnh và camera |
| NumPy | Xử lý dữ liệu hình ảnh |
| Pygame | Phát âm thanh cảnh báo |
| Edge-TTS | Tạo giọng nói tiếng Việt |

## 6. Dataset và mô hình

- Dataset: SafeWalkBD v9.
- Mô hình: YOLOv8n.
- Phương pháp: Fine-tuning mô hình YOLOv8n pretrained trên SafeWalkBD.
- File trọng số sử dụng: `best.pt`.

**Lưu ý:** Đây là mô hình được fine-tune từ trọng số pretrained, không phải mô hình được xây dựng và huấn luyện hoàn toàn từ đầu.

## 7. Cấu trúc dự án

```text
AI_Blind_Assistant/
│
├── datasets/       # Dataset
├── docs/           # Tài liệu dự án
├── outputs/        # File đầu ra, âm thanh
├── runs/           # Kết quả huấn luyện
├── src/
│   ├── alerts/     # Quản lý và phát cảnh báo
│   ├── camera/     # Xử lý camera và video
│   ├── data/       # Xử lý dữ liệu
│   ├── detection/  # Nhận diện và xử lý đối tượng
│   ├── models/     # Thành phần mô hình
│   ├── training/   # Huấn luyện mô hình
│   ├── utils/      # Các tiện ích hỗ trợ
│   └── main.py
│
├── tests/          # Kiểm thử
├── videos/         # Video thử nghiệm
├── weights/        # Trọng số mô hình
├── requirements.txt
├── README.md
└── .gitignore
```

## 8. Cài đặt và sử dụng

### 8.1. Yêu cầu hệ thống

- Windows 10/11 hoặc hệ điều hành tương thích.
- Python 3.13.14 (phiên bản đã sử dụng trong môi trường phát triển).
- Webcam nếu muốn chạy nhận diện trực tiếp.
- GPU NVIDIA được khuyến nghị để tăng tốc xử lý.

### 8.2. Tải dự án

```bash
git clone <GITHUB_REPOSITORY_URL>
cd AI_Blind_Assistant
```

### 8.3. Tạo môi trường Python

```bash
python -m venv .venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 8.4. Cài đặt PyTorch

Cài đặt PyTorch phù hợp với hệ điều hành và phần cứng.

Tham khảo hướng dẫn chính thức:

https://pytorch.org/get-started/locally/

### 8.5. Cài đặt các thư viện

```bash
pip install -r requirements.txt
```

### 8.6. Chuẩn bị trọng số mô hình

Đặt file `best.pt` đúng vị trí mà chương trình đang cấu hình.

Nếu không có file trọng số, hệ thống sẽ không thể tải mô hình đã fine-tune để nhận diện.

### 8.7. Khởi chạy chương trình

Chạy từ thư mục gốc của dự án:

```bash
python -m src.camera.camera
```

Sau khi khởi chạy, chương trình sẽ mở webcam và thực hiện nhận diện, xử lý cảnh báo.

Nhấn phím `Q` để thoát cửa sổ camera.

## 9. Giới hạn của hệ thống

- Khoảng cách được ước lượng tương đối từ bounding box, không phải khoảng cách vật lý chính xác.
- Độ chính xác nhận diện phụ thuộc vào chất lượng camera, ánh sáng và môi trường.
- Temporal Filtering hiện tại đối chiếu theo loại đối tượng và vùng vị trí, chưa phải thuật toán theo dõi từng đối tượng riêng biệt.
- Hệ thống chỉ đưa ra cảnh báo, không đảm bảo người dùng tránh được mọi nguy hiểm.
- Hiệu năng thực tế phụ thuộc vào phần cứng và môi trường chạy.

## 10. Định hướng phát triển

- Cải thiện độ chính xác nhận diện các chướng ngại vật.
- Tối ưu tốc độ xử lý video và webcam.
- Cải thiện cơ chế lọc và quản lý cảnh báo.
- Hoàn thiện giao diện và quy trình cài đặt.
- Thực hiện đánh giá hiệu năng trên nhiều tình huống thực tế.

## 11. Tác giả

AI Blind Assistant – Dự án ứng dụng trí tuệ nhân tạo hỗ trợ người khiếm thị.