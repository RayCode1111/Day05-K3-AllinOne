# Log bằng chứng — chạy lại được

Sinh tự động bằng `python codebase/evidence.py --ghi`. Sửa tay file này là vô nghĩa: chạy lại lệnh trên sẽ ghi đè. Con số trong `spec.md` §1-§2 phải khớp với file này.

## Đường A — khảo sát nhóm tự chạy

- Nguồn thô: `eval/survey-responses.csv` (n = **11**, form ẩn danh — không thu tên, không thu email).
- Chuẩn A của đề bài đòi **≥20 người ngoài nhóm**. Hiện **n = 11** → **CHƯA ĐẠT, còn thiếu 9 người**.

### Câu hỏi đã hỏi (nguyên văn)

1. 1. Trung bình mỗi ngày bạn dành bao nhiêu thời gian để check/tìm kiếm các thông báo, tài liệu học tập trên server Discord chung?
2. 2. Bạn có thường xuyên bị "miss" (bỏ lỡ) các thông tin quan trọng trên Discord không?
3. 3. Những loại thông tin nào bạn thường dễ bị bỏ lỡ nhất?
4. 4.Theo bạn, nguyên nhân chính dẫn đến việc bị lỡ thông tin là gì?
5. 5. Việc lỡ thông tin hoặc mất thời gian tìm kiếm trên Discord đã gây ra hậu quả gì cho bạn?
6. 6. Nếu có một AI Agent tự động đọc server chung và gửi một bản "Tóm tắt thông tin quan trọng trong ngày" cho bạn, bạn đánh giá mức độ hữu ích của nó như thế nào?
7. 7. Bạn kỳ vọng AI Agent này sẽ có những tính năng nào nhất
8. 8. Bạn muốn AI Agent tương tác/nhắc nhở bạn qua hình thức nào để bạn dễ chú ý nhất?

### Q2 — Mức độ bị bỏ lỡ thông tin (thang 1-5)

| Mức | Số người |
|---|---|
| 1 | 3 |
| 3 | 2 |
| 4 | 4 |
| 5 | 2 |

**Xác nhận có pain (chọn ≥3/5): 8/11 = 72.7%** → vượt ngưỡng ≥50% của chuẩn A. Trung bình 3.18/5.

### Q5 — Hậu quả đã thực sự xảy ra *(đây là phần đắt nhất của khảo sát)*

| Hậu quả | Số người | Tỉ lệ |
|---|---|---|
| Gây stress, lo lắng, lúc nào cũng sợ mình bỏ lỡ thông tin quan trọng (FOMO) | 9/11 | 81.8% |
| Bị trừ điểm / Trễ deadline nộp bài | 8/11 | 72.7% |
| Đi nhầm phòng học / Đến lớp khi đã được nghỉ | 7/11 | 63.6% |
| Phải đi hỏi lại bạn bè/lớp trưởng liên tục gây phiền phức | 6/11 | 54.5% |

### Q4 — Nguyên nhân

| Nguyên nhân | Số người | Tỉ lệ |
|---|---|---|
| Tin nhắn quan trọng bị "trôi" do mọi người chat/thảo luận quá nhiều | 9/11 | 81.8% |
| Server có quá nhiều kênh (channels), không biết tìm ở đâu | 9/11 | 81.8% |
| Phải tắt thông báo (Mute) vì bị spam (VD: @everyone, @here liên tục) | 7/11 | 63.6% |
| Đọc thông báo rồi nhưng sau đó lại quên mất do không note lại | 7/11 | 63.6% |

### Q3 — Loại tin dễ bỏ lỡ nhất

| Loại tin | Số người | Tỉ lệ |
|---|---|---|
| Thông báo thay đổi lịch học / lịch thi / phòng học đột xuất | 9/11 | 81.8% |
| Link tải tài liệu, slide bài giảng do Giảng viên/Trợ giảng gửi | 8/11 | 72.7% |
| Thông báo đăng ký tín chỉ, nộp học phí, giấy tờ hành chính | 6/11 | 54.5% |
| Các thông báo sự kiện, ngoại khóa có tính điểm rèn luyện | 6/11 | 54.5% |
| Deadline nộp bài tập / đồ án / bài thu hoạch | 6/11 | 54.5% |

### Q7 — Tính năng mong đợi

| Tính năng | Số người | Tỉ lệ |
|---|---|---|
| Deadline Reminder: Nhắc nhở nhắc lại khi sắp đến hạn chót (VD: "Bạn ơi, còn 12h nữa là đến hạn nộp bài môn A") | 9/11 | 81.8% |
| Urgent Alert (Cảnh báo khẩn): Gửi tin nhắn ngay lập tức nếu có thay đổi khẩn cấp (VD: Nghỉ học đột xuất, đổi phòng thi) | 8/11 | 72.7% |
| Daily Digest: Gửi tin nhắn tóm tắt ngắn gọn các sự kiện/thông báo quan trọng vào một giờ cố định mỗi ngày (VD: 8h tối) | 7/11 | 63.6% |
| Lọc theo tag môn học: Chỉ nhận thông báo của những môn mình đang học, bỏ qua các môn khác | 3/11 | 27.3% |

### Q8 — Kênh nhắc mong muốn

| Kênh | Số người | Tỉ lệ |
|---|---|---|
| Tag tên bạn vào một kênh (channel) #nhac-viec riêng tư trên server | 10/11 | 90.9% |
| Nhắn tin trực tiếp (Direct Message - DM) trên Discord cho tài khoản của bạn | 6/11 | 54.5% |
| Đẩy thông báo qua nền tảng khác (VD: Zalo, Email, Telegram) | 4/11 | 36.4% |
| Khác: [Điền vào chỗ trống] | 1/11 | 9.1% |

### Giới hạn của khảo sát — nhóm tự khai

1. **n = 11 < 20** → chưa đạt chuẩn A. Nhóm phải thu thêm 9 phản hồi trước khi chốt spec.
2. **Câu 6 là câu hỏi dẫn dắt.** "Nếu có một AI Agent… bạn đánh giá mức độ hữu ích" đúng vào lỗi mà `02-guide.md` §1.3 cảnh báo — hầu như ai cũng trả lời cao. Nhóm **không dùng Q6 làm bằng chứng pain**; chỉ dùng Q2 (mức bị miss), Q4 (nguyên nhân) và Q5 (hậu quả đã xảy ra).
3. Q3/Q4/Q5/Q7/Q8 là câu chọn nhiều đáp án từ danh sách có sẵn → có thiên lệch theo lựa chọn nhóm đưa ra. Vòng validation CP5 dùng câu hỏi mở để bù.

## Đường B — mining data pack Discord *(thông báo THẬT của khoá)*

Tiêu chí đếm — viết ra để tranh luận được, không giấu trong đầu người đếm:

- Ranh giới giữa hai thông báo: khoảng trống **từ 2 dòng trống trở lên** (regex `\n{3,}`). Xuống đoạn trong cùng một thông báo chỉ cách 1 dòng trống, nên ngưỡng này tách đúng tin thay vì cắt vụn tin dài.
- Tin **có việc phải làm**: khớp regex `hạn|deadline|hết hạn|trước ngày|nộp|gia hạn|đóng đúng|due`.
- Tin **ping cả lớp**: khớp regex `@everyone|@here|@Learner|@Lab Coach`.

| Chỉ số | Giá trị |
|---|---|
| Tổng số thông báo trong pack | 28 |
| Tin có việc phải làm kèm hạn | 6/28 = 21.4% |
| Tin ping cả lớp (@everyone/@here/@Learner) | 13/28 = 46.4% |
| **Tin ping cả lớp nhưng KHÔNG kèm việc phải làm** | **11/13 = 85%** |
| Độ dài thông báo (trung bình · trung vị · dài nhất) | 625 · 579 · 1941 ký tự |
| Thông báo dài hơn 500 ký tự | 17/28 |

**Hai con số đáng giá nhất:**

1. **11/13 (85%) tin ping cả lớp không kèm việc phải làm.** Đây là bằng chứng **độc lập với khảo sát** cho đúng nguyên nhân mà 7/11 người khảo sát khai là lý do họ phải mute. Khảo sát nói người dùng *cảm thấy* bị spam; pack cho thấy họ *bị spam thật*.
2. **Thông báo dài trung bình 625 ký tự, 17/28 tin dài hơn 500 ký tự.** Chỉ 6/28 tin thật sự có việc phải làm — tức là học viên phải đọc rất nhiều chữ để tìm ra phần nhỏ thật sự liên quan tới mình. Đó đúng là việc mà bản tin lọc gánh hộ.

**Chỉ số đã thử nhưng KHÔNG dùng — khai để khỏi bị hiểu là chọn số đẹp:** nhóm định đo *"hạn chót bị chôn sâu trong thân bài"*, nhưng đo ra hạn xuất hiện trung bình ở **23%** chiều dài tin và chỉ **1/7** tin phải đọc quá nửa mới thấy hạn. Giả thuyết đó **không được data ủng hộ**, nên bỏ, không đưa vào spec.

> Không dán nguyên văn dài từ data pack vào repo này theo luật bảo mật (`.gitignore` chặn `data/`). Chỉ giữ số đếm và tiêu chí đếm.
