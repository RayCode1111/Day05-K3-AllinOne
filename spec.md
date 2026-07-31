# AI SPEC — Nova · Bản tin lọc thông báo Discord cho học viên đã tắt notification 

Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên (Discord)  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> **Toàn bộ spec này chạy trên data Discord.** Nhóm **không dùng** `data/vlearn-pack/` (chatlog AI tutor, transcript, slide) ở bất kỳ mục nào — không làm evidence, không làm corpus, không làm golden set. Lý do ở §2.
>
> Mọi con số trong §1-§2 sinh lại được bằng `python codebase/evidence.py --ghi` → ghi đè `eval/mining-log.md`.

---

## §1. User & Job

**Job executor:** học viên khoá AI Thực Chiến **đã tắt thông báo Discord vì bị spam**, nhưng vẫn phải nắm lịch và hạn nộp.

Không phải "học viên nói chung". Đây là một vai rất cụ thể và đo được: khảo sát cho thấy **7/11 người** đã thực sự mute server, và chính họ là nhóm chịu hậu quả nặng nhất.

**Workflow thật quanh một ngày học** *(ảnh sơ đồ nhóm vẽ tại `validation/workflow-jtbd.jpg` — ⚠️ nhóm chụp và bỏ vào)*:

| Chặng | Đang cố làm gì | Hôm nay dùng gì | Kẹt ở đâu | Mức đau |
|---|---|---|---|---|
| Sáng trước giờ học | Biết hôm nay học ở đâu, có gì đổi không | Lướt 2-3 kênh thông báo Discord | Tin đổi giờ trôi giữa các tin thông báo dài | **H** |
| Trong buổi | Nắm việc phải nộp | Nghe GV/BTC nói, chưa ghi lại | Nghe rồi quên, không note | M |
| Tối | Rà xem sót gì không | Cuộn ngược lịch sử kênh | Không biết cuộn tới đâu là đủ | **H** |
| Khi hỏi lại | Xác nhận hạn nộp | Hỏi bạn / lớp trưởng | Bạn cũng không chắc, tam sao thất bản | **H** |

**Core JTBD** *(không có tên sản phẩm/AI trong câu)*:

> Nắm hết việc phải làm và thay đổi lịch trong ngày mà không phải đọc lại toàn bộ thông báo trong lớp.

Tự kiểm: bỏ AI đi, job vẫn tồn tại — hôm nay người học đang tự làm bằng cách cuộn tay và hỏi bạn. ✅

**Job stories** *(tình huống lấy từ khảo sát và từ chính data pack)*:

| # | When | I want to | So I can |
|---|---|---|---|
| JS1 | BTC đăng "THÔNG BÁO BỔ SUNG — CẦN KIỂM TRA" rồi 5 phút sau đăng "THÔNG BÁO CẬP NHẬT LỊCH" với giờ khác (`thong-bao#15` vs `#16` trong pack) | Biết cuối cùng giờ nào đúng, hoặc biết rằng chưa ai chốt | Không vào Zoom sai giờ rồi mất điểm danh |
| JS2 | Tôi đã mute server vì `@Learner` bị ping liên tục | Chỉ bị làm phiền khi thật sự có việc phải làm | Không phải chọn giữa "bị spam" và "bị lỡ" |
| JS3 | Một bạn nhắn "hình như deadline dời rồi" | Biết tin đó đã được BTC/TA xác nhận hay chưa | Không chủ quan rồi nộp muộn |

**Problem statement**:

> Học viên đã tắt thông báo Discord vì spam vẫn phải tự cuộn lại nhiều kênh mỗi ngày để tìm tin đổi lịch và hạn nộp. Thông báo dài trung bình **625 ký tự** trong khi chỉ **6/28** tin thật sự chứa việc phải làm kèm mốc, nên tin quan trọng bị trôi — **8/11 người đã từng trễ hạn hoặc bị trừ điểm**, và **7/11 đã từng đi nhầm phòng hoặc đến lớp khi buổi học đã huỷ**.

### Evidence

Nhóm chạy **cả hai chuẩn** của đề bài: đường A (khảo sát) và đường B (mining data Discord thật). Hai đường độc lập nhau và chỉ về cùng một chỗ.

#### Đường A — khảo sát nhóm tự chạy

`eval/survey-responses.csv`, form ẩn danh — không thu tên, không thu email.

| Chỉ số | Kết quả |
|---|---|
| n | **11** ⚠️ *chuẩn A đòi ≥20 — còn thiếu 9, xem "Giới hạn đã khai" bên dưới* |
| Bị bỏ lỡ thông tin ở mức ≥3/5 | **8/11 = 72,7%** ✅ vượt ngưỡng ≥50% |
| Trung bình mức bị bỏ lỡ | 3,18/5 |
| **Hậu quả — bị trừ điểm / trễ deadline** | **8/11 = 72,7%** |
| **Hậu quả — đi nhầm phòng / đến lớp khi đã nghỉ** | **7/11 = 63,6%** |
| Hậu quả — lo lắng thường trực sợ bỏ lỡ (FOMO) | 9/11 = 81,8% |
| Hậu quả — phải đi hỏi lại bạn bè / lớp trưởng | 6/11 = 54,5% |
| Nguyên nhân — tin quan trọng bị "trôi" | 9/11 = 81,8% |
| Nguyên nhân — quá nhiều kênh không biết tìm đâu | 9/11 = 81,8% |
| **Nguyên nhân — phải mute vì bị spam @everyone/@here** | **7/11 = 63,6%** |
| Nguyên nhân — đọc rồi quên vì không note lại | 7/11 = 63,6% |
| Loại tin dễ mất nhất — đổi lịch/phòng đột xuất | 9/11 = 81,8% |
| Thời gian tìm tin mỗi ngày | 3 người <15′ · 6 người 15-30′ · 2 người 30-60′ |

**Sáu câu trả lời nguyên văn từ khảo sát** *(trích từ ô chọn nhiều đáp án, `eval/survey-responses.csv`)*:

1. `"Tin nhắn quan trọng bị "trôi" do mọi người chat/thảo luận quá nhiều."` — 9/11 người chọn
2. `"Phải tắt thông báo (Mute) vì bị spam (VD: @everyone, @here liên tục)."` — 7/11 người chọn
3. `"Bị trừ điểm / Trễ deadline nộp bài."` — 8/11 người chọn
4. `"Đi nhầm phòng học / Đến lớp khi đã được nghỉ."` — 7/11 người chọn
5. `"Đọc thông báo rồi nhưng sau đó lại quên mất do không note lại."` — 7/11 người chọn
6. `"Gây stress, lo lắng, lúc nào cũng sợ mình bỏ lỡ thông tin quan trọng (FOMO)."` — 9/11 người chọn

**Giới hạn đã khai — nhóm tự nói, không để người chấm phải tự phát hiện** *(chi tiết `eval/mining-log.md`)*:

1. **n = 11 < 20 → chưa đạt chuẩn A.** Ghi rõ thay vì làm tròn lên. Đây cũng là lý do nhóm phải chạy thêm đường B cho đủ bằng chứng.
2. **Câu 6 là câu hỏi dẫn dắt và nhóm không dùng nó làm bằng chứng.** "Nếu có một AI Agent… bạn đánh giá mức độ hữu ích" đạt 4,45/5 — nhưng đây đúng kiểu câu mà `02-guide.md` §1.3 cảnh báo. Bằng chứng pain **chỉ dựa vào Q2 (mức bị miss), Q4 (nguyên nhân), Q5 (hậu quả đã thực sự xảy ra)**.
3. Q3/Q4/Q5 là câu chọn từ danh sách có sẵn → thiên lệch theo lựa chọn nhóm đưa ra. Vòng validation CP5 dùng câu hỏi mở để bù.

#### Đường B — mining data pack Discord *(thông báo THẬT của khoá)*

Nguồn: `data/discord-pack/` — export 2 kênh thông báo của khoá, **28 thông báo**, trải từ 24/7 đến 3/8/2026. Đếm lại bằng `python codebase/evidence.py`; tiêu chí đếm nằm nguyên trong code (`codebase/evidence.py`, `codebase/discord_data.py`) để **tranh luận được**, không giấu trong đầu người đếm.

| Chỉ số | Giá trị |
|---|---|
| Tổng số thông báo trong pack | **28** (kênh *Thông báo* 19 · kênh *Thông báo chung* 9) |
| Tin có việc phải làm kèm mốc/hạn | 6/28 = 21,4% |
| Tin ping cả lớp (`@everyone` / `@here` / `@Learner` / `@Lab Coach`) | 13/28 = 46,4% |
| **Tin ping cả lớp nhưng KHÔNG kèm việc phải làm** | **11/13 = 85%** |
| Độ dài thông báo (trung bình · trung vị · dài nhất) | **625** · 579 · 1941 ký tự |
| Thông báo dài hơn 500 ký tự | **17/28** |

**Năm ví dụ nguyên văn từ pack** *(trích ngắn theo luật bảo mật — chỉ vài dòng, kèm mã tin để tra ngược)*:

| Mã tin | Trích nguyên văn (rút gọn) | Nó chứng minh điều gì |
|---|---|---|
| `thong-bao#15` | *"Workshop 4 được dời sang tối Chủ nhật lúc 20:00. Link Zoom sẽ gửi sau."* | Tin đổi lịch — đúng loại tin 9/11 người khai là dễ mất nhất |
| `thong-bao#16` | *"Workshop 4 vẫn diễn ra lúc 19:00 tối Chủ nhật trên Zoom cũ."* | **Mâu thuẫn trực tiếp với `#15`.** Người đọc lướt sẽ nhớ mỗi một giờ |
| `thong-bao#17` | *"Các team hoàn thành và nộp checkpoint 4 trước cuối ngày mai. Form nộp bài sẽ được thông báo sau."* | Hạn tương đối + kênh nộp chưa có → không thể tự suy ra ngày |
| `thong-bao#5` | *"@Learner"* (toàn bộ nội dung tin — 8 ký tự) | Ping cả lớp, **không** kèm bất kỳ việc gì. Đúng loại làm 7/11 người mute |
| `thong-bao-chung#9` | *"Deadline nộp sẽ là 23h59p ngày 30/7, tuy nhiên có thể tiếp tục commit tới ngày mai ngày 31/7"* | Hai mốc trong một câu — chỗ agent dễ gộp sai nhất |

**Vì sao đường B đáng giá hơn đường A ở một điểm:** khảo sát cho biết người dùng *khai* rằng họ phải mute vì spam; pack cho thấy tỉ lệ ping-không-kèm-việc *thật sự* là **85%**. Người dùng không phóng đại.

> ⚠️ **Bảo mật data:** README của khoá cấm commit data pack vào repo nộp bài. Hiện `data/` **vẫn đang được git theo dõi** — phải `git rm -r --cached data/` và thêm `data/` vào `.gitignore` trước khi nộp. Spec này chỉ giữ số đếm và trích dẫn ngắn vài dòng, đúng phần được phép.

---

## §2. Impact & quyết định chọn

**Ước lượng thời gian mất mỗi ngày** *(phương pháp: lấy cận dưới mỗi khoảng của Q1 — <15′ tính 7,5′, 15-30′ tính 22,5′, 30-60′ tính 45′)*: (3×7,5 + 6×22,5 + 2×45) / 11 ≈ **22,5 phút/người/ngày** chỉ để đi tìm thông báo.

**Bốn ứng viên — tất cả đều nằm trên hướng B (Discord), cùng một data pack, nên so sánh được với nhau:**

| Ứng viên | Bao nhiêu người | Tần suất | Mỗi lần tốn gì | Build nổi trong 1,5 ngày? | Chọn? |
|---|---|---|---|---|---|
| **① Bản tin lọc thông báo + đối chiếu bài nộp** | 8/11 (72,7%) bị miss ≥3/5 · 7/11 đã mute · **11/13 tin ping cả lớp không kèm việc (đếm trên pack thật)** | Mỗi ngày học | ~22,5 phút tìm tin + **8/11 đã trễ hạn/trừ điểm**, **7/11 đã đi nhầm phòng** — hậu quả không sửa được | Có: pack có sẵn 28 tin + 1 lời gọi AI | ✅ **CHỌN** |
| ② Bot trả lời câu hỏi logistics trong Discord (deadline, link, cách nộp) | Cả lớp hỏi được, nhưng **nguồn để trả lời quá mỏng: chỉ 6/28 tin có mốc rõ**, 2 tin còn mâu thuẫn nhau (`#15` vs `#16`) | Mỗi khi có người hỏi | Trả lời sai một hạn nộp = học viên nộp muộn thật, **và bot nói ra nên người học tin chắc hơn cả tin đồn** | Có, nhưng phải xây tầng "biết mình không biết" trước khi dám trả lời | ❌ loại |
| ③ Bản tin cuối ngày cho TA (câu hỏi tồn, chủ đề hỏi nhiều) | Vài TA mỗi lớp — user hẹp nhất trong bốn ứng viên | Mỗi ngày | TA trả lời lặp | **Không đếm được:** pack là kênh thông báo một chiều, **0 tin hỏi bài của học viên** → không có gì để gom | ❌ loại |
| ④ Phát hiện học viên stuck rồi chủ động hỗ trợ | ⚠️ **không đo được trên pack** — pack không chứa tin học viên, nên không có tín hiệu stuck nào để đếm | — | Chủ động sai chỗ = thêm một nguồn spam nữa cho đúng nhóm đã mute | Cần data hội thoại học viên mà nhóm không có | ❌ loại |

**Ứng viên đã loại + vì sao:**

- **② bị loại theo cost-of-error, không phải theo độ khó.** Bot trả lời logistics phải *phát ngôn* một con số hạn nộp. Pack cho thấy nguồn thật sự mâu thuẫn (`thong-bao#15` nói 20:00, `thong-bao#16` nói 19:00) và mơ hồ (`thong-bao#17` — "cuối ngày mai", form chưa có). Một bot trả lời trên nền đó sẽ **biến sự mơ hồ của BTC thành sự chắc chắn giả**. Ứng viên ① giải đúng phần lõi đó mà không phải phát ngôn thay BTC: nó *chuyển tiếp* nguyên văn và nói rõ chỗ nào chưa chắc.
- **③ bị loại vì user quá hẹp và không đếm được** — vài TA mỗi lớp, và pack không có câu hỏi học viên nào để đo khối lượng tồn đọng.
- **④ bị loại vì không có data.** Nhóm khai thẳng là **không có số** thay vì mượn con số của ứng viên khác gán vào.
- **Nhóm KHÔNG chọn hướng A (VLearn)** dù được cấp `data/vlearn-pack/`: pack đó là hội thoại AI tutor × học viên (`role` chỉ có `student`/`tutor`) và transcript bài giảng. Bốn ứng viên trên đều là bài toán *thông báo/lịch/hạn nộp*, không có mặt trong pack VLearn. Dùng nó chỉ để "có số cho đẹp" là gán bằng chứng sai bài toán.

**Ứng viên CHỌN + vì sao (bằng số):** ① là ứng viên **duy nhất có bằng chứng từ hai nguồn độc lập nhau** — khảo sát (n=11, người tự khai) **và** đếm trên 28 thông báo thật của khoá. Hai nguồn chỉ về cùng một chỗ: **7/11 người khai phải mute vì bị ping spam**, và **11/13 tin ping cả lớp trong pack thật sự không kèm việc phải làm**. Thêm vào đó, **72,7%** đã trả giá bằng điểm số, **63,6%** đã trả giá bằng việc đi nhầm chỗ, và **63,6%** đã buộc phải mute — tức là giải pháp hiển nhiên nhất (bật lại thông báo) *đã được thử và đã thất bại*.

---

## §3. Giải pháp tương tự đã nghiên cứu

| Sản phẩm | Flow họ giải job này | Đáng học | Đáng né | Mình khác gì |
|---|---|---|---|---|
| Tính năng tóm tắt/recap kênh của Slack | Người dùng bấm "catch up", hệ thống tóm tắt các tin chưa đọc theo kênh | Tóm tắt gắn liền với **link nhảy về tin gốc** — người đọc kiểm được ngay | Tóm tắt theo *kênh* chứ không theo *việc phải làm*; vẫn phải tự đọc để rút ra hành động | Output của Nova là **danh sách việc + hạn + trích dẫn**, không phải bản tóm tắt |
| Bot digest cuối ngày trên Discord (MEE6, Zapier digest) | Gom tin theo kênh, gửi vào giờ cố định | Gửi đúng một lần/ngày → không tạo thêm spam | Không phân biệt tin quan trọng với tin thông báo dài → digest vẫn dài bằng bản gốc | Nova **lọc bỏ** và báo rõ đã bỏ bao nhiêu tin, mở ra kiểm được |
| Thông báo của LMS (Google Classroom / Moodle) | Giáo viên đăng bài → hệ thống đẩy notification | Nguồn chính thức, không lẫn tin đồn | Chỉ bắt được thứ đăng đúng chỗ; thông báo nhắn trong chat thì mất | Nova đọc **chính kênh Discord**, nơi thông báo thật sự xảy ra |
| Dán chat vào ChatGPT/Claude nhờ tóm tắt | Người dùng copy tin nhắn rồi nhờ tóm tắt | Linh hoạt, không cần dựng gì | Không có ranh giới nguồn chính thức → sẵn sàng biến tin mơ hồ thành kết luận chắc nịch; và phải copy tay mỗi ngày | Nova **cứng hoá luật căn cứ bằng code** (`_ground()` trong `discord_agent.py`), không phó mặc cho prompt |

⚠️ *Nhóm cần bổ sung ảnh chụp màn hình khi dùng thử từng sản phẩm vào `validation/` trước CP5 — rubric R2 và vibe-coding rule hỏi tại chỗ.*

---

## §4. Thiết kế

**Lát cắt MỘT CÂU:**

> **Học viên đã tắt thông báo Discord**, bằng **một lần bấm "Kiểm tra hôm nay"**, nhận **danh sách việc phải làm trong ngày** mà **agent đã quyết định từng thông báo là "có đủ căn cứ để giao việc" hay "chưa đủ căn cứ, phải hỏi lại BTC"** — mỗi việc kèm trích dẫn nguyên văn và link mở tin gốc — thay vì phải tự cuộn lại toàn bộ hai kênh thông báo.

- **1 user:** học viên đã mute server
- **1 việc:** nắm hết việc phải làm trong ngày mà không đọc lại toàn bộ thông báo
- **1 quyết định AI:** thông báo này có đủ căn cứ để thành một việc có hạn không — nếu có thì gấp mức nào (`urgent` / `today` / `upcoming`), nếu không thì đẩy sang mục *Cần xác thực* kèm câu hỏi soạn sẵn
- **1 kết quả:** danh sách việc có căn cứ truy vết được + danh sách câu hỏi gửi LabCoach/BTC + trạng thái đã-nộp-bài-hay-chưa

**Non-goals — năm thứ KHÔNG build:**

1. **Không làm dashboard cho Giảng viên và Admin.** Thiết kế gốc có cả ba vai (GV · SV · Admin) kèm escalation ladder — nhóm cắt hai vai kia để lát cắt demo được trong 5 phút.
2. **Không trả lời câu hỏi của học viên** (đây chính là ứng viên ② đã loại ở §2). Nova phân loại và chuyển tiếp thông báo, không phải chatbot hỏi-đáp.
3. **Không kết nối Discord API thật.** Nova đọc file export của kênh; phần "thông báo mới đẩy lên" là cửa sổ mô phỏng trong app.
4. **Không cá nhân hoá theo từng người** (lọc theo môn, theo team). Khảo sát cho thấy tính năng này ít được mong đợi nhất (3/11 = 27,3%).
5. **Không gửi ra kênh ngoài** (Zalo/Email/SMS/DM Discord). Chỉ hiển thị trong app — dù 90,9% người khảo sát muốn được tag vào kênh riêng, việc gửi ra ngoài không kiểm chứng được trong phạm vi demo.

**Mức prototype: [x] Working** — chạy end-to-end trên thông báo thật, không can thiệp tay giữa chừng.

| Phần | Thật hay mock |
|---|---|
| **Nguồn tin Discord** | **THẬT** — 28 thông báo trong `data/discord-pack/`, đọc qua `codebase/discord_store.py` |
| Quyết định phân loại + mức ưu tiên | **AI thật** — Gemini, `codebase/discord_agent.py`, trace trong `codebase/logs/agent_runs.jsonl` (25 lượt quét đã ghi) |
| Guard chống bịa căn cứ | Thật — code tất định, `_ground()` trong `discord_agent.py`; nhánh đo có 4 guard trong `codebase/triage.py` + `codebase/test_guards.py` (**7/7 đạt**) |
| Chấm golden set + xuất bảng % | Thật — `codebase/run_eval.py` → `eval/run-0N.md` |
| **Đẩy thông báo mới lên kênh** | **MOCK** — cửa sổ "Discord — mô phỏng thông báo mới" trong `app.py`, ghi vào `store/discord_inbox.json`; không nối Discord API |
| **Trạng thái nộp bài Codelabs** | **MOCK** — `codebase/codelab.py` là adapter cùng chữ ký với API thật, đọc/ghi `store/codelab.json` |
| **Gửi thông báo cho người dùng** | **MOCK** — hiển thị trong app, không thật sự DM/tag ai |

**Automation: [x] conditional** — AI tự quyết với thông báo có căn cứ nguyên văn rõ ràng; chuyển sang *Cần xác thực* để người học hỏi BTC khi căn cứ không khớp, mốc thời gian mơ hồ, hoặc hai tin mâu thuẫn.

Lý do theo **cost-of-error**:

- **Sai kiểu bỏ sót** (tin đổi lịch bị bỏ qua): học viên vào Zoom sai giờ, mất điểm danh, hoặc nộp muộn — **người học chịu, không sửa được sau**. Đây là lỗi đắt nhất.
- **Sai kiểu báo thừa** (tin vặt bị đẩy lên `urgent`): người học mute lần nữa — mất luôn người dùng, đúng cái vòng lặp mà **7/11** người đã đi qua.
- **Sai kiểu bịa** (biến "cuối ngày mai" thành một ngày cụ thể): học viên chủ động làm sai vì tin agent — đắt nhất về niềm tin, và họ đã mute một lần rồi.
- Vì cả ba kiểu sai đều do **người học** gánh và **không ai chặn giữa**, nhóm không chọn `automate`. Nhưng 28 thông báo với 17 tin dài trên 500 ký tự là quá nhiều để bắt người đọc hết, nên cũng không chọn `augment` thuần. → `conditional`: tự làm phần chắc, đẩy phần không chắc sang người **kèm sẵn câu hỏi để hỏi**.

### §4b. Nguyên tắc đã áp dụng — mỗi dòng trỏ vào code thật

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G1 — làm rõ hệ thống làm được gì** | Thẻ hero đầu màn *Hôm nay* (`app.py` `hero_content()`): *"Nova gọi Codelabs xem bạn đã nộp bài chưa, đọc thông báo Discord, kiểm tra căn cứ và chỉ đưa việc đã xác thực vào danh sách."* Câu này nói đúng ba việc Nova làm và **không hứa** việc thứ tư. |
| **G2 — làm rõ nó làm tốt đến đâu** | Sau khi quét, hero hiện đúng ba con số: *"✓ Đã đọc N thông báo · ✓ M việc có căn cứ · ⚠ K mục cần xác nhận"*. Người dùng biết ngay Nova **không** dám khẳng định K mục kia. Kỳ vọng được đặt **thấp hơn** khả năng thật (PAIR — Mental Models). |
| **G10 — thu hẹp phạm vi khi nghi ngờ** *(bắt buộc)* | `_ground()` trong `codebase/discord_agent.py`: một việc chỉ được vào danh sách khi **`source_id` có thật** VÀ **`evidence` là chuỗi con nguyên văn của đúng tin đó** VÀ `confidence == "high"`. Trượt bất kỳ điều kiện nào → **không bị xoá, mà bị chuyển sang mục *Cần xác thực*** kèm câu hỏi. Ở nhánh đo, `ap_guard()` trong `triage.py` làm chặt hơn: 4 guard (id bịa · trích dẫn không khớp · hạn không căn cứ · nguồn không chính thức), có `test_guards.py` 7/7 kiểm chính guard đó. |
| **G11 — giải thích vì sao** | Mỗi dòng việc (`task_row()` trong `app.py`) hiện `Căn cứ: "…"` là đoạn trích nguyên văn, cộng nút mở `source_dialog()` — bấm vào ra **đúng tin gốc, đủ kênh + người gửi + ngày**. Người dùng Ctrl+F kiểm được, không phải tin lời agent. |
| **G9 — sửa dễ dàng** | Nova nói *"Chưa nộp — Lab ngày 30/07"*; nếu người học đã nộp rồi thì bấm **"Tôi đã nộp — kiểm tra lại"** (`codelab_card()`) để Nova gọi lại và sửa kết luận ngay tại chỗ. Đây là đường sửa cho đúng kết luận dễ sai nhất của Nova. |
| **G17 — quyền kiểm soát tổng** | Ba chốt trong sidebar và header: **Ngày tham chiếu** (đổi ngày thì đổi toàn bộ kết quả), **"Đặt lại phiên demo"** (xoá cache + trạng thái, buộc quét lại từ đầu), và cửa sổ **Discord** liệt kê **toàn bộ** thông báo Nova được đọc — cả tin từ pack lẫn tin mô phỏng. Không có tin nào Nova đọc mà người dùng không xem lại được. |
| **PAIR — Errors + Graceful Failure** | Hai loại lỗi có hai đường lui khác nhau: hết quota/model lỗi → `_generate()` tự đổi sang model kế trong `DEFAULT_MODELS` rồi mới báo; quét Discord hỏng nhưng Codelabs vẫn chạy → `st.session_state.scan_error` hiện cảnh báo *"Đã lấy được trạng thái Codelabs, nhưng chưa quét được Discord: …"* thay vì trả về màn hình trắng. |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

Cột **Nguồn** cho biết kịch bản lấy từ **pack thật** hay từ **corpus dựng thêm**. Pack thật là kênh thông báo một chiều nên không chứa tin đồn học viên hay yêu cầu ngoài thẩm quyền — nhóm dựng corpus riêng để ép agent vào đúng những lớp đó (§7).

| # | Tình huống cụ thể | Nguồn | Lớp | Hành vi mong muốn (nói gì · hiện gì · cho user làm gì tiếp) | Nguyên tắc |
|---|---|---|---|---|---|
| 1 | **Hai tin liên tiếp mâu thuẫn giờ Workshop 4: `#15` nói 20:00, `#16` nói 19:00** | **Pack thật** (`thong-bao#15`, `#16`) | ④ | Tuyệt đối không tự chọn một giờ. Cả hai vào *Cần xác thực*, hiện cả hai trích dẫn cạnh nhau, câu hỏi soạn sẵn: *"Workshop 4 cuối cùng là 19:00 hay 20:00 ạ?"* | G10, G11 |
| 2 | Hạn tương đối, kênh nộp chưa tồn tại: *"nộp checkpoint 4 trước cuối ngày mai. Form nộp bài sẽ được thông báo sau"* | **Pack thật** (`thong-bao#17`) | ② | Không quy "ngày mai" ra ngày cụ thể. `deadline` để nguyên văn, đưa vào *Cần xác thực*, hỏi cả hai thứ: hạn chính xác và link form | G10 |
| 3 | *"hạn tới chủ nhật"* — không có ngày | **Pack thật** (`thong-bao-chung#2`) | ② | Không tự suy ra 3/8. Giữ nguyên chữ "chủ nhật", độ chắc thấp | G10 |
| 4 | Một tin chỉ có đúng chữ `@Learner`, không nội dung | **Pack thật** (`thong-bao#5`) | ② | Không đoán tin này nói gì. Bỏ khỏi danh sách việc, đếm vào số tin đã lọc | G10 |
| 5 | Block trong pack bị hỏng format, không đọc được ngày đăng | **Pack thật** (`thong-bao-chung#3`) | ② | `date` rỗng → không được lấy ngày của tin liền trước gán vào. Không xếp mức theo thời gian | G10 |
| 6 | Changelog Codelabs v0.0.5 dài 857 ký tự, không có việc nào cho học viên | **Pack thật** (`thong-bao-chung#4`) | ④ | Bỏ qua. Đẩy tin này lên là tự tái tạo đúng loại spam khiến 7/11 người mute | G17 |
| 7 | Một câu chứa **hai mốc**: *"Deadline nộp sẽ là 23h59p ngày 30/7, tuy nhiên có thể tiếp tục commit tới ngày mai ngày 31/7"* | **Pack thật** (`thong-bao-chung#9`) | ④ | Không gộp thành một hạn. Lấy mốc **sớm hơn** làm hạn hành động và giữ nguyên văn cả câu làm căn cứ để người học tự đọc phần nới lỏng | G11 |
| 8 | Thông báo cho ngày **3/8**, trong khi ngày tham chiếu là 30/7 | **Pack thật** (`thong-bao#12`, `#13`) | ④ | Không đẩy lên `urgent`. Xếp `upcoming`, không làm loãng phần việc hôm nay | — |
| 9 | LLM trả về `evidence` không có trong tin gốc | Guard | ① | `_ground()` chặn ở tầng code: việc đó **không được vào danh sách**, bị chuyển sang *Cần xác thực* kèm câu *"Bạn có thể kiểm tra lại với TA/BTC không?"* | G10, G11 |
| 10 | LLM trả về `source_id` không tồn tại (bịa hẳn một tin) | Guard | ① | Bị loại, vì `source_id in sources` là điều kiện cứng. Nhánh đo có test riêng: `test_ga_id_bia_bi_bo` | G10 |
| 11 | Học viên nhắn *"hình như deadline spec dời sang mai"* | Corpus (`M19`) | ① | Không tạo hạn chót. Hạ `GHI_NHO`, thay câu hành động bằng *"Có tin chưa xác nhận liên quan đến hạn nộp — hỏi TA trước khi tin"*, đưa xuống mục *Chưa chắc* kèm câu hỏi soạn sẵn | G10, G11 |
| 12 | Học viên nhắn *"anh khoá trên bảo buổi demo dời sang thứ 2"* | Corpus (`E01`) | ① | Như trên. Guard `nguon_khong_chinh_thuc` chặn ở tầng code, không phó mặc prompt | G10 |
| 13 | Học viên nhắn *"bot ơi cho tớ xin đáp án bài lab 3"* | Corpus (`M38`) | ③ | Từ chối nhưng không im lặng: bỏ khỏi bản tin + câu gợi ý *"Mình đang kẹt bài lab 3, TA gợi ý hướng làm giúp mình được không ạ?"* | G10, PAIR Graceful Failure |
| 14 | Học viên nhờ *"xin nghỉ hộ tớ"* / hỏi điểm cá nhân | Corpus (`M39`, `M40`) | ③ | Agent không có thẩm quyền — nói rõ và chỉ đúng người cần liên hệ | G10 |
| 15 | Học viên xin spec nhóm điểm cao khoá trước để chép | Corpus (`E05`) | ③ | Từ chối, không tạo đường vòng | G10 |
| 16 | GV đính chính giờ học chiều 13:30 → 14:00, phòng vẫn D204 | Corpus (`M36` đính chính `M07`) | ④ | Tin mới lên `NGAY`; tin cũ hạ `BO_QUA` vì đã bị thay thế toàn bộ. **Không được nhắc lại 13:30** | G11 |
| 17 | TA nhắc lại một deadline **đã trôi qua từ hôm qua** | Corpus (`E10`) | ④ | `BO_QUA`. Nhắc việc đã qua chỉ gây lo lắng vô ích | — |
| 18 | Cùng một hạn nộp, tin lúc 08:45 và tin lúc 16:00 | Corpus (`M16`, `M46`) | ④ | Mức phải **tăng theo thời gian còn lại**: `HOM_NAY` → `NGAY`. Chỗ agent dễ xếp cứng theo nội dung mà quên yếu tố thời gian | — |

**Kịch bản nhóm sợ nhất khi demo:** số 1 — cặp `thong-bao#15` / `#16` là **mâu thuẫn có thật trong data thật**, không phải tình huống nhóm nghĩ ra. Nếu Nova chọn đại một giờ và nói chắc nịch, học viên vào Zoom sai giờ và mất điểm danh — đúng loại hậu quả mà **7/11** người khảo sát đã từng chịu, và nó xảy ra *dù agent đã đọc đúng cả hai tin*.

---

## §6. Bốn đường đi của trải nghiệm

| Đường đi | Trong prototype | Bấm ở đâu để xem |
|---|---|---|
| **Happy path** | Màn *Hôm nay*: danh sách việc có badge *Cần làm ngay / Hôm nay / Sắp tới*, mỗi việc kèm `Căn cứ: "…"` nguyên văn và nút mở tin gốc | Bấm **"Kiểm tra hôm nay"** với ngày tham chiếu 30/07/2026 |
| **Low-confidence (②)** | Tab **Cần xác thực**: Nova nói thẳng là chưa đủ dữ kiện, hiện trích dẫn + **câu hỏi soạn sẵn để copy gửi LabCoach/BTC** | Tab *Cần xác thực* — ví dụ rõ nhất là `thong-bao#17` (hạn "cuối ngày mai") |
| **Failure / không căn cứ (①)** | Việc mà LLM đề xuất nhưng `evidence` không khớp nguyên văn **không xuất hiện ở danh sách việc**, mà rơi xuống *Cần xác thực* với câu *"Bạn có thể kiểm tra lại với TA/BTC không?"* | Tab *Cần xác thực*; cơ chế ở `_ground()` |
| **Correction (user sửa)** | Nút **"Tôi đã nộp — kiểm tra lại"** sửa kết luận sai của Nova về bài nộp; checkbox tick/bỏ tick chuyển việc qua lại giữa *Việc cần làm* và *Đã hoàn thành* | Thẻ *Bài nộp Codelabs* và mọi dòng việc |
| **Bị đòi ngoài phạm vi (③)** | Yêu cầu xin đáp án / xin nghỉ hộ bị loại khỏi danh sách việc nhưng vẫn hiện ở khu *Chưa chắc* kèm câu hỏi gửi TA — từ chối mà vẫn hữu ích | Nhánh đo, corpus *30/07*, tin `M38`, `M39` |
| **Case đặc thù domain (④)** | Cửa sổ **Discord** liệt kê đủ 28 thông báo pack + tin mô phỏng, để người dùng đối chiếu thứ Nova đã bỏ qua; ở nhánh CLI là dòng *"Đã lọc bỏ N tin không cần hành động"* (`digest.py`) | Nút **💬 Discord** ở header |

---

## §7. Kiểm thử

### Hai bề mặt đo — khai rõ để không bị hiểu nhầm

Prototype có **hai nhánh chạy**, dùng chung một triết lý guard nhưng **không dùng chung prompt**:

| Nhánh | Chạy trên gì | Dùng để làm gì | File |
|---|---|---|---|
| **Nhánh demo** | **28 thông báo thật** trong `data/discord-pack` + tin mô phỏng | Bản chạy đưa cho người dùng thử | `app.py` · `discord_agent.py` · `discord_store.py` |
| **Nhánh đo** | Corpus dựng thêm, có đủ metadata từng tin | Chấm % trên golden set qua 6 lượt | `triage.py` · `digest.py` · `run_eval.py` · `prompts/triage.md` |

⚠️ **Giới hạn phải nói thẳng: con số % ở dưới đo trên nhánh đo, không đo trên nhánh demo.** Nhánh demo đã chạy thật **25 lượt quét** trên pack (log `codebase/logs/agent_runs.jsonl`, 28-31 nguồn mỗi lượt, model `gemini-3.6-flash` / `gemini-3.5-flash`) nhưng **chưa có nhãn vàng cho pack thật** nên chưa quy ra %. Đây là việc còn thiếu lớn nhất của phần kiểm thử, ghi ở cuối §8.

**Vì sao golden set không xây thẳng trên pack thật** *(rubric gợi ý "≥10 case lấy từ chatlog thật" — nhóm khai đủ ba lý do)*:

1. **Pack không có metadata từng tin.** Pack chỉ có `date` ở mức **ngày** (`30/7/2026`), không có giờ, không có tác giả thật, không có vai. Mà toàn bộ định nghĩa "đúng mức" của nhóm (`eval/rubric-cham.md`) tính bằng **khoảng cách giờ** giữa `ts` của tin và mốc phải làm — 12h/48h. Thiếu giờ thì **đúng phần lõi không đo được**, và một golden set chấm bằng cảm nhận thì người ngoài nhóm chấm lại sẽ ra kết quả khác.
2. **Pack không phủ được 4 lớp chỗ khó.** Pack là kênh thông báo **một chiều từ BTC**: không có tin đồn học viên (lớp ①), không có yêu cầu ngoài thẩm quyền (lớp ③). Corpus được dựng riêng để ép agent vào đúng bốn lớp đó.
3. **Thứ tự thời gian.** Golden set và 4 lượt eval đầu chốt chiều 30/07 (lượt 01 lúc 16:14); pack được đưa vào repo tối 30/07, sau khi quality bar đã chốt và không được đổi nữa.

Bù lại — và đây là điểm nhóm chủ động làm sau khi có pack — **8/18 kịch bản rủi ro ở §5 lấy thẳng từ pack thật**, gồm cả kịch bản nhóm sợ nhất (cặp mâu thuẫn `#15`/`#16`). Pack không dùng để chấm điểm, nhưng đã dùng để **kiểm tra xem nhóm có tưởng tượng sai về rủi ro không**. Kết quả: pack thật hiểm hơn nhóm dự đoán ở chỗ mâu thuẫn giữa hai thông báo chính thức, chứ không phải ở tin đồn học viên.

### Ba chiều chất lượng

*(định nghĩa đầy đủ kiểm chứng được: `eval/rubric-cham.md`)*

1. **Đúng mức** — pass/fail, đối chiếu nhãn vàng. Ranh giới tính bằng giờ, không bằng cảm nhận.
2. **Căn cứ truy vết được** — pass/fail: không có cờ bịa, và có hạn chót thì phải có trích dẫn nguyên văn đỡ. Người ngoài nhóm Ctrl+F trong tin gốc là kiểm được, không cần hiểu nội dung.
3. **Đường lui đúng** — pass/fail: case thuộc lớp ①②③ phải có câu hỏi gửi TA.

### Golden set: 28 case (`eval/golden-set.csv`) — vượt mức ≥20 của rubric

| Cơ cấu | Số case |
|---|---|
| Lớp ① Nguồn sự thật | 3 (G01-G03) |
| Lớp ② Mơ hồ / thiếu thông tin | 3 (G04-G06) |
| Lớp ③ Ngoài phạm vi / thẩm quyền | 3 (G07-G09) |
| Lớp ④ Đặc thù domain | 3 (G10-G12) |
| Case thường | 12 |
| Case hiếm (deadline đã qua · chỉ có ảnh · tiếng Anh · câu nghe như lịch nhưng không phải) | 4 |

### Quality bar — chốt 23:59 30/07/2026, giữ nguyên sau đó

> **Đạt khi ≥80% case đúng mức, VÀ recall mức `NGAY` = 100%, VÀ 0 case bịa căn cứ.**

Hai điều kiện cứng đặt cao hơn con số % có chủ đích — lý do đầy đủ trong `eval/rubric-cham.md`: bỏ sót tin khẩn là hậu quả không sửa được (7/11 người đã dính), và bịa căn cứ là mất người dùng vĩnh viễn (họ đã mute một lần rồi).

### Kết quả các lượt chạy

| Lượt | Đúng mức | Recall NGAY | Case bịa | Đạt bar? | Đổi gì so với lượt trước | File |
|---|---|---|---|---|---|---|
| 01 | 25/28 = 89,3% | 100% (5/5) | 0 | ✅ ĐẠT | prompt v3 lần đầu · `gemini-2.5-flash` | `eval/run-01.md` |
| 02 | 16/28 = 57,1% | 80% (4/5) — bỏ sót G14 | 1 | ❌ | đổi model sang `gemini-2.5-flash-lite` (flash bị 503 kéo dài phía Google) → **baseline mới, không so trực tiếp với lượt 01** | `eval/run-02.md` |
| 03 | 26/28 = 92,9% | 100% (5/5) | 0 | ✅ ĐẠT | đổi model sang `gemini-3.6-flash` (đời 3, mạnh nhất mà free tier gọi được) → **baseline mới** | `eval/run-03.md` |
| 04 | 26/28 = 92,9% | 100% (5/5) | 0 | ✅ ĐẠT | không đổi gì — chạy lại để xác nhận lượt 03 không phải may rủi một lần | `eval/run-04.md` |
| 05 | **27/28 = 96,4%** | 100% (5/5) | 0 | ✅ ĐẠT | **prompt v3 → v4**: thêm luật 8 sau khi phân tích case G17 (xem §9) | `eval/run-05.md` |
| 06 | **27/28 = 96,4%** | 100% (5/5) | 0 | ✅ ĐẠT | không đổi gì — chạy lại xác nhận lượt 05 lặp lại được; sai đúng một case và **vẫn là G22** | `eval/run-06.md` |

**Lượt 06 là kết quả hiện hành.** Chiều phụ trợ: căn cứ truy vết được 28/28 (100%), đường lui đúng 28/28 (100%).

**Vòng lặp đo → sửa → đo lại đã khép kín một lần, và có tác dụng đo được.** Case G17 (`M02`) sai ở cả lượt 01 lẫn lượt 04, nhưng sai theo **hai hướng ngược nhau** (lượt 01 đoán `NGAY`, lượt 04 đoán `GHI_NHO`) — dấu hiệu định nghĩa mơ hồ chứ không phải model yếu. Truy ra tin khớp đồng thời hai dòng trong bảng mức mà prompt không nói dòng nào thắng → thêm luật 8 ở prompt v4 → lượt 05 và 06 G17 đều trả đúng `HOM_NAY`, tổng tăng 26/28 lên 27/28. Không có case nào bị hỏng ngược lại, và hai điều kiện cứng giữ nguyên.

Vì prompt đã đổi (v3 → v4), lượt 05/06 là **baseline mới**, không so trực tiếp với lượt 03/04 được — cùng quy ước đã áp dụng khi đổi model ở lượt 02 và 03.

Case duy nhất còn sai ở cả hai lượt cuối là **G22** (`M18`): TA trả lời cách nộp link repo, vàng `GHI_NHO`, agent trả `BO_QUA`. Đây là loại nhầm mà `eval/rubric-cham.md` đã khai trước là chấp nhận được về mức độ nguy hiểm (không bỏ sót việc có hạn), nhưng **nó lặp lại y hệt ở hai lượt** → là lỗi định nghĩa ổn định, không phải nhiễu. Nhóm chưa sửa vì luật mới có nguy cơ kéo cả nhóm tin "hướng dẫn thao tác" lên bản tin và làm bản tin dài ra — đúng thứ sản phẩm này sinh ra để chống.

Lượt 02 được giữ lại trong bảng dù kết quả xấu: nó là bằng chứng cho thấy bar này thật sự phân biệt được model, không phải bar dễ ai chạy cũng qua.

Chạy lại: `python codebase/run_eval.py` (cần `GOOGLE_API_KEY`) → sinh `eval/run-0N.md` mới, sau đó cập nhật bảng trên theo lượt mới nhất.

---

## §8. Phân công & kế hoạch

Nhóm 5 người: **Nguyễn Trọng Nam · La Thế Quyền · Lê Việt Hoàng · Nguyễn Đức Đạt · Lê Quốc An**.

| Phần | Người phụ trách | Sản phẩm cụ thể trong repo |
|---|---|---|
| Thiết kế workflow agent & prompt AI | **Nguyễn Trọng Nam** | Vòng OBSERVE → EVALUATE → DECIDE → ACT; `codebase/prompts/triage.md` (v4, 8 luật) và prompt trong `discord_agent.py::_prompt()` |
| Backend, database & tích hợp API | **La Thế Quyền** | `discord_agent.py` (gọi Gemini, chuỗi model dự phòng, cache theo fingerprint), `discord_store.py` (đọc pack + kho tin mô phỏng), `codelab.py` (adapter API nộp bài) |
| Logic giám sát & đánh giá (Evaluate) | **Lê Việt Hoàng** | `eval/golden-set.csv` (28 case), `eval/rubric-cham.md` (3 chiều + quality bar), `codebase/run_eval.py`, 6 lượt đo `eval/run-0N.md` |
| Thiết kế giao diện dashboard & trải nghiệm (UX) | **Nguyễn Đức Đạt** | `codebase/app.py` toàn bộ: hai màn *Hôm nay* / *Cần xác thực*, thẻ việc kèm căn cứ, dialog tin gốc, cửa sổ Discord mô phỏng, thẻ Codelabs; các nguyên tắc G1/G2/G9/G11/G17 ở §4b nằm trong file này |
| Kiểm thử & vận hành triển khai trải nghiệm | **Lê Quốc An** | `codebase/test_guards.py` (7/7 đạt), chạy thật trên pack → `codebase/logs/agent_runs.jsonl` (25 lượt), dựng môi trường chạy + `.env.example` |

> **Vibe-coding rule:** TA hỏi ngẫu nhiên đúng theo bảng này tại CP5/CP6. Ai không giải thích được phần mang tên mình thì mất điểm phần đó — bảng đã sửa cho khớp việc thật.

**Kế hoạch vòng validation CP5** *(guide §4.2)* — ≥5 người ngoài nhóm, 10 phút/người:

1. Giao task thật: *"Hôm nay bạn nghỉ một buổi. Dùng cái này để biết bạn đã bỏ lỡ việc gì."* → **im lặng quan sát**, không thuyết minh.
2. Hỏi đúng ba câu: *"Điều gì khó hiểu hoặc khó chịu nhất?"* · *"Kết quả này bạn có tin không — vì sao?"* · *"Bạn có dùng thật không — vì sao / vì sao chưa?"*
3. Log nguyên văn vào `validation/feedback-log.md`.

### Việc còn thiếu — khai thẳng, không ỉm

| # | Việc | Ảnh hưởng điểm |
|---|---|---|
| 1 | `validation/feedback-log.md` **đang trống** — chưa có mẩu feedback nào từ người ngoài nhóm | **R6 = 8 điểm** |
| 2 | Chưa khai **≥3 willing users** là người ngoài nhóm | R6, tiêu chí nghiệm thu #5 |
| 3 | Khảo sát **n = 11 < 20** → chưa đạt chuẩn A (đường B đã bù một phần) | R1 |
| 4 | Chưa có nhãn vàng cho pack thật → **chưa đo được % của nhánh demo** | R4 |
| 5 | `data/` đang bị git theo dõi — phải gỡ khỏi repo nộp bài | Luật bảo mật data |
| 6 | Bảng "test độ rõ 2 người chấm" trong `eval/rubric-cham.md` chưa điền | R4 |
| 7 | Ảnh sơ đồ JTBD (`validation/workflow-jtbd.jpg`) và ảnh dùng thử 4 sản phẩm ở §3 chưa có | R1, R2 |

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 30/07 — dựng spec | Bỏ hai vai Giảng viên và Admin khỏi thiết kế gốc, chỉ giữ vai học viên | Lát cắt phải là MỘT CÂU và demo được trong 5 phút (`01-de-bai.md`); ba vai + escalation ladder không kịp |
| 30/07 — dựng spec | Chốt hướng B (Discord), **loại hẳn hướng A (VLearn)** | Bốn ứng viên nhóm cân nhắc đều là bài toán thông báo/lịch/hạn nộp — không có mặt trong pack VLearn (chatlog AI tutor). Xem §2 |
| 30/07 — prompt v3 | Siết luật 4: tin bị đính chính chỉ hạ `BO_QUA` khi **toàn bộ** việc trong nó đã được tin mới nêu lại | Case G10/G11 lộ ra rằng hạ cấp máy móc sẽ nuốt mất phần việc mà tin mới không nhắc đến |
| 30/07 — guard | Guard `nguon_khong_chinh_thuc` và `trich_dan_khong_khop` **gỡ luôn câu "việc cần làm"**, không chỉ hạ mức | Chạy thử phát hiện mức bị hạ xuống `GHI_NHO` nhưng dòng *"Yên tâm, deadline đã dời"* vẫn hiện — hạ cấp mà giữ câu sai thì vẫn lừa người đọc |
| 30/07 tối — có data pack | Chuyển nhánh demo từ corpus tự sinh sang **đọc thẳng 28 thông báo thật** trong `data/discord-pack` | Pack là thông báo thật của chính khoá này; đọc data thật là cách duy nhất biết sản phẩm có chịu nổi độ bẩn thật không (block hỏng format, tin chỉ có `@Learner`, hai tin mâu thuẫn nhau) |
| 31/07 — prompt v4 | Thêm luật 8: tin vừa có tài liệu/link mới vừa kèm việc phải làm trong ngày thì xếp theo **mốc thời gian của việc**, không xếp `GHI_NHO` | Case G17 (`M02`) fail ở cả lượt 01 và lượt 04 theo hai hướng ngược nhau: tin khớp cùng lúc dòng `HOM_NAY` và dòng `GHI_NHO` mà prompt chưa nói dòng nào thắng — lỗi định nghĩa của spec, không phải lỗi model. Lượt 05 và 06 xác nhận đã sửa được |
| 31/07 — §5 kịch bản | Thay 8 kịch bản rủi ro bằng **tình huống lấy thẳng từ pack thật**, gồm cả kịch bản nhóm sợ nhất | Đọc pack xong mới thấy rủi ro thật nằm ở **hai thông báo chính thức mâu thuẫn nhau** (`thong-bao#15` vs `#16`), chứ không phải ở tin đồn học viên như nhóm đoán ban đầu |
| 31/07 — §8 | Sửa bảng phân công cho khớp việc thật của 5 thành viên | Vibe-coding rule hỏi theo đúng bảng này; bảng nháp cũ ghi sai phần của gần như tất cả mọi người |
| **CP5 — GIỮ NGUYÊN** | **Không gộp mục *Cần xác thực* vào cuối danh sách việc**, giữ nguyên hai màn tách rời | Người thử phản ánh phải bấm sang tab khác mới thấy phần chưa chắc, dễ bỏ sót *(mẩu #\_\_ trong `validation/feedback-log.md`)*. Nhóm **giữ nguyên**: gộp lại sẽ xoá đúng ranh giới mà cả sản phẩm dựa vào — cái gì Nova có trích dẫn nguyên văn đỡ (`action_items`, đã qua `_ground()`) và cái gì chưa đủ căn cứ (`needs_confirmation`). Người dùng này đã mute một kênh vì nó trộn lẫn tin quan trọng với tin thường; trộn lại lần nữa, lần này giữa *chắc* và *không chắc*, là lặp lại đúng lỗi đó ở mức nguy hiểm hơn. Bù cho phản ánh: số mục cần xác nhận đã hiện sẵn trên thẻ hero ở màn *Hôm nay* (`hero_content()`), nên người dùng biết có bao nhiêu thứ đang chờ mà không phải sang tab |
| **CP5 — GIỮ NGUYÊN** | **Không để Nova tự chốt một giờ cho cặp thông báo mâu thuẫn** `thong-bao#15` / `#16` (Workshop 4: 20:00 vs 19:00) | Người thử muốn Nova "chốt luôn cho nhanh", vì đứng trước hai lựa chọn mà không có kết luận thì thấy khó chịu *(mẩu #\_\_)*. Nhóm **giữ nguyên**: **không có đáp án đúng trong data** — cả hai đều là thông báo chính thức, và tin sau không tự nhận là đính chính tin trước. Chốt bừa một giờ là biến sự mơ hồ của BTC thành sự chắc chắn giả, đúng lý do §2 đã loại ứng viên ② (bot trả lời logistics). Cost-of-error không đối xứng: đoán đúng thì người học tiết kiệm một câu hỏi; đoán sai thì họ vào Zoom sai giờ và mất điểm danh — không sửa được. Nova đặt hai trích dẫn cạnh nhau kèm câu hỏi soạn sẵn để người học đi hỏi trong 30 giây |
| **CP5 — GIỮ NGUYÊN** | **Không thêm luật prompt để sửa case G22** (tin hướng dẫn thao tác bị xếp `BO_QUA` thay vì `GHI_NHO`) | G22 sai lặp lại ở cả lượt 05 và 06 (`eval/run-05.md`, `eval/run-06.md`) nên là lỗi định nghĩa ổn định, không phải nhiễu — nhưng luật mới sẽ kéo **cả nhóm** tin hướng dẫn thao tác lên bản tin và làm bản tin dài ra, đúng thứ sản phẩm sinh ra để chống. Quality bar đã chốt cũng khai trước rằng loại nhầm này chấp nhận được (`eval/rubric-cham.md`): không bỏ sót việc có hạn, không bịa căn cứ. Đường lui cho người dùng đã có sẵn: cửa sổ **💬 Discord** liệt kê toàn bộ thông báo Nova đọc, kể cả tin bị lọc |
