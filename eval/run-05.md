# Lượt đo 05 — 2026-07-31 00:05

- Prompt: `codebase/prompts/triage.md` version **v4**
- Model: `gemini-3.6-flash` · temperature 0
- Số lời gọi AI: 2 (mỗi corpus 1 lượt, trace trong `codebase/logs/trace.jsonl`)
- Ghi chú lượt này: —

## Đối chiếu quality bar (chốt 23:59 30/07, không đổi)

| Điều kiện | Bar | Đo được | Đạt? |
|---|---|---|---|
| Đúng mức | ≥80% | **27/28 = 96.4%** | ✅ |
| Recall mức NGAY (không bỏ sót) | 100% | **100%** (5/5) | ✅ |
| Case bịa căn cứ | 0 | **0** | ✅ |

**Kết luận lượt này: ĐẠT quality bar**

Chiều phụ trợ: căn cứ truy vết được 28/28 (100.0%) · đường lui đúng 28/28 (100.0%).

## Toàn bộ case (kể cả case chưa đạt)

| Case | Tin | Lớp | Loại | Mức vàng | Mức agent | Đúng mức | Căn cứ | Đường lui | Ghi chú |
|---|---|---|---|---|---|:--:|:--:|:--:|---|
| G01 | `E01` | ① | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G02 | `M19` | ① | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G03 | `M21` | ① | kho | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G04 | `M32` | ② | kho | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
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
| G16 | `M41` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | — |
| G17 | `M02` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | — |
| G18 | `M22` | - | thuong | GHI_NHO | GHI_NHO | ✅ | ✅ | ✅ | — |
| G19 | `M06` | - | thuong | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G20 | `M45` | - | thuong | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G21 | `M33` | - | thuong | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G22 | `M18` | - | thuong | GHI_NHO | HOM_NAY | ❌ | ✅ | ✅ | đoán HOM_NAY, vàng GHI_NHO |
| G23 | `E07` | - | thuong | NGAY | NGAY | ✅ | ✅ | ✅ | — |
| G24 | `E10` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G25 | `E12` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G26 | `E11` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G27 | `E13` | - | hiem | BO_QUA | BO_QUA | ✅ | ✅ | ✅ | — |
| G28 | `E04` | - | thuong | HOM_NAY | HOM_NAY | ✅ | ✅ | ✅ | hạn chót lệch kỳ vọng |

## Phân tích case chưa đạt

Tổng 1 case sai mức, phân bố theo lớp: - × 1

- **G22** (`M18`, lớp -) — TA trả lời nộp link repo mỗi bạn nộp riêng vào form. Vàng `GHI_NHO`, agent trả `HOM_NAY`. Nhãn vàng đặt vậy vì: làm rõ cách nộp — cần biết nhưng bản thân nó không có hạn riêng.

> Chọn **một** failure đau nhất ở trên để sửa prompt, rồi chạy lại **trọn bộ** (guide §4.1).
