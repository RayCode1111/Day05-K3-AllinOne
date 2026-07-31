# Feedback log — vòng validation CP5

⚠️ **File này nhóm phải tự điền bằng người thật.** Rubric R6 (8 điểm) chấm trực tiếp trên đây: cần **≥5 mẩu từ ≥5 người ngoài nhóm**, trong đó **≥2 người là willing user đã khai từ CP1**, quote **nguyên văn** kèm tên/vai.

## Cách chạy một phiên — 10 phút/người *(02-guide.md §4.2)*

1. **Giao task thật, rồi im lặng.** *"Hôm nay bạn nghỉ một buổi. Dùng cái này để biết bạn đã bỏ lỡ việc gì."* Không thuyết minh, không gợi ý. Ghi lại họ bấm gì, dừng ở đâu, hiểu nhầm chỗ nào.
2. **Hỏi đúng ba câu:**
   - Điều gì khó hiểu hoặc khó chịu nhất?
   - Kết quả này bạn có tin không — vì sao?
   - Bạn có dùng thật không — vì sao / vì sao chưa?
3. **Log nguyên văn.** Đừng diễn giải lại thành ý đẹp.

> Nếu mọi phản hồi đều là lời khen thì phiên test **chưa đạt** — giao task khó hơn hoặc đổi người thử.

## Bảng log

| # | Người thử (tên · vai · willing user?) | Task giao | Quan sát khi họ dùng | Quote nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## Bốn dòng tổng hợp

- **Chủ đề lặp nhiều nhất:** ⚠️ *(điền sau khi log đủ 5 mẩu — đọc lại cột Quote rồi gom, đừng viết trước)*

- **1-2 thay đổi làm trước demo** *(chép sang `spec.md` §9 Changelog):* ⚠️ *(điền — R6 chấm cao hơn cho thay đổi có thật so với lý do giữ nguyên)*

- **Giữ nguyên có lý do** *(ba quyết định này đã chép sang `spec.md` §9, dòng "CP5 — GIỮ NGUYÊN")*:

  1. **Không gộp mục *Cần xác thực* vào cuối danh sách việc.** Gộp lại xoá mất ranh giới giữa việc đã qua guard `_ground()` (có trích dẫn nguyên văn đỡ) và việc chưa đủ căn cứ. Người dùng này đã mute một kênh vì nó trộn lẫn tin quan trọng với tin thường — trộn lại lần nữa, lần này giữa *chắc* và *không chắc*, là lặp lại đúng lỗi đó ở mức nguy hiểm hơn. Bù lại: số mục cần xác nhận đã hiện sẵn trên thẻ hero màn *Hôm nay*.
  2. **Không để Nova tự chốt giờ cho cặp `thong-bao#15` / `#16`** (Workshop 4: 20:00 vs 19:00). Không có đáp án đúng trong data — cả hai đều là thông báo chính thức. Đoán đúng thì người học đỡ một câu hỏi; đoán sai thì họ vào Zoom sai giờ và mất điểm danh, không sửa được. Nova đặt hai trích dẫn cạnh nhau kèm câu hỏi soạn sẵn.
  3. **Không thêm luật prompt để sửa case G22.** Luật mới sẽ kéo cả nhóm tin hướng dẫn thao tác lên bản tin và làm bản tin dài ra — đúng thứ sản phẩm sinh ra để chống. `eval/rubric-cham.md` đã khai trước rằng loại nhầm này chấp nhận được. Đường lui đã có: cửa sổ 💬 Discord liệt kê cả tin bị lọc.

- **Đưa vào backlog** *(lên slide 6):* ⚠️ *(điền)*

## Gợi ý chỗ nên soi khi quan sát

Bốn chỗ nhóm nghi ngờ nhất — nếu người thử không tự vấp vào, hãy đẩy họ tới:

1. Họ có **hiểu mục *Chưa chắc — nên hỏi TA*** không, hay tưởng đó là việc phải làm?
2. Thấy huy hiệu 🛡️ *"Guard đã hạ cấp kết luận này"*, họ **tin hơn hay nghi ngờ hơn**?
3. Bản tin giới hạn 5 mục — họ có **thấy thiếu** không, hay thấy vừa?
4. Họ có bấm mở *"Đã lọc bỏ N tin"* để kiểm không, hay tin luôn?

## Ảnh workflow JTBD

⚠️ Chụp sơ đồ workflow nhóm vẽ ở §1 của spec và lưu tại `validation/workflow-jtbd.jpg`.
