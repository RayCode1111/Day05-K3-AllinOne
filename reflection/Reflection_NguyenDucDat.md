# Reflection — 

**Họ và tên:** [Nguyễn Đức Đạt]  
**Mã học viên:** [2A202601633]  
**Nhóm:** AllInOne  
**Sản phẩm:** Nova - Agentic tổng hợp và nhắc thông báo Discord cho học viên
**Vai trò:** Thiết kế giao diện dashboard & trải nghiệm (UX)

---

## Vai trò của mình trong nhóm

Mình phụ trách **toàn bộ tầng giao diện** của Nova — file `codebase/app.py`. Nói cho đúng phạm vi: mình không viết phần gọi Gemini (anh Quyền), không viết prompt (anh Nam), không dựng golden set (anh Hoàng). Việc của mình là câu hỏi đứng ngay sau đó: **khi agent đã trả về kết quả rồi thì bày ra màn hình thế nào để một người đã mute server chịu tin và chịu dùng.**

Đó không phải việc trang trí. Người dùng của nhóm là người **đã từ chối** một kênh thông tin một lần rồi (7/11 người khảo sát đã mute). Nếu màn hình của mình bày ra 28 thông báo hoặc bày ra một danh sách việc nghe chắc nịch mà không kiểm được, thì sản phẩm tái tạo đúng cái vấn đề nó sinh ra để giải. Nên nguyên tắc mình tự đặt cho phần của mình là: **mọi thứ Nova nói phải mở ra được tin gốc, và mọi thứ Nova giấu phải xem lại được.**

## Phần mình trực tiếp làm

Tất cả nằm trong `codebase/app.py`:

**1. Tách hai màn — *Hôm nay* và *Cần xác thực*** (`page = st.radio(...)`, dòng 290).
Đây là quyết định thiết kế lớn nhất của mình và nó đến từ một ràng buộc của sản phẩm chứ không phải từ thẩm mỹ. Agent trả về hai thứ khác hẳn nhau: `action_items` (đã qua guard, có trích dẫn khớp nguyên văn) và `needs_confirmation` (chưa đủ căn cứ). Nếu trộn chung một danh sách thì người dùng không phân biệt được cái nào Nova dám đảm bảo. Mình tách hẳn thành hai màn, và màn *Cần xác thực* mở đầu bằng đúng một câu nói rõ nó là gì: *"Chỉ hiển thị thông tin thiếu dữ kiện, mâu thuẫn ngày giờ hoặc chưa đủ rõ để Nova đưa vào danh sách việc."*

**2. `current_tasks()` (dòng 66) — chỉ đọc từ `result["action_items"]`, không có đường vòng.**
Hàm này cố tình không có nhánh nào dựng việc từ dữ liệu khác. Guard `_ground()` bên `discord_agent.py` đã đẩy mọi thứ không khớp căn cứ sang `needs_confirmation`, nên nếu UI của mình còn một đường nào khác để hiển thị việc, guard coi như vô hiệu. Nó rỗng khi chưa quét, và nó rỗng thật chứ không hiện dữ liệu mẫu.

**3. Mỗi dòng việc là một đường dẫn về nguồn** (`task_row()`, dòng 208 và `source_dialog()`, dòng 108).
Mỗi việc hiện `Căn cứ: "…"` — đoạn trích nguyên văn — cộng một nút mở ra **đúng tin gốc kèm kênh, người gửi, ngày đăng**. Người dùng Ctrl+F được. Đây là chỗ mình áp G11 (giải thích vì sao) và PAIR *Explainability + Trust*: mục tiêu không phải làm người ta tin tối đa, mà tin **đúng mức**.

**4. Thẻ Codelabs + nút "Tôi đã nộp — kiểm tra lại"** (`codelab_card()`, dòng 165).
Nova có một kết luận rất dễ sai: "bạn chưa nộp bài". Mình không giấu kết luận đó đi cho an toàn, mà đặt ngay cạnh nó một nút để người dùng sửa lại trong một cú bấm (G9 — sửa dễ dàng). Nếu chưa nộp thì có luôn link mở Codelabs — sửa xong là làm được việc luôn, không phải đi tìm.

**5. Cửa sổ Discord mô phỏng** (`discord_dialog()`, dòng 120).
Hai mục đích. Demo được cảnh "có tin mới đẩy lên → quét lại → Nova cập nhật" mà không cần Discord API thật. Và quan trọng hơn: nó liệt kê **toàn bộ** thông báo Nova được đọc — cả 28 tin từ data pack lẫn tin mới đẩy — nên người dùng luôn kiểm được thứ Nova đã bỏ qua (G17 — quyền kiểm soát tổng). Badge `💬 Discord · N mới` ở header đếm số tin chưa được quét.

**6. Ba con số trên thẻ hero** (`hero_content()`, dòng 185): *đã đọc N thông báo · M việc có căn cứ · K mục cần xác nhận*.
Con số K là con số mình cố ý để lộ ra. Nó nói thẳng "có K thứ Nova không dám kết luận". Đặt kỳ vọng thấp hơn khả năng thật, đúng chương *Mental Models* của PAIR.

**Ba lỗi mình phải tự sửa, và mình giải thích được từng cái** *(đều còn comment trong code)*:

- **Tick "hoàn thành" tự bật lại sau khi quét lại** (dòng 210-214). Streamlit ưu tiên giá trị cũ của widget key hơn tham số `value`, nên checkbox vẫn checked dù `completed_task_ids` đã bị xoá. Sửa bằng cách gán lại `st.session_state[key] = completed` **trước** khi vẽ, và lấy `completed_task_ids` làm nguồn sự thật duy nhất.
- **Cửa sổ Discord tự bật lại mỗi lần bấm bất cứ thứ gì** (dòng 346-355). Streamlit không báo lại khi người dùng đóng dialog bằng nút ✕, nên cờ `show_discord` giữ nguyên `True` và dialog bật lại ở mọi lượt rerun sau đó. Sửa bằng cách cho cờ chỉ sống đúng một lượt: đọc xong là đặt lại `False` ngay rồi mới gọi dialog.
- **Thông báo lỗi biến mất trước khi ai kịp đọc** (`refresh_today()`, dòng 91-106). Ban đầu mình in lỗi quét ngay trong hàm, nhưng màn hình rerun ngay sau đó nên nó bị xoá. Sửa bằng cách cất lỗi vào `st.session_state.scan_error` rồi mới hiện ở lượt vẽ tiếp theo — và hiện dưới dạng *"Đã lấy được trạng thái Codelabs, nhưng chưa quét được Discord"*, tức là nói rõ **phần nào vẫn dùng được**, thay vì báo lỗi toàn màn.

## Mình dùng AI thế nào để làm phần đó

Mình dùng AI ở hai việc rất khác nhau, và kết quả cũng khác nhau rõ rệt.

**Việc AI làm tốt — dựng khung và CSS.** Mình mô tả bố cục muốn có (sidebar tiến độ, hero, danh sách việc có badge mức ưu tiên, thẻ Codelabs) và nhờ sinh khung Streamlit + khối CSS. Phần này AI làm nhanh hơn mình gõ tay nhiều, nhất là khối `st.markdown` CSS ở đầu file. Mình giữ gần như nguyên phần màu sắc và bo góc.

**Việc AI làm sai — mọi thứ liên quan tới trạng thái giữa các lượt rerun.** Cả ba lỗi kể ở trên đều nằm trong code AI sinh ra, và cả ba đều **chạy đúng trong lần bấm đầu tiên** rồi mới sai ở lần thứ hai. AI viết `st.checkbox(..., value=completed)` — đúng theo tài liệu, sai theo cách Streamlit thật sự ưu tiên widget key. Mình phải tự dựng lại mô hình "một lượt chạy lại của Streamlit gồm những gì" rồi sửa tay, chứ hỏi lại AI thì nó đề xuất vòng vo (thêm `st.rerun()`, đổi key) mà không chạm vào nguyên nhân.

**Chỗ mình chủ động không nghe AI.** Khi mình mô tả màn hình, AI đề xuất gộp `needs_confirmation` vào cuối danh sách việc cho "gọn màn hình". Mình bỏ đề xuất đó. Gọn hơn thật, nhưng nó xoá mất đúng ranh giới mà cả sản phẩm dựa vào: cái gì Nova có căn cứ và cái gì không. Đây là chỗ mình thấy rõ nhất là AI tối ưu cho *đẹp mắt*, còn ràng buộc của bài này là *đáng tin* — hai thứ đó không phải lúc nào cũng cùng hướng, và người phải chọn là mình.

**Bài học về cách dùng AI:** AI viết hộ được thứ *nhìn thấy được* (bố cục, màu, chữ). Thứ *không nhìn thấy được* — trạng thái, thứ tự chạy, và ranh giới tin/không-tin — thì mình phải tự hiểu, vì đó cũng đúng là thứ nếu sai thì demo mới lộ.

## Một bài học từ case fail của chính nhóm

**Case G22, tin `M18`, sai ở cả lượt 05 và lượt 06** (`eval/run-05.md`, `eval/run-06.md`).

Tin: TA trả lời cách nộp link repo, mỗi bạn nộp riêng vào form. Nhãn vàng là `GHI_NHO`, agent trả `BO_QUA` — tức là **Nova giấu hẳn tin này đi**. Nó lặp lại y hệt ở hai lượt liên tiếp, nên không phải nhiễu mà là lỗi định nghĩa ổn định.

Điều làm mình chú ý là hướng sai: đây là loại tin "hướng dẫn thao tác" — không có hạn riêng, nhưng thiếu nó thì nộp bài sai cách. Và nhóm quyết định **không sửa bằng cách thêm luật vào prompt**, vì luật mới sẽ kéo cả nhóm tin hướng dẫn lên bản tin và làm bản tin dài ra — đúng thứ sản phẩm sinh ra để chống.

Bài học rơi đúng vào phần của mình: **một quyết định "bỏ qua" của agent không phải lúc nào cũng sửa được bằng cách dạy agent kỹ hơn — nhiều khi phải sửa bằng cách để người dùng lấy lại được thứ đã bị bỏ.** Trước case này mình coi cửa sổ Discord và danh sách "thông báo trong data pack" là thứ phụ, làm cho có để demo. Sau case này mình hiểu nó là **cái van an toàn cho một loại lỗi mà nhóm đã biết là sẽ còn xảy ra**: 96,4% đúng mức nghĩa là vẫn còn tin bị xếp sai, và người dùng cần một chỗ để tự tìm lại nó mà không phải quay về cuộn Discord — tức là quay về đúng cái việc họ trả tiền bằng 22,5 phút mỗi ngày.

Cũng chính vì vậy mà khi đọc data pack thật, chỗ mình thấy đáng sợ nhất không phải một tin sai, mà là cặp `thong-bao#15` / `thong-bao#16`: hai thông báo **chính thức** nói Workshop 4 lúc 20:00 và 19:00. Không có luật prompt nào chọn đúng được, vì không có đáp án đúng trong data. Màn *Cần xác thực* là câu trả lời của mình cho tình huống đó — Nova đặt hai trích dẫn cạnh nhau và đưa sẵn câu hỏi để người học đi hỏi BTC, thay vì chọn bừa một giờ rồi nói bằng giọng chắc nịch.

---

### Trả lời được cho vibe-coding rule (CP5/CP6)

| Câu hỏi | Trả lời của mình |
|---|---|
| Phần bạn làm là gì? | Toàn bộ `codebase/app.py` — hai màn *Hôm nay* / *Cần xác thực*, thẻ việc kèm căn cứ + dialog tin gốc, thẻ Codelabs, cửa sổ Discord mô phỏng |
| Vì sao tách màn *Cần xác thực* riêng? | Vì `action_items` đã qua guard còn `needs_confirmation` thì chưa. Trộn chung là xoá mất ranh giới tin/không-tin |
| Vì sao mỗi việc phải có nút mở tin gốc? | Người dùng đã mute một lần rồi; họ chỉ tin lại nếu kiểm lại được. G11 + PAIR *Explainability + Trust* |
| Augment hay automate? | `conditional` — lý do cost-of-error ở `spec.md` §4 |
| Failure nguy hiểm nhất? | Bỏ sót tin đổi lịch. Không sửa được, và 7/11 người khảo sát đã dính |
| Vì sao guard nằm trong code chứ không trong prompt? | Prompt bị thuyết phục được bởi một tin viết chắc nịch; hàm kiểm chuỗi con nguyên văn thì không |
