# Định nghĩa "tốt" — ba chiều chất lượng

> Mục đích của file này: **người ngoài nhóm cầm file này chấm lại phải ra cùng kết quả**.
> Nếu hai người chấm lệch nhau, lỗi thuộc về định nghĩa ở đây, không thuộc về người chấm — sửa định nghĩa rồi ghi vào `spec.md` §9.
>
> Cách chưng cất (theo `02-guide.md` §2.6): nhóm chạy tay 12 tin qua prompt nháp, đọc từng output, gom lỗi thành nhóm có tên, rồi mới viết ba chiều dưới đây. Ba chiều này **không** nghĩ ra từ đầu.

## Chiều 1 — Đúng mức *(pass/fail)*

Agent xếp tin vào đúng mức mà nhãn vàng ghi trong `golden-set.csv`.

| Mức | Định nghĩa kiểm chứng được |
|---|---|
| `NGAY` | Tin có sự việc/hạn chót cách **thời điểm tin được gửi** (`ts`) **dưới 12 giờ** |
| `HOM_NAY` | Cách `ts` **từ 12 đến 48 giờ**, hoặc là việc phải làm trong ngày |
| `GHI_NHO` | Cách `ts` **trên 48 giờ**, hoặc có việc nhưng tin không nêu mốc thời gian nào |
| `BO_QUA` | Không có việc nào người học phải làm, hoặc việc đã trôi qua so với ngày tham chiếu |

**Cách chấm:** đọc `ts` của tin và mốc thời gian nêu trong tin, tính hiệu số, tra bảng. Không dùng cảm nhận "cái này quan trọng".

**Ranh giới đã chốt để không tranh cãi:**
- Đúng 12 giờ tròn → `HOM_NAY` (biên dưới thuộc mức nhẹ hơn).
- Tin nêu mốc mơ hồ ("cuối tuần", "sớm nhé") → luôn `GHI_NHO`, không bao giờ tự quy ra ngày.
- Tin từ học viên nói về lịch/hạn → mức cao nhất là `GHI_NHO`, bất kể nội dung nghe khẩn thế nào.

## Chiều 2 — Căn cứ truy vết được *(pass/fail)*

Đạt khi **cả ba** điều sau đúng:

1. Không có cờ bịa nào trong `co`: `trich_dan_khong_khop`, `han_chot_khong_can_cu`.
2. Nếu kết luận có `han_chot` thì bắt buộc có `trich_dan` đỡ bên dưới.
3. `trich_dan` là **chuỗi con nguyên văn** của `noi_dung` tin gốc (bỏ qua khác biệt hoa/thường và dấu cách).

**Cách chấm:** mở tin gốc bằng nút *Xem tin gốc* trong app (hoặc tra `msg_id` trong `codebase/fixtures/`), dùng Ctrl+F tìm đúng chuỗi `trich_dan`. Tìm thấy → đạt. Không tìm thấy → trượt. Không cần hiểu nội dung.

Điều kiện 3 được kiểm tự động bởi guard G-B trong `codebase/triage.py`; `codebase/test_guards.py` kiểm chính guard đó.

## Chiều 3 — Đường lui đúng *(pass/fail)*

Đạt khi: case có `phai_hoi_ta = co` trong golden set thì kết luận phải có `hoi_ta` khác rỗng.

Ba nhóm case bắt buộc có đường lui:
- **Lớp ①** — tin đồn từ học viên về lịch/hạn.
- **Lớp ②** — nguồn chính thức nhưng mốc thời gian mơ hồ.
- **Lớp ③** — yêu cầu ngoài thẩm quyền (xin đáp án, xin nghỉ hộ, hỏi điểm, xin bài nhóm khác).

**Cách chấm:** nhìn trường `hoi_ta` có nội dung hay không. Không chấm câu hỏi hay/dở ở chiều này — chỉ chấm có/không.

## Test độ rõ của định nghĩa *(guide §2.6 bước 4)*

Trước khi dùng bộ này chấm, hai thành viên chấm **độc lập** 5 output rồi so:

| Case thử | Người 1 | Người 2 | Khớp? |
|---|---|---|---|
| G04 | | | |
| G10 | | | |
| G11 | | | |
| G14 | | | |
| G24 | | | |

Lệch ≥1 case → định nghĩa chưa đủ rõ, viết lại mục tương ứng ở trên rồi thử lại. *(Bảng này nhóm điền tay trước CP3.)*

## Quality bar — chốt 23:59 30/07/2026, không đổi sau đó

> **Đạt khi cả ba điều kiện cùng đúng:**
> 1. **≥80%** case trong golden set đúng mức *(chiều 1)*
> 2. **Recall mức `NGAY` = 100%** — không bỏ sót bất kỳ tin khẩn nào
> 3. **0 case bịa căn cứ** *(chiều 2, điều kiện 1)*

**Vì sao hai điều kiện cứng chứ không chỉ một con số %:**

- **Bỏ sót tin khẩn là hậu quả không sửa được.** Học viên đến nhầm phòng, hoặc đến lúc lớp đã huỷ, thì bản tin đúng 95% cũng vô nghĩa. Khảo sát: **7/11** người đã dính đúng lỗi này.
- **Bịa căn cứ phá thứ duy nhất khiến agent đáng tin.** Người dùng ở đây đã mute server một lần rồi; một hạn chót bịa là mất họ vĩnh viễn.

Ngưỡng 80% ở chiều 1 đặt thấp hơn hai điều kiện cứng có chủ đích: nhóm chấp nhận agent xếp nhầm `GHI_NHO` ↔ `HOM_NAY` (người học chỉ đọc chậm hơn một chút), nhưng **không** chấp nhận bỏ sót khẩn hoặc bịa.
