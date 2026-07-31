# Reflection cá nhân — Lê Quốc An

**Mã học viên:** 2A202601811  
**Nhóm:** Nguyễn Trọng Nam · Nguyễn Đức Đạt · La Thế Quyền · Lê Quốc An  
**Sản phẩm:** Nova — trợ lý tổng hợp thông báo Discord cho học viên

## Vai trò của mình trong nhóm

Mình phụ trách phần **phát triển prototype**, đồng thời **hỗ trợ kiểm thử, vận hành triển khai và hoàn thiện trải nghiệm UI/UX**. Mục tiêu của phần việc này là biến luồng AI phân loại thông báo thành một trải nghiệm mà học viên có thể hiểu, kiểm tra lại nguồn tin và thao tác ngay, thay vì chỉ xem một kết quả tóm tắt.

## Phần mình trực tiếp làm

- Phát triển và hoàn thiện giao diện Streamlit trong `codebase/app.py`: màn hình tổng quan, danh sách việc cần làm, khu vực việc đã hoàn thành, trạng thái Codelabs, thông báo Discord mô phỏng và hộp thoại xem nguồn gốc.
- Thiết kế luồng UI/UX theo trạng thái của người dùng: sau khi quét, việc có căn cứ xuất hiện trong danh sách cần làm; mục chưa chắc được tách riêng để người dùng không nhầm với kết luận đã xác nhận; mỗi việc có thể mở lại thông báo nguồn để kiểm tra.
- Hoàn thiện thao tác checkbox hoàn thành/chưa hoàn thành. Trạng thái được lưu trong `st.session_state.completed_task_ids`; callback `update_task_completion()` đồng bộ trạng thái trước khi Streamlit render lại, nên việc được chuyển đúng giữa hai danh sách ngay khi tick hoặc bỏ tick.
- Hỗ trợ vận hành demo: kiểm tra cấu hình `.env`, chế độ dữ liệu, luồng “Kiểm tra hôm nay”, trạng thái lỗi khi quét và thao tác đặt lại phiên demo để có thể chạy lại kịch bản ổn định.
- Hỗ trợ kiểm thử prototype bằng golden set và các lượt eval. Ở `eval/run-06.md`, hệ thống đạt 27/28 case đúng mức (96,4%), recall mức `NGAY` 5/5 và không có case bịa căn cứ.

## Mình dùng AI thế nào để làm phần đó

Mình dùng AI để hỗ trợ phác thảo cấu trúc giao diện, rà soát các trạng thái dễ gây nhầm lẫn và đề xuất cách tổ chức session state trong Streamlit. AI cũng hỗ trợ diễn giải các case kiểm thử thành tình huống người dùng có thể quan sát được trên giao diện.

Tuy nhiên, mình không dùng AI để tự quyết định giao diện đã đúng hay luồng đã an toàn. Mình đối chiếu lại với yêu cầu của sản phẩm: kết quả chỉ đáng tin khi có căn cứ; phần chưa chắc phải được hiển thị như một câu hỏi để xác nhận, không phải một việc chắc chắn. Khi có lỗi checkbox, mình kiểm tra vòng đời rerun của Streamlit và chuyển việc cập nhật state sang callback thay vì ghi state ngay trong lúc render widget.

## Một case lỗi và bài học rút ra

Lỗi UI/UX đáng chú ý là checkbox hoàn thành trước đây không chuyển việc nhất quán giữa hai khu vực “Việc cần làm” và “Đã hoàn thành”. Nguyên nhân là danh sách được phân loại theo trạng thái ở đầu lượt render, trong khi trạng thái checkbox lại được cập nhật trong lúc vẽ giao diện. Vì vậy, người dùng có thể tick/bỏ tick nhưng vẫn nhìn thấy task ở danh sách cũ trong lượt chạy đó.

Mình sửa bằng cách dùng callback `on_change` cho checkbox. Callback đọc giá trị từ `st.session_state` và cập nhật `completed_task_ids` trước khi ứng dụng render lại. Nhờ đó, task được đưa sang đúng danh sách, đồng thời tiêu đề gạch ngang và badge “Đã xong” cũng phản ánh đúng trạng thái.

Bài học của mình là một trải nghiệm AI đáng tin không chỉ phụ thuộc vào output của model. Những thao tác nhỏ như đánh dấu hoàn thành, xem nguồn hoặc phân biệt “đã xác nhận” với “cần xác nhận” phải nhất quán; nếu không, người dùng sẽ mất niềm tin ngay cả khi phần phân loại phía sau hoạt động tốt.

## Nếu có thêm thời gian

Mình sẽ ưu tiên:

1. Thực hiện user test với học viên ngoài nhóm để đo xem họ có hiểu ngay ý nghĩa của mục “Cần xác nhận” và có tìm được thông báo nguồn hay không.
2. Bổ sung kiểm thử tự động cho các trạng thái giao diện quan trọng: tick/bỏ tick, quét lại dữ liệu, lỗi API và đặt lại phiên demo.
3. Chuẩn bị kịch bản triển khai demo ổn định hơn, gồm dữ liệu mẫu, kiểm tra biến môi trường và phương án dự phòng khi dịch vụ AI không phản hồi.
