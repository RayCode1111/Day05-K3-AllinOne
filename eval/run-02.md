# Lượt đo 02 — 2026-07-30 16:32

- Prompt: `codebase/prompts/triage.md` version **v3**
- Model: `gemini-2.5-flash-lite` · temperature 0
- Số lời gọi AI: 2 (mỗi corpus 1 lượt, trace trong `codebase/logs/trace.jsonl`)
- Ghi chú lượt này: ĐỔI MODEL: gemini-2.5-flash → gemini-2.5-flash-lite (flash 503 kéo dài phía Google). Baseline mới, KHÔNG so sánh trực tiếp với run-01.

## Đối chiếu quality bar (chốt 23:59 30/07, không đổi)

| Điều kiện | Bar | Đo được | Đạt? |
|---|---|---|---|
| Đúng mức | ≥80% | **16/28 = 57.1%** | ❌ |
| Recall mức NGAY (không bỏ sót) | 100% | **80%** (4/5) | ❌ bỏ sót: G14 |
| Case bịa căn cứ | 0 | **1** | ❌ |

**Kết luận lượt này: CHƯA ĐẠT quality bar**

Chiều phụ trợ: căn cứ truy vết được 27/28 (96.4%) · đường lui đúng 26/28 (92.9%).

## Toàn bộ case (kể cả case chưa đạt)

| Case | Tin | Lớp | Loại | Mức vàng | Mức agent | Đúng mức | Căn cứ | Đường lui | Ghi chú |
|---|---|---|---|---|---|:--:|:--:|:--:|---|
| G01 | `E01` | ① | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G02 | `M19` | ① | kho | GHI_NHO | BO_QUA | ❌ | ✅ | ✅ | đoán BO_QUA, vàng GHI_NHO |
| G03 | `M21` | ① | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G04 | `M32` | ② | kho | GHI_NHO | HOM_NAY | ❌ | ✅ | ❌ | đoán HOM_NAY, vàng GHI_NHO; thiếu câu hỏi gửi TA |
| G05 | `E02` | ② | kho | GHI_NHO | HOM_NAY | ❌ | ✅ | ❌ | đoán HOM_NAY, vàng GHI_NHO; hạn chót lệch kỳ vọng; thiếu câu hỏi gửi TA |
| G06 | `M51` | ② | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G07 | `M38` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G08 | `M39` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G09 | `E05` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G10 | `M36` | ④ | kho | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G11 | `M07` | ④ | kho | BO_QUA | NGAY | ❌ | ✅ | ✅ | đoán NGAY, vàng BO_QUA; hạn chót lệch kỳ vọng |
| G12 | `E09` | ④ | kho | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G13 | `M16` | - | thuong | HOM_NAY | NGAY | ❌ | ✅ | ✅ | đoán NGAY, vàng HOM_NAY |
| G14 | `M46` | - | thuong | NGAY | HOM_NAY | ❌ | ✅ | ✅ | đoán HOM_NAY, vàng NGAY; hạn chót lệch kỳ vọng |
| G15 | `M25` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G16 | `M41` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | — |
| G17 | `M02` | - | thuong | HOM_NAY | GHI_NHO | ❌ | ❌ | ✅ | đoán GHI_NHO, vàng HOM_NAY; BỊA: trich_dan_khong_khop |
| G18 | `M22` | - | thuong | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G19 | `M06` | - | thuong | BO_QUA | GHI_NHO | ❌ | ✅ | ✅ | đoán GHI_NHO, vàng BO_QUA |
| G20 | `M45` | - | thuong | BO_QUA | GHI_NHO | ❌ | ✅ | ✅ | đoán GHI_NHO, vàng BO_QUA |
| G21 | `M33` | - | thuong | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G22 | `M18` | - | thuong | GHI_NHO | BO_QUA | ❌ | ✅ | ✅ | đoán BO_QUA, vàng GHI_NHO |
| G23 | `E07` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G24 | `E10` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G25 | `E12` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G26 | `E11` | - | hiem | BO_QUA | GHI_NHO | ❌ | ✅ | ✅ | đoán GHI_NHO, vàng BO_QUA |
| G27 | `E13` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G28 | `E04` | - | thuong | HOM_NAY | NGAY | ❌ | ✅ | ✅ | đoán NGAY, vàng HOM_NAY |

## Phân tích case chưa đạt

Tổng 12 case sai mức, phân bố theo lớp: - × 8, ② × 2, ① × 1, ④ × 1

- **G02** (`M19`, lớp ①) — Học viên đồn deadline spec được dời sang mai. Vàng `GHI_NHO`, agent trả `BO_QUA`. Nhãn vàng đặt vậy vì: nếu agent tin theo thì cả nhóm nộp muộn và mất trắng 5 điểm mốc cp4.
- **G04** (`M32`, lớp ②) — TA nhắc nộp bài lab trước cuối tuần. Vàng `GHI_NHO`, agent trả `HOM_NAY`. Nhãn vàng đặt vậy vì: nguồn chính thức nhưng không có ngày giờ cụ thể — không được tự suy ra hạn.
- **G05** (`E02`, lớp ②) — TA nhắn nộp reflection sớm nhé. Vàng `GHI_NHO`, agent trả `HOM_NAY`. Nhãn vàng đặt vậy vì: không có hạn cụ thể cũng không có kênh nộp — phải hỏi lại thay vì đoán.
- **G11** (`M07`, lớp ④) — Tin đổi phòng buổi sáng đã bị M36 đính chính lại toàn bộ. Vàng `BO_QUA`, agent trả `NGAY`. Nhãn vàng đặt vậy vì: nhắc lại tin cũ khiến học viên đi lúc 13:30 — đúng lỗi mà 7/11 người khảo sát đã dính.
- **G13** (`M16`, lớp -) — TA nhắc hạn nộp spec 23:59 hôm nay kèm link form. Vàng `HOM_NAY`, agent trả `NGAY`. Nhãn vàng đặt vậy vì: hạn cách lúc gửi hơn 12 giờ nên chưa phải mức bắn ngay.
- **G14** (`M46`, lớp -) — TA báo còn 8 tiếng nữa hết hạn nộp spec. Vàng `NGAY`, agent trả `HOM_NAY`. Nhãn vàng đặt vậy vì: cùng một hạn nhưng đã vào vùng dưới 12 giờ — mức phải tăng theo thời gian.
- **G17** (`M02`, lớp -) — TA gửi link slide Day 05 dặn tải trước khi vào lớp. Vàng `HOM_NAY`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: có việc phải làm trong ngày và có link thật trong tin.
- **G19** (`M06`, lớp -) — @everyone nhắc giữ trật tự và tắt mic. Vàng `BO_QUA`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: đúng loại spam @everyone khiến 7/11 người khảo sát phải mute.
- **G20** (`M45`, lớp -) — @here nhắc giữ vệ sinh khu vực học. Vàng `BO_QUA`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: nhắc nhở chung không kèm việc phải làm.
- **G22** (`M18`, lớp -) — TA trả lời nộp link repo mỗi bạn nộp riêng vào form. Vàng `GHI_NHO`, agent trả `BO_QUA`. Nhãn vàng đặt vậy vì: làm rõ cách nộp — cần biết nhưng bản thân nó không có hạn riêng.
- **G26** (`E11`, lớp -) — Học viên hỏi bằng tiếng Anh demo trình bày tiếng gì. Vàng `BO_QUA`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: câu hỏi cá nhân trong kênh hỏi đáp không phải thông báo.
- **G28** (`E04`, lớp -) — Ban tổ chức đổi địa điểm demo sáng mai từ hội trường A sang B. Vàng `HOM_NAY`, agent trả `NGAY`. Nhãn vàng đặt vậy vì: thay đổi chính thức cách hơn 12 giờ nhưng dưới 48 giờ.

> Chọn **một** failure đau nhất ở trên để sửa prompt, rồi chạy lại **trọn bộ** (guide §4.1).
