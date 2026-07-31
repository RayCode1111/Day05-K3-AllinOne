 # Reflection cá nhân — Lê Việt Hoàng

## Vai trò

Trong nhóm, tôi phụ trách **Thiết lập Logic Giám sát & Đánh giá (Evaluate)**. Công việc chính của tôi gồm:

- Xác định các chiều chất lượng cần theo dõi: đúng mức phân loại, căn cứ truy vết được và đường lui đúng.
- Thiết lập golden set, các case khó và logic kiểm tra guard để phát hiện lỗi bịa căn cứ, hạn chót không có căn cứ hoặc nguồn tin không chính thức.
- Chạy và phân tích các lượt đánh giá, đối chiếu kết quả với quality bar, sau đó ghi nhận từng case fail để nhóm sửa prompt và đo lại.

## Phần tôi đã làm

Tôi sử dụng dữ liệu từ Google Form và mining làm đầu vào để thiết lập các tiêu chí đánh giá có liên hệ với hậu quả thực tế. Các kết quả chính được nhóm sử dụng là: 8/11 người từng bị trễ hạn hoặc bị trừ điểm, 7/11 người từng đi nhầm phòng hoặc đến lớp khi đã được nghỉ, và 7/11 người phải mute server vì spam `@everyone`/`@here`. Dữ liệu gốc và cách tổng hợp được lưu trong `eval/survey-responses.csv` và `eval/mining-log.md`.

Tôi cũng kiểm tra giới hạn của khảo sát. Mẫu chỉ có 11 người, chưa đạt yêu cầu tối thiểu 20 người của evidence chuẩn A. Một số câu hỏi dùng danh sách lựa chọn có sẵn nên có thể tạo thiên lệch; câu hỏi về mức hữu ích của AI là câu dẫn dắt và không được dùng làm bằng chứng pain chính. Vì vậy, nhóm chỉ dùng các câu trả lời về vấn đề và hậu quả đã thực sự xảy ra, đồng thời bổ sung mining từ thông báo Discord để có nguồn kiểm chứng độc lập.

Tôi thiết lập và theo dõi kết quả theo từng case thay vì chỉ nhìn phần trăm tổng. Golden set có 28 case, gồm các case khó thuộc bốn lớp rủi ro, case thường và case hiếm. Lượt hiện hành đạt 27/28 đúng mức (96,4%), recall mức `NGAY` đạt 100% và không có case bịa căn cứ. Các guard cũng có test riêng, trong đó kiểm tra việc xoá hạn chót hoặc hạ mức tin khi trích dẫn không khớp và khi nguồn là tin đồn của học viên. Kết quả được đối chiếu với quality bar: đúng mức tối thiểu 80%, recall `NGAY` 100% và 0 case bịa căn cứ.

## AI đã hỗ trợ tôi như thế nào

AI hỗ trợ nhóm đọc và tổng hợp dữ liệu, gợi ý các tình huống cần đưa vào golden set, tạo corpus kiểm thử và chạy nhiều lượt đánh giá. AI cũng giúp phát hiện các trường hợp dễ bị xử lý sai, nhưng tôi không xem kết quả của AI là bằng chứng tự thân. Tôi kiểm tra lại số lượng case, nhãn vàng, quality bar và từng case fail trong các file kết quả. Phần quyết định cuối cùng về tiêu chí pass/fail, việc giữ nguyên hay thay đổi quality bar và cách diễn giải lỗi vẫn do tôi cùng nhóm đối chiếu với dữ liệu gốc.

## Bài học từ một case fail

Case G22 (`M18`) là bài học rõ nhất. Tin nói về việc mỗi thành viên phải nộp link repo riêng vào form. Nhãn vàng là `GHI_NHO`, nhưng agent lại trả `BO_QUA`, vì nó xem đây là thông tin không có hạn riêng. Lỗi này cho thấy phân loại không chỉ dựa vào việc tin có deadline hay không; một việc cần ghi nhớ vẫn có giá trị hành động dù không có hạn cụ thể.

Từ case này, tôi học được rằng khi thiết lập logic Evaluate phải đọc cả lý do của nhãn vàng và kiểm tra những case nằm ở ranh giới giữa “không cần hành động” và “cần ghi nhớ”. Chỉ đạt phần trăm cao chưa đủ; cần xem từng lỗi có thể làm người dùng bỏ sót việc gì và có vi phạm quality bar hay không. Tôi cũng rút ra rằng golden set nên có các case về hành động thực tế, không chỉ về mức độ hài lòng hoặc mong muốn có tính năng.

## Tự đánh giá

Đóng góp của tôi giúp nhóm biến dữ liệu đầu vào thành hệ thống đánh giá có tiêu chí, case kiểm thử và kết quả đối chiếu được. Điểm còn thiếu là golden set chưa có đủ 10 case lấy từ chatlog thật theo gợi ý của rubric, và phản hồi validation với người dùng cần được ghi đầy đủ hơn trong `validation/feedback-log.md`. Nếu làm lại, tôi sẽ lập bảng mapping giữa từng phát hiện khảo sát, rủi ro người dùng và case trong golden set ngay từ đầu; đồng thời bổ sung các case biên để kiểm tra độ ổn định của logic đánh giá.
