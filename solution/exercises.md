# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Temperature càng thấp (0.0), câu trả lời càng an toàn, rập khuôn và ít biến đổi; temperature càng cao (1.0 - 1.5), văn phong càng sáng tạo, phong phú nhưng nếu quá cao sẽ dễ bị lan man hoặc sinh ra thông tin sai lệch (hallucination).*

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Nên đặt ở mức thấp (từ 0.0 đến 0.3). Vì chatbot hỗ trợ khách hàng cần sự chính xác tuyệt đối, nhất quán và bám sát tài liệu/chính sách của công ty thay vì tự do sáng tạo câu chữ.*

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *GPT-4o đắt hơn khoảng **16.67 lần** so với GPT-4o-mini. (Dựa trên đơn giá: $0.010 / $0.0006).*

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *- **GPT-4o xứng đáng khi:** Cần suy luận logic phức tạp, giải quyết bài toán lập trình khó, dịch thuật ngữ cảnh sâu hoặc phân tích biểu đồ/hình ảnh đa phương tiện.*
> *- **GPT-4o-mini tốt hơn khi:** Xử lý các tác vụ đơn giản, lặp lại với số lượng khổng lồ (ví dụ: phân loại bình luận, trích xuất từ khóa, tóm tắt văn bản ngắn) để tối ưu hóa chi phí.*

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming quan trọng nhất trong các ứng dụng chat tương tác trực tiếp với người dùng, giúp giảm cảm giác chờ đợi (độ trễ nhận thức thấp) khi LLM đang sinh ra một đoạn văn dài. Ngược lại, non-streaming phù hợp cho các tác vụ chạy ngầm (background jobs) như xử lý dữ liệu hàng loạt, dịch tự động toàn bộ file, hoặc khi hệ thống cần nhận trọn vẹn văn bản để parse ra file JSON/kiểm duyệt trước khi hiển thị.*


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
