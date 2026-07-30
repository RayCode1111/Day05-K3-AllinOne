# Lượt đo 01 — 2026-07-30 16:14

- Prompt: `codebase/prompts/triage.md` version **v3**
- Model: `gemini-2.5-flash` · temperature 0
- Số lời gọi AI: 2 (mỗi corpus 1 lượt, trace trong `codebase/logs/trace.jsonl`)
- Ghi chú lượt này: —

## Đối chiếu quality bar (chốt 23:59 30/07, không đổi)

| Điều kiện | Bar | Đo được | Đạt? |
|---|---|---|---|
| Đúng mức | ≥80% | **25/28 = 89.3%** | ✅ |
| Recall mức NGAY (không bỏ sót) | 100% | **100%** (5/5) | ✅ |
| Case bịa căn cứ | 0 | **0** | ✅ |

**Kết luận lượt này: ĐẠT quality bar**

Chiều phụ trợ: căn cứ truy vết được 28/28 (100.0%) · đường lui đúng 27/28 (96.4%).

## Toàn bộ case (kể cả case chưa đạt)

| Case | Tin | Lớp | Loại | Mức vàng | Mức agent | Đúng mức | Căn cứ | Đường lui | Ghi chú |
|---|---|---|---|---|---|:--:|:--:|:--:|---|
| G01 | `E01` | ① | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G02 | `M19` | ① | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G03 | `M21` | ① | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G04 | `M32` | ② | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ❌ | hạn chót lệch kỳ vọng; thiếu câu hỏi gửi TA |
| G05 | `E02` | ② | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G06 | `M51` | ② | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G07 | `M38` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G08 | `M39` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G09 | `E05` | ③ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G10 | `M36` | ④ | kho | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G11 | `M07` | ④ | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G12 | `E09` | ④ | kho | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G13 | `M16` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | — |
| G14 | `M46` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | hạn chót lệch kỳ vọng |
| G15 | `M25` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G16 | `M41` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | hạn chót lệch kỳ vọng |
| G17 | `M02` | - | thuong | HOM_NAY | NGAY | ❌ | ✅ | ✅ | đoán NGAY, vàng HOM_NAY; hạn chót lệch kỳ vọng |
| G18 | `M22` | - | thuong | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G19 | `M06` | - | thuong | BO_QUA | GHI_NHO | ❌ | ✅ | ✅ | đoán GHI_NHO, vàng BO_QUA |
| G20 | `M45` | - | thuong | BO_QUA | GHI_NHO | ❌ | ✅ | ✅ | đoán GHI_NHO, vàng BO_QUA |
| G21 | `M33` | - | thuong | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G22 | `M18` | - | thuong | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | hạn chót lệch kỳ vọng |
| G23 | `E07` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G24 | `E10` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G25 | `E12` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G26 | `E11` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G27 | `E13` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G28 | `E04` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | hạn chót lệch kỳ vọng |

## Phân tích case chưa đạt

Tổng 3 case sai mức, phân bố theo lớp: - × 3

- **G17** (`M02`, lớp -) — TA gửi link slide Day 05 dặn tải trước khi vào lớp. Vàng `HOM_NAY`, agent trả `NGAY`. Nhãn vàng đặt vậy vì: có việc phải làm trong ngày và có link thật trong tin.
- **G19** (`M06`, lớp -) — @everyone nhắc giữ trật tự và tắt mic. Vàng `BO_QUA`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: đúng loại spam @everyone khiến 7/11 người khảo sát phải mute.
- **G20** (`M45`, lớp -) — @here nhắc giữ vệ sinh khu vực học. Vàng `BO_QUA`, agent trả `GHI_NHO`. Nhãn vàng đặt vậy vì: nhắc nhở chung không kèm việc phải làm.

> Chọn **một** failure đau nhất ở trên để sửa prompt, rồi chạy lại **trọn bộ** (guide §4.1).
