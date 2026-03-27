# Safe-Lab Simulator - Phòng Thí Nghiệm An Toàn Huấn Luyện Bảo Vệ

**Hệ thống mô phỏng hoàn toàn an toàn cho huấn luyện bảo vệ mạng và kỹ thuật phát hiện tấn công**

---

## 📋 Tổng Quan

Dự án này là một phòng thí nghiệm mô phỏng dành cho:

- Huấn luyện bảo vệ mạng (Defensive Security Training)
- Phát triển kỹ thuật phát hiện tấn công (Detection Engineering)
- Tập huấn về phản ứng sự cố (Incident Response)

### ✅ Đặc Điểm An Toàn

- **Mô phỏng hoàn toàn**: Không thực hiện tấn công thực tế
- **Lệnh được kiểm soát**: Danh sách lệnh an toàn được xác định sẵn
- **Liên kết local**: Mặc định chỉ kết nối tới `127.0.0.1`
- **Ghi nhật ký cấu trúc**: Tất cả các hành động được ghi lại chi tiết
- **Công tắc dừng khẩn cấp**: Có thể kích hoạt bằng `LAB_KILL_SWITCH=true`

---

## 🚀 Hướng Dẫn Bắt Đầu Nhanh (5 phút)

### Bước 1: Cài đặt môi trường

```bash
pip install -r requirements.txt
```

### Bước 2: Kiểm tra cấu hình

```bash
python lab/deploy.py
```

Lệnh này sẽ kiểm tra các yêu cầu an toàn trước khi chạy.

### Bước 3: Khởi động Server Điều Phối (Orchestrator)

```bash
python orchestrator/api.py
```

Server chính sẽ chạy trên `http://127.0.0.1:5000`

### Bước 4: Khởi động Dịch Vụ Mục Tiêu (trong terminal khác)

```bash
python target/app.py
```

Dịch vụ mục tiêu chạy trên `http://127.0.0.1:5001`

### Bước 5: Chạy Demo An Toàn

```bash
python lab/demo.py
```

Demo này minh họa các lệnh mô phỏng an toàn.

### Bước 6: Khởi động Giám Sát (Monitor)

```bash
python target/monitor.py
```

Công cụ này giám sát và ghi lại các sự kiện từ dịch vụ mục tiêu.

---

## 📖 Cấu Trúc Dự Án

```
ddos-botnet-lab/
├── core/                          # Cấu hình và bảo mật cốt lõi
│   ├── config.py                  # Biến môi trường
│   ├── safety.py                  # Các quy tắc bảo mật
│   ├── schemas.py                 # Định dạng dữ liệu
│   └── types.py                   # Kiểu dữ liệu
├── orchestrator/                  # Máy chủ điều phối lệnh
│   ├── api.py                     # API REST chính
│   ├── command_router.py          # Định tuyến lệnh
│   └── session_registry.py        # Quản lý phiên làm việc
├── simulator/                     # Công cụ mô phỏng
│   ├── agents/                    # Các tác nhân mô phỏng
│   └── telemetry/                 # Sinh sự kiện & phát lại kịch bản
├── observability/                 # Ghi nhật ký và số liệu
│   ├── audit_logger.py            # Ghi nhật ký kiểm tra
│   └── metrics_collector.py       # Thu thập số liệu
├── target/                        # Ứng dụng mục tiêu
│   ├── app.py                     # Dịch vụ web
│   └── monitor.py                 # Công cụ giám sát
├── datasets/                      # Dữ liệu kịch bản
│   └── replay_scenarios/          # Các kịch bản phát lại
│       ├── baseline.jsonl         # Kịch bản cơ sở
│       ├── sdn_flow_anomaly.jsonl # Kịch bản bất thường lưu lượng
│       ├── sdn_control_plane_stress.jsonl  # Kịch bản căng thẳng điều khiển
│       └── sdn_recovery_drill.jsonl        # Kịch bản phục hồi
├── tests/                         # Bài kiểm tra
│   ├── unit/                      # Kiểm tra đơn vị
│   ├── integration/               # Kiểm tra tích hợp
│   └── safety/                    # Kiểm tra an toàn
└── docs/                          # Tài liệu
```

---

## 🎮 Cách Sử Dụng Hệ Thống

### 1. Kiểm Tra Trạng Thái Hệ Thống

```bash
curl http://127.0.0.1:5000/api/health
```

### 2. Liệt Kê Các Tác Nhân Đang Hoạt Động

```bash
curl http://127.0.0.1:5000/api/agents
```

### 3. Xem Các Kịch Bản Có Sẵn

```bash
curl http://127.0.0.1:5000/api/scenarios
```

### 4. Xem Chi Tiết Một Kịch Bản

```bash
curl http://127.0.0.1:5000/api/scenarios/sdn_flow_anomaly
```

### 5. Gửi Lệnh (POST Request)

**Endpoint**: `POST http://127.0.0.1:5000/api/command`

**Ví dụ - Ping tác nhân**:

```json
{
  "command": "ping",
  "agent_id": "agent-001",
  "issued_by": "trainer"
}
```

**Ví dụ - Phát lại kịch bản phát hiện bất thường**:

```json
{
  "command": "replay_detection_scenario",
  "agent_id": "agent-001",
  "issued_by": "trainer",
  "args": {
    "scenario_name": "sdn_flow_anomaly",
    "duration_seconds": 30
  }
}
```

---

## ✨ Lệnh An Toàn Được Phép

Hệ thống chỉ cho phép 5 lệnh an toàn:

| Lệnh                        | Mô Tả                                    |
| --------------------------- | ---------------------------------------- |
| `ping`                      | Kiểm tra xem tác nhân có hoạt động không |
| `report_status`             | Lấy trạng thái hiện tại của tác nhân     |
| `simulate_state_transition` | Mô phỏng chuyển đổi trạng thái           |
| `simulate_load_profile`     | Mô phỏng hồ sơ tải                       |
| `replay_detection_scenario` | Phát lại kịch bản phát hiện từ dataset   |

**Bất kỳ lệnh nào khác sẽ bị từ chối và ghi lại.**

---

## 📊 Các Kịch Bản SDN Có Sẵn

Hệ thống bao gồm 4 kịch bản mô phỏng mạng SDN an toàn:

### 1. **baseline** - Kịch Bản Cơ Sở

- Dữ liệu bình thường để so sánh
- Không có bất thường

### 2. **sdn_flow_anomaly** - Bất Thường Lưu Lượng

- Mô phỏng sự tăng trưởng bảng lưu lượng
- Độ trễ hàng đợi tăng lên
- **Đặc điểm**: Phát hiện tăng trưởng bảng luồng

### 3. **sdn_control_plane_stress** - Căng Thẳng Mặt Phẳng Điều Khiển

- Mô phỏng CPU điều khiển tăng cao
- Độ trễ API tăng lên
- Tăng đột biến gói tin
- **Đặc điểm**: Phát hiện quá tải điều khiển

### 4. **sdn_recovery_drill** - Tập Huấn Phục Hồi

- Mô phỏng chuyển đổi dự phòng (failover)
- Chuỗi phục hồi
- **Đặc điểm**: Thực hành phục hồi sự cố

---

## 👥 Vai Trò Người Dùng

Hệ thống hỗ trợ 2 vai trò:

| Vai Trò    | Quyền                             |
| ---------- | --------------------------------- |
| `viewer`   | Chỉ đọc: `ping`, `report_status`  |
| `operator` | Toàn quyền: tất cả 5 lệnh an toàn |

---

## 🔍 Quy Trình Vận Hành Chuẩn

### Quy Trình Mục Tiêu:

1. ✅ Kiểm tra sức khỏe: `GET /api/health`
2. ✅ Liệt kê tác nhân: `GET /api/agents`
3. ✅ Xem kịch bản: `GET /api/scenarios`
4. ✅ Xem chi tiết kịch bản: `GET /api/scenarios/<scenario_name>`
5. ✅ Gửi lệnh mô phỏng: `POST /api/command`
6. ✅ Kiểm tra nhật ký: Đọc file `lab_audit.jsonl`

### Thực Hành Tốt Nhất:

- **Sử dụng correlation_id**: Theo dõi từng bài tập
- **Xem xét nhật ký kiểm tra**: Sau mỗi lần chạy, kiểm tra `lab_audit.jsonl`
- **Khởi động công tắc dừng**: Nếu có hành vi bất thường, đặt `LAB_KILL_SWITCH=true`

### Thứ Tự Chạy Kịch Bản Được Đề Nghị:

1. **Trước tiên**: `sdn_flow_anomaly` - Phát hiện bất thường lưu lượng
2. **Sau đó**: `sdn_control_plane_stress` - Phát hiện quá tải
3. **Cuối cùng**: `sdn_recovery_drill` - Thực hành phục hồi

---

## 🛡️ Các Yêu Cầu An Toàn Bắt Buộc

Hệ thống yêu cầu thỏa mãn ba điều kiện an toàn:

```
SIMULATE_ONLY=true          # Chỉ mô phỏng, không thực hiện
BIND_HOST=127.0.0.1         # Chỉ lắng nghe trên localhost
ALLOWLISTED_SUBNETS=127.0.0.0/8  # Chỉ cho phép mạng local
```

Nếu bất kỳ yêu cầu nào không được thỏa mãn, hệ thống sẽ từ chối khởi động.

---

## 📝 Ví Dụ Hoàn Chỉnh

### Chạy Một Bài Tập Hoàn Chỉnh

**Terminal 1 - Khởi động Server**:

```bash
python orchestrator/api.py
```

**Terminal 2 - Khởi động Dịch Vụ Mục Tiêu**:

```bash
python target/app.py
```

**Terminal 3 - Khởi động Giám Sát**:

```bash
python target/monitor.py
```

**Terminal 4 - Chạy Các Lệnh**:

```bash
# Kiểm tra sức khỏe
curl http://127.0.0.1:5000/api/health

# Liệt kê kịch bản
curl http://127.0.0.1:5000/api/scenarios

# Gửi lệnh bắt đầu kịch bản
curl -X POST http://127.0.0.1:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "replay_detection_scenario",
    "agent_id": "sdn-agent-1",
    "issued_by": "instructor",
    "args": {
      "scenario_name": "sdn_flow_anomaly",
      "duration_seconds": 60
    },
    "correlation_id": "exercise-001"
  }'

# Kiểm tra nhật ký kiểm tra
cat lab_audit.jsonl
```

---

## 📚 Tài Liệu Chi Tiết

Để hiểu sâu hơn, xem các file trong thư mục `docs/`:

- [docs/setup-guide.md](docs/setup-guide.md) - Hướng dẫn cài đặt chi tiết
- [docs/usage-guide.md](docs/usage-guide.md) - Hướng dẫn sử dụng API
- [docs/operator-guide.md](docs/operator-guide.md) - Hướng dẫn vận hành
- [docs/safety-policy.md](docs/safety-policy.md) - Chính sách an toàn
- [docs/architecture.md](docs/architecture.md) - Kiến trúc hệ thống
- [docs/incident-stop-procedure.md](docs/incident-stop-procedure.md) - Quy trình dừng khẩn cấp

---

## 🧪 Chạy Kiểm Tra

```bash
# Kiểm tra toàn bộ bộ kiểm tra
python -m pytest tests/

# Chỉ kiểm tra an toàn
python -m pytest tests/safety/

# Chỉ kiểm tra đơn vị
python -m pytest tests/unit/

# Chỉ kiểm tra tích hợp
python -m pytest tests/integration/
```

---

## ⚠️ Xử Lý Sự Cố

### Nếu gặp lỗi bất thường:

1. **Kích hoạt công tắc dừng**:

   ```bash
   export LAB_KILL_SWITCH=true
   ```

2. **Kiểm tra nhật ký**:

   ```bash
   tail -f lab_audit.jsonl
   ```

3. **Xem chi tiết lỗi**:
   - Kiểm tra terminal nơi server đang chạy
   - Tìm tin nhắn lỗi trong `lab_audit.jsonl`

4. **Khởi động lại hệ thống**:
   ```bash
   # Dừng tất cả các quy trình (Ctrl+C)
   # Sau đó khởi động lại từ bước 3 trong "Hướng dẫn bắt đầu nhanh"
   ```

---

## 📞 Hỗ Trợ

- Kiểm tra thư mục `docs/` để có hướng dẫn chi tiết
- Xem `docs/faq.md` cho các câu hỏi thường gặp
- Kiểm tra `lab_audit.jsonl` để tìm nguồn gốc vấn đề

---

## ✅ Kiểm Danh Sách Lần Đầu Tiên Sử Dụng

- [ ] Cài đặt Python 3.10+
- [ ] Cài đặt các gói (pip install -r requirements.txt)
- [ ] Chạy kiểm tra cấu hình (python lab/deploy.py)
- [ ] Khởi động orchestrator và dịch vụ mục tiêu
- [ ] Chạy demo an toàn (python lab/demo.py)
- [ ] Thử ghi các lệnh POST để kiểm tra
- [ ] Xem nhật ký kiểm tra (lab_audit.jsonl)
- [ ] Đọc tài liệu bảo mật (docs/safety-policy.md)

---

**Chúc bạn huấn luyện hiệu quả! 🎓**
