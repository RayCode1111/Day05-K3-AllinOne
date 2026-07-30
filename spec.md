# AI SPEC — Bản tin lọc thông báo cho học viên đã tắt notification · Nhóm [XX] · Zone [X]

Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> Mọi con số trong §1-§2 sinh lại được bằng `python codebase/evidence.py --ghi` → `eval/mining-log.md`.

---

## §1. User & Job

**Job executor:** học viên khoá AI Thực Chiến **đã tắt thông báo Discord vì bị spam**, nhưng vẫn phải nắm lịch và hạn nộp.

Không phải "học viên nói chung". Đây là một vai rất cụ thể và đo được: khảo sát cho thấy **7/11 người** đã thực sự mute server, và chính họ là nhóm chịu hậu quả nặng nhất.

**Workflow thật quanh một ngày học** *(đính kèm ảnh sơ đồ nhóm vẽ tại `validation/workflow-jtbd.jpg` — ⚠️ nhóm chụp và bỏ vào)*:

| Chặng | Đang cố làm gì | Hôm nay dùng gì | Kẹt ở đâu | Mức đau |
|---|---|---|---|---|
| Sáng trước giờ học | Biết hôm nay học ở đâu, có gì đổi không | Lướt 3-4 kênh Discord | Tin đổi phòng trôi giữa 20 tin chat | **H** |
| Trong buổi | Nắm việc phải nộp | Nghe GV nói, chưa ghi lại | Nghe rồi quên, không note | M |
| Tối | Rà xem sót gì không | Cuộn ngược lịch sử chat | Không biết cuộn tới đâu là đủ | **H** |
| Khi hỏi lại | Xác nhận hạn nộp | Hỏi bạn / lớp trưởng | Bạn cũng không chắc, tam sao thất bản | **H** |

**Core JTBD** *(không có tên sản phẩm/AI trong câu)*:

> Nắm hết việc phải làm và thay đổi lịch trong ngày mà không phải đọc lại toàn bộ tin nhắn trong lớp.

Tự kiểm: bỏ AI đi, job vẫn tồn tại — hôm nay người học đang tự làm bằng cách cuộn tay và hỏi bạn. ✅

**Job stories** *(lấy tình huống từ câu trả lời khảo sát)*:

| # | When | I want to | So I can |
|---|---|---|---|
| JS1 | Tin đổi phòng học được gửi lúc 8h15 rồi bị 20 tin chat đẩy trôi | Vẫn nhận được đúng tin đó và chỉ tin đó | Không đi nhầm phòng buổi chiều |
| JS2 | Tôi đã mute server vì @everyone quá nhiều | Chỉ bị làm phiền khi thật sự khẩn | Không phải chọn giữa "bị spam" và "bị lỡ" |
| JS3 | Một bạn nhắn "hình như deadline dời rồi" | Biết tin đó đã được TA xác nhận hay chưa | Không chủ quan rồi nộp muộn |

**Problem statement** *(KHÔNG có chữ AI)*:

> Học viên đã tắt thông báo Discord vì spam vẫn phải tự cuộn lại nhiều kênh mỗi ngày để tìm tin đổi lịch và hạn nộp. Tin quan trọng bị trôi giữa tin trò chuyện, nên **8/11 người đã từng trễ hạn hoặc bị trừ điểm**, và **7/11 đã từng đi nhầm phòng hoặc đến lớp khi buổi học đã huỷ**.

### Evidence

**Đường A — khảo sát nhóm tự chạy** (`eval/survey-responses.csv`, form ẩn danh — không thu tên, không thu email):

| Chỉ số | Kết quả |
|---|---|
| n | **11** ⚠️ *chuẩn A đòi ≥20 — còn thiếu 9, xem "Việc còn thiếu" cuối §8* |
| Bị bỏ lỡ thông tin ở mức ≥3/5 | **8/11 = 72,7%** ✅ vượt ngưỡng ≥50% |
| Trung bình mức bị bỏ lỡ | 3,18/5 |
| **Hậu quả — bị trừ điểm / trễ deadline** | **8/11 = 72,7%** |
| **Hậu quả — đi nhầm phòng / đến lớp khi đã nghỉ** | **7/11 = 63,6%** |
| Hậu quả — lo lắng thường trực sợ bỏ lỡ (FOMO) | 9/11 = 81,8% |
| Hậu quả — phải đi hỏi lại bạn bè / lớp trưởng | 6/11 = 54,5% |
| Nguyên nhân — tin quan trọng bị "trôi" | 9/11 = 81,8% |
| Nguyên nhân — quáLa Thế Quyền - 2A202601699 nhiều kênh không biết tìm đâu | 9/11 = 81,8% |
| **Nguyên nhân — phải mute vì bị spam @everyone/@here** | **7/11 = 63,6%** |
| Loại tin dễ mất nhất — đổi lịch/phòng đột xuất | 9/11 = 81,8% |
| Thời gian tìm tin mỗi ngày | 3 người <15′ · 6 người 15-30′ · 2 người 30-60′ |

**Sáu câu trả lời nguyên văn từ khảo sát** *(trích từ ô chọn nhiều đáp án, `eval/survey-responses.csv`)*:

1. `"Tin nhắn quan trọng bị "trôi" do mọi người chat/thảo luận quá nhiều."` — 9/11 người chọn
2. `"Phải tắt thông báo (Mute) vì bị spam (VD: @everyone, @here liên tục)."` — 7/11 người chọn
3. `"Bị trừ điểm / Trễ deadline nộp bài."` — 8/11 người chọn
4. `"Đi nhầm phòng học / Đến lớp khi đã được nghỉ."` — 7/11 người chọn
5. `"Đọc thông báo rồi nhưng sau đó lại quên mất do không note lại."` — 7/11 người chọn
6. `"Gây stress, lo lắng, lúc nào cũng sợ mình bỏ lỡ thông tin quan trọng (FOMO)."` — 9/11 người chọn

**Nhóm tự khai ba giới hạn của khảo sát** *(chi tiết trong `eval/mining-log.md`)*:

1. **n = 11 < 20** → **chưa đạt chuẩn A**. Nhóm ghi rõ thay vì làm tròn lên.
2. **Câu 6 là câu hỏi dẫn dắt và nhóm không dùng nó làm bằng chứng.** "Nếu có một AI Agent… bạn đánh giá mức độ hữu ích" đạt trung bình 4,45/5 — nhưng đây đúng là kiểu câu mà `02-guide.md` §1.3 cảnh báo ("hầu như ai cũng trả lời có"). Bằng chứng pain của nhóm **chỉ dựa vào Q2 (mức bị miss), Q4 (nguyên nhân) và Q5 (hậu quả đã thực sự xảy ra)**.
3. Q3/Q4/Q5 là câu chọn từ danh sách có sẵn → thiên lệch theo lựa chọn nhóm đưa ra. Vòng validation CP5 dùng câu hỏi mở để bù.

**Đường B — mining data pack VLearn:** dùng cho **ứng viên đã loại** ở §2, không dùng cho ứng viên chọn. Hướng B không có data pack; corpus Discord của prototype là **data giả tự sinh** (đề bài §3 cho phép), neo bối cảnh theo lời giảng có thật trong transcript.

---

## §2. Impact & quyết định chọn

**Ước lượng thời gian mất mỗi ngày** *(phương pháp: lấy cận dưới mỗi khoảng của Q1 — <15′ tính 7,5′, 15-30′ tính 22,5′, 30-60′ tính 45′)*: (3×7,5 + 6×22,5 + 2×45) / 11 ≈ **22,5 phút/người/ngày** chỉ để đi tìm thông báo.

| Ứng viên | Bao nhiêu người | Tần suất | Mỗi lần tốn gì | Build nổi? | Chọn? |
|---|---|---|---|---|---|
| **① Bản tin lọc thông báo Discord** | 8/11 (72,7%) bị miss ≥3/5; 7/11 đã mute | Mỗi ngày học | ~22,5 phút tìm tin + **8/11 đã trễ hạn/trừ điểm**, **7/11 đã đi nhầm phòng** — hậu quả không sửa được | Có: corpus giả + 1 lời gọi AI | ✅ **CHỌN** |
| ② Cứu lượt AI tutor VLearn bí vì không tra được tài liệu | 113/369 học viên (30,6%) | 170/1.261 lượt (13,5%) | Mất một chỗ không hiểu ngay trong buổi — nhưng **hỏi lại được sau** | Cần index 700 đoạn + đo grounding | ❌ loại |
| ③ Bản tin cuối ngày cho TA (câu hỏi tồn đọng) | Chỉ vài TA mỗi lớp | Mỗi ngày | TA trả lời lặp | Không có data Discord để đếm | ❌ loại |
| ④ Bắt lỗi tutor trả lời không kèm trích dẫn | 46,2% lượt trả lời | Rất cao | Khó kiểm chứng, phần lớn vẫn đúng nội dung | Khó định nghĩa "đạt" | ❌ loại |

**Ứng viên đã loại + vì sao:**

- **② bị loại dù bằng chứng mining mạnh hơn** (170/1.261 đếm được, so với n=11 của khảo sát). Lý do chọn ① là **mức độ hậu quả**, không phải độ lớn con số: hỏi hụt AI tutor thì học viên hỏi lại được buổi sau; còn đi nhầm phòng thi hoặc nộp muộn thì **không có đường sửa**. 8/11 và 7/11 là tỉ lệ người đã *thực sự chịu hậu quả*, không phải người *thấy bất tiện*.
- **③ bị loại vì user quá hẹp** — vài TA mỗi lớp, và nhóm không có cách đếm khối lượng câu hỏi tồn.
- **④ bị loại vì không định nghĩa được "đạt"** trong một ngày: phải phân biệt "trả lời đúng nhưng không cite" với "trả lời sai", mà chính đó lại là một bài toán đo lường riêng.

**Ứng viên CHỌN + vì sao (bằng số):** ① — **72,7%** xác nhận có pain, **72,7%** đã trả giá bằng điểm số, **63,6%** đã trả giá bằng việc đi nhầm chỗ, và **63,6%** đã buộc phải mute — tức là giải pháp hiển nhiên nhất (bật lại thông báo) *đã được thử và đã thất bại*.

---

## §3. Giải pháp tương tự đã nghiên cứu

> ⚠️ **Việc của nhóm trước CP4:** mỗi thành viên dùng thử một sản phẩm 15 phút và **thay các dòng dưới đây bằng quan sát cụ thể của mình**. Rubric R2 và vibe-coding rule kiểm ở CP5 — không dùng thử thì không giải thích được.

| Sản phẩm | Flow họ giải job này | Đáng học | Đáng né | Mình khác gì |
|---|---|---|---|---|
| Tính năng tóm tắt/recap kênh của Slack | Người dùng bấm "catch up", hệ thống tóm tắt các tin chưa đọc theo kênh | Tóm tắt gắn liền với **link nhảy về tin gốc** — người đọc kiểm được ngay | Tóm tắt theo *kênh* chứ không theo *việc phải làm*; vẫn phải tự đọc để rút ra hành động | Output của nhóm là **danh sách việc + hạn**, không phải bản tóm tắt |
| Bot digest cuối ngày trên Discord | Gom tin theo kênh, gửi vào giờ cố định | Gửi đúng một lần/ngày → không tạo thêm spam | Không phân biệt tin quan trọng với tin chat → digest vẫn dài | Nhóm **lọc bỏ** và ghi rõ đã lọc bao nhiêu tin |
| Thông báo của LMS (Google Classroom / Moodle) | Giáo viên đăng bài → hệ thống đẩy notification | Nguồn chính thức, không lẫn tin đồn | Chỉ bắt được thứ đăng đúng chỗ; thông báo nói miệng hoặc nhắn trong chat thì mất | Nhóm đọc **chính kênh chat**, nơi thông báo thật sự xảy ra |
| ChatGPT/Claude tự dán chat vào hỏi | Người dùng copy tin nhắn rồi nhờ tóm tắt | Linh hoạt | Không có ranh giới nguồn chính thức → sẵn sàng biến tin đồn thành kết luận chắc nịch | Nhóm **cứng hoá luật nguồn** bằng guard trong code, không phó mặc cho prompt |

---

## §4. Thiết kế

**Lát cắt MỘT CÂU:**

> **Học viên đã tắt thông báo Discord**, cuối một ngày học, nhận **một bản tin tối đa 5 mục** trong đó **agent đã quyết định mỗi tin thuộc mức nào trong bốn mức** — kèm hạn chót và trích dẫn nguyên văn làm căn cứ, còn thứ chưa đủ căn cứ thì xếp riêng vào mục *Chưa chắc* — thay vì phải tự cuộn lại toàn bộ tin trong ngày.

- **1 user:** học viên đã mute server
- **1 việc:** nắm hết việc phải làm trong ngày mà không đọc lại toàn bộ chat
- **1 quyết định AI:** tin này thuộc mức `NGAY` / `HOM_NAY` / `GHI_NHO` / `BO_QUA`, và có đủ căn cứ để khẳng định không
- **1 kết quả:** một bản tin ≤5 mục có căn cứ truy vết được, cộng danh sách câu hỏi soạn sẵn để gửi TA

**Non-goals — năm thứ KHÔNG build:**

1. **Không làm dashboard cho Giảng viên và Admin.** `note.txt` gốc thiết kế cả ba vai (GV · SV · Admin) kèm escalation ladder — nhóm cắt hai vai kia để lát cắt demo được trong 5 phút.
2. **Không tự động trả lời câu hỏi của học viên trong Discord.** Agent chỉ phân loại thông báo, không phải chatbot hỏi-đáp.
3. **Không kết nối Discord API thật.** Corpus là data giả tự sinh; phần đọc server là mock, ghi rõ ở mục "phần nào mock" bên dưới.
4. **Không cá nhân hoá theo từng người** (lọc theo môn học, học lại lịch riêng). Khảo sát cho thấy tính năng này ít được mong đợi nhất (3/11).
5. **Không gửi ra kênh ngoài** (Zalo/Email/SMS). Chỉ hiển thị trong app.

**Mức prototype: [x] Working** — chạy end-to-end trên corpus, không can thiệp tay giữa chừng.

| Phần | Thật hay mock |
|---|---|
| Quyết định phân mức 4 bậc | **AI thật** — Gemini, `codebase/triage.py`, trace trong `codebase/logs/trace.jsonl` |
| Bốn guard chống bịa | Thật — code tất định, `codebase/test_guards.py` (7/7 đạt) |
| Dựng bản tin + luật chống spam ≤5 mục | Thật — `codebase/digest.py` |
| Chấm golden set + xuất bảng % | Thật — `codebase/run_eval.py` |
| **Nguồn tin Discord** | **MOCK** — `codebase/fixtures/*.json`, data giả tự sinh, không nối Discord API |
| **Gửi thông báo cho người dùng** | **MOCK** — hiển thị trong app, không thật sự DM/tag ai |

**Automation: [x] conditional** — AI tự quyết với tin từ nguồn chính thức có căn cứ rõ; chuyển sang hỏi TA khi nguồn không chính thức hoặc mốc thời gian mơ hồ.

Lý do theo **cost-of-error**:
- **Sai kiểu bỏ sót** (tin khẩn bị xếp `BO_QUA`): học viên đi nhầm phòng hoặc nộp muộn — **người học chịu, mất điểm, không sửa được sau**. Đây là lỗi đắt nhất.
- **Sai kiểu báo thừa** (tin vặt bị đẩy lên `NGAY`): người học mute lần nữa — mất luôn người dùng, đúng cái vòng lặp mà **7/11** người đã đi qua.
- **Sai kiểu bịa** (biến tin đồn thành hạn chót): học viên chủ động làm sai vì tin agent — đắt nhất về niềm tin.
- Vì cả ba kiểu sai đều do **người học** gánh và **không ai chặn giữa**, nhóm không chọn `automate`. Nhưng đa số tin trong ngày là tin lành và số lượng quá lớn để bắt người đọc hết, nên cũng không chọn `augment` thuần. → `conditional`: tự làm phần chắc, đẩy phần không chắc sang người.

### §4b. Nguyên tắc đã áp dụng

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G2 — làm rõ nó làm tốt đến đâu** | Khung `st.info` cố định đầu `codebase/app.py`: *"Mình chỉ tin thông báo từ Giảng viên / TA / Ban tổ chức. Tin bạn học nói về lịch hay hạn nộp, mình xếp riêng vào mục Chưa chắc — mình không đoán hộ."* Kỳ vọng được đặt **thấp hơn** khả năng thật (PAIR — Mental Models). |
| **G10 — thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | Bốn guard trong `ap_guard()` (`codebase/triage.py`): trích dẫn không khớp → hạ mức + gỡ luôn câu "việc cần làm"; hạn chót không có căn cứ → xoá hạn; nguồn không chính thức → ép về `GHI_NHO` + bắt buộc sinh câu hỏi cho TA. Prompt cũng ép chọn đúng 1 trong 4 mức, không cho bỏ trống. |
| **G11 — giải thích vì sao** | Mỗi mục trong bản tin hiện `📌 trích dẫn nguyên văn` ngay dưới kết luận, cộng expander *"Xem tin gốc"* mở ra đúng tin + dòng `vi_sao`. Người dùng Ctrl+F kiểm được, không phải tin lời agent. |
| **G8 — gạt bỏ dễ dàng** | Nút **Bỏ qua** trên từng mục (`app.py`), đóng mục đó ngay, không chặn phần còn lại của bản tin. |
| **G9 — sửa dễ dàng** | Nút **"Không đúng ý mình"** mở ô nhập ngay tại chỗ, ghi vào `codebase/logs/feedback.jsonl`. |
| **G15 — mời feedback chi tiết** | 👍/👎 kèm ô **"Mình sai chỗ nào?"** — không phải rating trần trụi. *(Đối chiếu: trong data pack VLearn, chỉ 2,8% lượt trả lời có rating vì chỉ có nút trống.)* |
| **G17 — quyền kiểm soát tổng** | Expander *"Đã lọc bỏ N tin không cần hành động"* liệt kê **mọi** tin agent đã giấu kèm lý do — người dùng luôn kiểm được thứ bị ẩn. |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

| # | Tình huống cụ thể | Lớp | Hành vi mong muốn (nói gì · hiện gì · cho user làm gì tiếp) | Nguyên tắc | Case |
|---|---|---|---|---|---|
| 1 | Học viên nhắn *"hình như deadline spec dời sang mai"* (`M19`) | ① | Không tạo hạn chót. Xếp `GHI_NHO`, thay câu hành động bằng *"Có tin chưa xác nhận liên quan đến hạn nộp — hỏi TA trước khi tin"*, đưa xuống mục **Chưa chắc** kèm câu hỏi soạn sẵn | G10, G11 | G02 |
| 2 | Học viên nhắn *"anh khoá trên bảo buổi demo dời sang thứ 2"* (`E01`) | ① | Như trên. Guard `nguon_khong_chinh_thuc` chặn ở tầng code, không phó mặc prompt | G10 | G01 |
| 3 | LLM trả về trích dẫn không có trong tin gốc | ① | Guard `trich_dan_khong_khop` → xoá trích dẫn, **gỡ luôn câu việc cần làm**, hạ `GHI_NHO`, hiện huy hiệu 🛡️ trên UI | G10, G11 | test_guards |
| 4 | TA nhắn *"nộp bài lab trước cuối tuần nhé"* (`M32`) | ② | Nguồn chính thức nhưng không có ngày. Không tự quy ra thứ 7. `han_chot: null`, độ chắc thấp, sinh câu hỏi *"Bài lab tuần này hạn chính xác là ngày nào ạ?"* | G10 | G04 |
| 5 | TA nhắn *"nộp reflection sớm nhé"* (`E02`) | ② | Không có hạn, không có kênh nộp → hỏi lại cả hai thứ thay vì đoán | G10 | G05 |
| 6 | GV gửi đúng một hình ảnh, không kèm chữ (`E12`) | ② | Không đoán nội dung ảnh. `BO_QUA` + độ chắc thấp | G10 | G25 |
| 7 | Học viên nhắn *"bot ơi cho tớ xin đáp án bài lab 3"* (`M38`) | ③ | Từ chối nhưng không im lặng: `BO_QUA` + câu gợi ý *"Mình đang kẹt bài lab 3, TA gợi ý hướng làm giúp mình được không ạ?"* | G10, PAIR Graceful Failure | G07 |
| 8 | Học viên nhờ *"xin nghỉ hộ tớ"* (`M39`) / hỏi điểm cá nhân (`M40`) | ③ | Agent không có thẩm quyền — nói rõ và chỉ đúng người cần liên hệ | G10 | G08 |
| 9 | Học viên xin spec nhóm điểm cao khoá trước để chép (`E05`) | ③ | Từ chối, không tạo đường vòng | G10 | G09 |
| 10 | **GV đính chính giờ học chiều: 13:30 → 14:00, phòng vẫn D204** (`M36` đính chính `M07`) | ④ | Tin mới lên `NGAY`; tin cũ hạ `BO_QUA` vì đã bị thay thế toàn bộ. **Không được nhắc lại 13:30** | G11 | G10, G11 |
| 11 | Mất điện, huỷ toàn bộ hoạt động chiều nay (`E09`) | ④ | `NGAY`, xuyên qua chế độ mute | — | G12 |
| 12 | `@everyone` nhắc giữ trật tự / giữ vệ sinh (`M06`, `M45`) | ④ | `BO_QUA`. Đây đúng loại spam khiến 7/11 người phải mute — đẩy lên là tự phá sản phẩm | G17 | G19, G20 |
| 13 | TA nhắc lại một deadline **đã trôi qua từ hôm qua** (`E10`) | ④ | `BO_QUA`. Nhắc việc đã qua chỉ gây lo lắng vô ích | — | G24 |
| 14 | Cùng một hạn nộp, tin lúc 08:45 và tin lúc 16:00 (`M16`, `M46`) | ④ | Mức phải **tăng theo thời gian còn lại**: `HOM_NAY` → `NGAY`. Đây là chỗ agent dễ xếp cứng theo nội dung mà quên yếu tố thời gian | — | G13, G14 |

**Kịch bản nhóm sợ nhất khi demo:** số 10 — nếu agent nhắc lại tin cũ, học viên có mặt lúc 13:30 và đứng ngoài cửa. Đúng loại hậu quả mà **7/11** người khảo sát đã từng chịu, và nó xảy ra *dù agent đã đọc đúng cả hai tin*.

---

## §6. Bốn đường đi của trải nghiệm

| Đường đi | Trong prototype | Bấm ở đâu để xem |
|---|---|---|
| **Happy path** | Mục `🔴 BÁO NGAY` với việc cần làm, hạn chót, trích dẫn nguyên văn, link nguồn | Corpus *30/07*, mục `M36` |
| **Low-confidence (②)** | Khu **⚠️ Chưa chắc — nên hỏi TA**: agent nói thẳng là không đủ căn cứ, đưa câu hỏi soạn sẵn để copy | Corpus *30/07*, mục `M32` |
| **Failure / không căn cứ (①)** | Huy hiệu 🛡️ *"Guard đã hạ cấp kết luận này"* + lý do; trích dẫn bịa bị xoá, việc cần làm bị gỡ | Corpus *30/07*, mục `M19` |
| **Correction (user sửa)** | Nút **"Không đúng ý mình"** → ô nhập → ghi `logs/feedback.jsonl`; nút **Bỏ qua** ẩn mục ngay | Mọi mục |
| **Bị đòi ngoài phạm vi (③)** | Yêu cầu xin đáp án/xin nghỉ hộ bị xếp `BO_QUA` nhưng vẫn xuất hiện ở khu *Chưa chắc* kèm câu hỏi gửi TA — từ chối mà vẫn hữu ích | Corpus *30/07*, mục `M38`, `M39` |
| **Case đặc thù domain (④)** | Expander *"Đã lọc bỏ N tin"* cho phép kiểm lại mọi thứ agent giấu — phòng đúng rủi ro bỏ sót | Cuối bản tin |

---

## §7. Kiểm thử

**Ba chiều chất lượng** *(định nghĩa đầy đủ kiểm chứng được: `eval/rubric-cham.md`)*:

1. **Đúng mức** — pass/fail, đối chiếu nhãn vàng. Ranh giới tính bằng giờ, không bằng cảm nhận.
2. **Căn cứ truy vết được** — pass/fail: không có cờ bịa, và có hạn chót thì phải có trích dẫn nguyên văn đỡ. Người ngoài nhóm Ctrl+F trong tin gốc là kiểm được, không cần hiểu nội dung.
3. **Đường lui đúng** — pass/fail: case thuộc lớp ①②③ phải có câu hỏi gửi TA.

**Golden set: 28 case** (`eval/golden-set.csv`) — vượt mức ≥20 của rubric:

| Cơ cấu | Số case |
|---|---|
| Lớp ① Nguồn sự thật | 3 (G01-G03) |
| Lớp ② Mơ hồ / thiếu thông tin | 3 (G04-G06) |
| Lớp ③ Ngoài phạm vi / thẩm quyền | 3 (G07-G09) |
| Lớp ④ Đặc thù domain | 3 (G10-G12) |
| Case thường | 12 |
| Case hiếm (deadline đã qua · chỉ có ảnh · tiếng Anh · câu nghe như lịch nhưng không phải) | 4 |

⚠️ **Khác biệt so với rubric cần khai:** rubric gợi ý *"≥10 case lấy từ chatlog thật"*. Hướng B **không có data pack chatlog Discord** — đề bài yêu cầu nhóm tự mining Discord khoá. Golden set của nhóm vì thế xây trên **corpus giả tự sinh**, nhưng mỗi tình huống đều neo vào một nguyên nhân/hậu quả **có thật trong khảo sát** (cột `vi_sao_nhan_nhu_vay` của từng case trỏ về con số khảo sát tương ứng).

**Quality bar — chốt 23:59 30/07/2026, giữ nguyên sau đó:**

> **Đạt khi ≥80% case đúng mức, VÀ recall mức `NGAY` = 100%, VÀ 0 case bịa căn cứ.**

Hai điều kiện cứng đặt cao hơn con số % có chủ đích — lý do đầy đủ trong `eval/rubric-cham.md`: bỏ sót tin khẩn là hậu quả không sửa được (7/11 người đã dính), và bịa căn cứ là mất người dùng vĩnh viễn (họ đã mute một lần rồi).

**Kết quả các lượt chạy:**

| Lượt | Đúng mức | Recall NGAY | Case bịa | Đạt bar? | Đổi gì so với lượt trước | File |
|---|---|---|---|---|---|---|
| 01 | ⚠️ chưa chạy | | | | prompt v3 lần đầu | `eval/run-01.md` |
| 02 | | | | | | |
| 03 | | | | | | |

⚠️ **Chưa có lượt đo nào vì máy dựng repo chưa có `GOOGLE_API_KEY`.** Chạy `python codebase/run_eval.py` sau khi đặt key → bảng trên tự có số. Nhóm **phải hoàn thành ít nhất lượt 01 trước CP3** và ghi nhận trung thực kể cả khi chưa đạt bar.

---

## §8. Phân công & kế hoạch

| Phần | Người phụ trách | Ghi chú |
|---|---|---|
| Spec §1-§4 | ⚠️ [tên] | |
| Evidence + khảo sát (thu thêm ≥9 phản hồi) | ⚠️ [tên] | |
| Prompt + golden set | ⚠️ [tên] | |
| Code prototype | ⚠️ [tên] | |
| Demo + slide | ⚠️ [tên] | |

**Willing users (≥3 tên thật, khai từ CP1):** ⚠️ [tên 1] · [tên 2] · [tên 3]

**Kế hoạch vòng validation CP5** *(guide §4.2)* — ≥5 người ngoài nhóm, 10 phút/người:
1. Giao task thật: *"Hôm nay bạn nghỉ một buổi. Dùng cái này để biết bạn đã bỏ lỡ việc gì."* → **im lặng quan sát**, không thuyết minh.
2. Hỏi đúng ba câu: *"Điều gì khó hiểu hoặc khó chịu nhất?"* · *"Kết quả này bạn có tin không — vì sao?"* · *"Bạn có dùng thật không — vì sao / vì sao chưa?"*
3. Log nguyên văn vào `validation/feedback-log.md`. Người log: ⚠️ [tên].

**Multi-prototype:** chưa làm. Nếu kịp giữa CP2 và CP3, trục khác biệt sẽ là **mức chủ động**: bản A đẩy tin khẩn ngay lập tức (như hiện tại) so với bản B chỉ gom vào một bản tin duy nhất cuối ngày, không bao giờ ngắt. Đây đúng là trục mà khảo sát mâu thuẫn với chính nó (8/11 muốn báo khẩn, 7/11 đã mute vì bị làm phiền).

### Việc còn thiếu — nhóm phải tự làm, không code thay được

1. **Thu thêm ≥9 phản hồi khảo sát** để đạt chuẩn A (n hiện tại = 11).
2. **Chạy `run_eval.py` ít nhất một lượt** với API key thật, điền bảng §7.
3. **Điền tên** vào bảng phân công, willing users, và `README.md`.
4. **Vòng validation CP5** với ≥5 người thật → `validation/feedback-log.md`.
5. **Mỗi người một file `reflection/`.**
6. **Dùng thử 4 sản phẩm ở §3** và thay bằng quan sát của chính mình.
7. **Bảng test độ rõ 2 người chấm** trong `eval/rubric-cham.md`.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 30/07 — dựng spec | Bỏ hai vai Giảng viên và Admin khỏi `note.txt` gốc, chỉ giữ vai học viên | Lát cắt phải là MỘT CÂU và demo được trong 5 phút (`01-de-bai.md`); ba vai + escalation ladder không kịp |
| 30/07 — dựng spec | Chuyển hướng từ "cứu lượt AI tutor VLearn bí" sang "lọc thông báo Discord" | Khảo sát nhóm tự chạy cho thấy hậu quả nặng hơn hẳn: 8/11 đã trễ hạn, 7/11 đã đi nhầm phòng — xem §2 |
| 30/07 — prompt v3 | Siết luật 4: tin bị đính chính chỉ hạ `BO_QUA` khi **toàn bộ** việc trong nó đã được tin mới nêu lại | Case G10/G11 lộ ra rằng hạ cấp máy móc sẽ nuốt mất phần việc mà tin mới không nhắc đến |
| 30/07 — guard | Guard `nguon_khong_chinh_thuc` và `trich_dan_khong_khop` **gỡ luôn câu "việc cần làm"**, không chỉ hạ mức | Chạy thử phát hiện mức bị hạ xuống `GHI_NHO` nhưng dòng *"Yên tâm, deadline đã dời"* vẫn hiện — hạ cấp mà giữ câu sai thì vẫn lừa người đọc |
| ⚠️ CP5 | *(điền sau vòng validation — rubric R6 đòi ≥1 thay đổi từ feedback, hoặc lý do giữ nguyên có căn cứ)* | |
