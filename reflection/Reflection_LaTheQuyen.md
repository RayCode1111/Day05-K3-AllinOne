# Reflection 

**Họ và tên:** [La Thế Quyền]  
**Mã học viên:** [2A202601699]  
**Nhóm:** AllInOne  
**Sản phẩm:** Nova - Agentic tổng hợp và nhắc thông báo Discord cho học viên
**Vai trò:** Xây dựng backend, database & tích hợp API

---

## Vai trò của mình trong nhóm

Mình phụ trách **tầng chạy phía dưới giao diện**: đọc dữ liệu, gọi Gemini, chặn output không có căn cứ, và giả lập API Codelabs. Cụ thể là ba file `codebase/discord_store.py`, `codebase/discord_agent.py` và `codebase/codelab.py`.

Nói cho đúng phạm vi: chữ trong prompt là của anh Nam, golden set và rubric chấm là của anh Hoàng, màn hình là của Đạt, môi trường chạy và test guard là của An. Việc của mình là câu hỏi nằm giữa: **làm sao để một lượt bấm "Kiểm tra hôm nay" đi từ file `.txt` đến một cấu trúc JSON mà UI dám hiển thị — và khi nó hỏng thì hỏng có tên gọi, không hỏng thành màn hình trắng.**

Nguyên tắc mình tự đặt cho phần của mình: **mọi thứ đi lên UI phải truy ngược được về đúng một dòng chữ có thật trong `data/discord-pack`.** Nếu không truy được thì nó không phải việc cần làm, nó là câu hỏi phải đi hỏi TA.

## Phần mình trực tiếp làm

### 1. Tầng dữ liệu — `discord_store.py`

Nova đọc hai nguồn: data pack tĩnh (`data/discord-pack/*.txt`, hai kênh) và các thông báo được đẩy lên lúc chạy qua cửa sổ Discord mô phỏng (`store/discord_inbox.json`). Cả hai đi qua module này và **ra cùng một hình dạng**, nên tầng trên không cần biết một tin đến từ file hay từ demo.

- `pack_messages()` tách block bằng `BLOCK_SPLIT` — trong pack, hai thông báo khác nhau luôn cách nhau ≥2 dòng trống còn xuống đoạn trong cùng một tin chỉ cách 1 dòng. Chọn sai ranh giới này là hai thông báo bị dính làm một và trích dẫn sẽ chỉ về sai tin.
- `id` đặt theo `{channel_id}#{index}` (`thong-bao#15`), không theo tên file có dấu cách. **Đây là chỗ quan trọng nhất của cả module**: `source_id` là khoá mà guard dùng để đối chiếu và là thứ Đạt dùng để mở lại tin gốc. ID không ổn định thì guard vô hiệu và nút "xem nguồn" chỉ sai tin.
- Pack là **read-only** — `add_message()` / `delete_message()` chỉ động vào kho mô phỏng. Dữ liệu gốc của khoá không bao giờ bị code của nhóm ghi đè.
- File kho hỏng JSON thì `_read_store()` trả về danh sách rỗng chứ không ném lỗi: mất tin demo còn hơn sập app giữa lúc trình bày.

### 2. Gọi Gemini và sống sót qua hạn mức — `discord_agent.py::_generate()`

Hạn mức free-tier của Gemini tính **theo từng model mỗi ngày** (`GenerateRequestsPerDayPerProjectPerModel`), nên khi model chính hết quota thì chờ không giải quyết được gì. Mình dựng một chuỗi model dự phòng (`DEFAULT_MODELS`, ghi đè được bằng `GEMINI_MODELS` trong `.env`) và xử lý lỗi theo **loại** chứ không theo mã:

- `_quota_kind()` đọc `QuotaFailure.quotaId` trong body lỗi 429 để biết đang bị chặn **theo phút** hay **theo ngày**, và đọc `RetryInfo.retryDelay` để biết API bảo chờ bao lâu.
- Chặn theo phút và delay ≤ 30s → `time.sleep(delay)` rồi thử lại đúng model đó. Hết quota theo ngày → đổi model ngay, vì chờ bao lâu cũng vô ích.
- Mất mạng, JSON hỏng, phản hồi rỗng đều xử lý như nhau: model này không xong thì sang model kế. Chỉ khi cả chuỗi thất bại mới ném lỗi — và thông báo lỗi nói thẳng ba đường lui: thêm model vào `GEMINI_MODELS`, đổi API key, hoặc chờ quota reset.

### 3. Đọc được JSON từ một model biết "suy nghĩ" — `_answer_text()` / `_json_block()` / `_extract_json()`

Ba lớp bóc, mỗi lớp sinh ra từ một lần hỏng thật:

- `_answer_text()` bỏ các part có `thought=true`. Model dòng thinking trả thêm phần văn xuôi suy nghĩ; ghép cả vào rồi parse thì JSON hợp lệ cũng hoá thành rác.
- `_json_block()` cắt khối JSON ngoài cùng, bỏ rào ```json và mọi lời dẫn quanh nó.
- `_extract_json()` phân biệt **hai nguyên nhân hỏng khác nhau**: phản hồi bị cắt (`finishReason=MAX_TOKENS`) thì phải tăng token, còn model kèm lời dẫn thì chỉ cần bóc lại chuỗi. Hai lỗi này mà báo chung một câu thì người sửa mò sai hướng. Phản hồi không parse được được ghi ra `store/last_bad_response.txt` để còn soi, chứ không im lặng nuốt.

### 4. Guard grounding — `_ground()`, và vì sao nó nằm trong code

Đây là phần mình coi là quan trọng nhất trong toàn bộ phần việc của mình. Một action item chỉ được lên UI khi thoả **đồng thời**: `confidence == "high"`, `source_id` có thật trong tập nguồn, và `evidence` là **chuỗi con nguyên văn** của tin gốc (`evidence in sources[source_id]`). Trượt bất kỳ điều kiện nào thì không bị xoá đi — nó **rơi xuống `needs_confirmation`** kèm sẵn câu hỏi để đi hỏi TA/BTC. `priority` cũng bị lọc theo whitelist `{urgent, today, upcoming}`, sai thì ép về `today`.

Guard đặt trong Python chứ không đặt trong prompt vì prompt có thể bị thuyết phục bởi một tin nhắn viết chắc nịch, còn `evidence in sources[source_id]` thì không. Đây là chỗ đỡ điều kiện cứng **0 case bịa căn cứ** của quality bar.

### 5. Cache theo fingerprint — `scan()`

Free-tier chỉ khoảng 20 request/model/ngày, mà demo thì bấm nút liên tục. `scan()` băm `sha256` của `[reference_date] + [(id, text) của mọi thông báo]` làm fingerprint; cùng ngày tham chiếu và cùng bộ tin thì trả lại kết quả trong `store/scan_cache.json` và gắn `meta.cached = True`. Đẩy một tin mới lên qua cửa sổ Discord là fingerprint đổi → gọi API thật. `force=True` để quét lại có chủ đích.

Mỗi lượt gọi thật ghi một dòng trace vào `logs/agent_runs.jsonl`: thời điểm, **model đã dùng**, số nguồn, số action, số mục cần xác nhận — hiện có 25 lượt trên pack thật.

### 6. Adapter API Codelabs — `codelab.py`

Prototype chưa có quyền truy cập Codelabs thật, nên mình viết module này **theo đúng hình dạng của một API thật** thay vì nhét dữ liệu cứng vào UI: `check_submission(student_id, reference_date)` trả về `lab_id / open_at / due_at / submitted / checked_at / url / source`, đọc-ghi trạng thái ở `store/codelab.json`. Có `LATENCY_SECONDS = 0.4` để spinner phản ánh đúng rằng đây là một lượt gọi mạng. Mặc định là **chưa nộp**, vì đó mới là nhánh cần nhắc. Khi có API thật, chỉ thay ruột `check_submission()`; UI không phải đổi một dòng.

## Mình dùng AI thế nào để làm phần đó

**AI làm tốt — phần khung.** Dựng request `urllib`, đọc/ghi JSON có `mkdir(parents=True)`, tách hàm cache. Phần này AI viết nhanh hơn mình gõ tay nhiều và mình giữ gần như nguyên.

**AI làm sai — mọi thứ thuộc về *hành vi thật* của API.** Ba chỗ mình phải tự sửa:

- AI viết `json.loads(response["candidates"][0]["content"]["parts"][0]["text"])`. Đúng với model thường, **hỏng với model dòng thinking** vì part đầu tiên là phần suy nghĩ. Mình phải đọc lại cấu trúc phản hồi thật rồi lọc theo cờ `thought` — thành `_answer_text()`.
- AI xử lý mọi lỗi HTTP như nhau, và khi mình kể bị 429 thì nó đề xuất thêm `time.sleep()` rồi retry **cùng model**. Với quota theo ngày thì đó là ngồi chờ vô ích. Mình phải mở body lỗi ra đọc `quotaId` mới phân biệt được PerMinute và PerDay — logic này (`_quota_kind()`) AI không tự nghĩ ra vì nó không thấy lỗi thật của mình.
- AI đề xuất viết guard thành một câu dặn trong prompt: *"chỉ trích dẫn nguyên văn, không được bịa"*. Mình không dùng. Một câu dặn không phải một điều kiện kiểm được, và quality bar của nhóm cần con số 0 case bịa — thứ chỉ chứng minh được bằng một hàm chạy được và có test (`test_guards.py`, 7/7 đạt).

**Chỗ mình chủ động không nghe AI.** Khi thấy vài action bị guard đánh rớt vì lệch khoảng trắng, AI đề xuất chuẩn hoá chuỗi hoặc so khớp mờ cho "đỡ fail oan". Mình bỏ. Nới điều kiện so khớp chính là nới đúng cái điều kiện cứng mà cả sản phẩm dựa vào; một việc rơi nhầm xuống *Cần xác thực* thì người dùng vẫn thấy và vẫn hỏi được, còn một trích dẫn bịa lọt lên bản tin thì không ai chặn nữa.

## Một bài học từ case fail của chính nhóm

**Lượt đo 02 (`eval/run-02.md`) — 16/28 = 57,1%, recall `NGAY` 80% (bỏ sót G14), 1 case bịa căn cứ. Trượt cả ba điều kiện.**

Nguyên nhân không nằm ở prompt (vẫn v3) và không nằm ở golden set. Nó nằm **đúng trong phần của mình**: `gemini-2.5-flash` bị 503 kéo dài phía Google, chuỗi dự phòng của mình lặng lẽ tụt xuống `gemini-2.5-flash-lite`, và lượt đo đó thực chất đang đo một model khác. Cơ chế mình viết ra để app *không bao giờ chết* đã làm kết quả đo *không còn so sánh được*.

Điều làm mình nhớ lâu là hai mục tiêu này ngược nhau và mình đã chỉ nghĩ tới một cái. Với nhánh demo, đổi model là đúng — thà chạy bằng model yếu hơn còn hơn đứng hình trước giám khảo. Với nhánh đo, đổi model là hỏng — 57,1% không nói lên gì về prompt v3, và nếu không ai để ý thì nhóm đã ngồi sửa prompt cho một lỗi hạ tầng.

Hai thứ mình sửa sau đó:

1. **Model phải đi kèm kết quả.** `_grounded_scan()` gắn `meta = {model, cached, at}` vào mọi kết quả, và mỗi lượt gọi thật ghi tên model vào `logs/agent_runs.jsonl`. Không còn kết quả nào ẩn danh model.
2. **Đổi model = baseline mới.** Nhóm chốt quy ước ghi thẳng vào `spec.md` §7: lượt nào đổi model thì không so trực tiếp với lượt trước. Quy ước này sau đó dùng lại cho lượt 03 (lên `gemini-3.6-flash`) và cho lượt 05 khi anh Nam đổi prompt v3 → v4.

Nhóm cũng cố ý **giữ lượt 02 trong bảng** dù nó xấu, vì nó là bằng chứng quality bar thật sự phân biệt được model chứ không phải cái bar ai chạy cũng qua.

Bài học của mình: **một quyết định hạ tầng có thể đổi kết quả AI mà không để lại dấu vết nào trên màn hình.** Fallback, cache, retry đều là thứ "chạy cho êm" — và đúng vì êm nên chúng nguy hiểm với một sản phẩm mà cả nhóm đang đo bằng con số. Từ đó mình mặc định: cái gì có thể im lặng đổi kết quả thì phải tự khai tên nó ra trong log.

Chỗ liên quan mà mình còn thấy chưa yên tâm: cache theo fingerprint cũng đúng loại rủi ro đó. Nó chỉ băm `reference_date` và nội dung tin — **không băm tên model và không băm phiên bản prompt**. Đổi prompt hay đổi chuỗi model mà bộ tin không đổi thì `scan()` vẫn trả kết quả cũ. Hiện nhóm đang chữa bằng tay (`clear_cache()` / nút đặt lại phiên demo), nhưng đúng ra fingerprint phải gồm cả hai trường đó.

## Nếu có thêm thời gian

1. **Đưa model + version prompt vào fingerprint của cache**, để không bao giờ lặp lại đúng loại lỗi của lượt 02 ở tầng cache.
2. **Thay `codelab.py` bằng API thật** — chữ ký đã dựng sẵn cho việc này, chỉ cần thay ruột `check_submission()` và thêm phần xác thực.
3. **Đọc Discord qua API thật thay vì file export**, sau khi chuẩn hoá được các trường `ts / vai / tác giả / trả lời cho` mà anh Hoàng cần cho golden set — hiện `discord_store.py` mới chỉ có `date` và `author` gán cứng là `LabCoach / BTC` cho toàn bộ pack, tức là guard nguồn không chính thức đang thiếu dữ liệu để làm việc trên dữ liệu thật.

---

### Trả lời được cho vibe-coding rule (CP5/CP6)

| Câu hỏi | Trả lời của mình |
|---|---|
| Phần bạn làm là gì? | `discord_store.py` (đọc pack + kho tin mô phỏng), `discord_agent.py` (gọi Gemini, chuỗi model dự phòng, bóc JSON, guard `_ground()`, cache fingerprint), `codelab.py` (adapter API nộp bài) |
| Một lượt quét chạy thế nào? | `all_messages()` gom pack + inbox → băm fingerprint, trúng cache thì trả luôn → `_prompt()` dựng nguồn có `[SOURCE id]` → `_generate()` thử lần lượt chuỗi model → `_extract_json()` bóc JSON → `_ground()` lọc theo trích dẫn nguyên văn → ghi cache + trace |
| Vì sao guard nằm trong code chứ không trong prompt? | Prompt bị thuyết phục được bởi một tin viết chắc nịch; `evidence in sources[source_id]` thì không. Và nó có test riêng trong `test_guards.py` |
| Vì sao phải có chuỗi model dự phòng? | Quota free-tier tính riêng cho từng model mỗi ngày; model chính hết quota thì chờ vô ích, phải đổi model |
| Vì sao phải cache? | ~20 request/model/ngày — mỗi lần bấm nút không được đốt một request. Fingerprint đổi khi có tin mới thì mới gọi API thật |
| Cái gì đã đi sai vì phần của bạn? | Lượt 02: fallback lặng lẽ đổi sang `gemini-2.5-flash-lite`, kết quả tụt còn 57,1%. Sửa bằng cách gắn `meta.model` vào kết quả + ghi model vào trace + quy ước "đổi model = baseline mới" |
| Augment hay automate? | `conditional` — lý do cost-of-error ở `spec.md` §4 |
