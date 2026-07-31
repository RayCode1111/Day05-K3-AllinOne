# Bài tự phản ánh cá nhân

**Họ và tên:** [Nguyễn Trọng Nam]  
**Mã học viên:** [2A202601529]  
**Nhóm:** Nguyễn Trọng Nam - Nguyễn Đức Đạt - La Thế Quyền - Lê Quốc An  
**Sản phẩm:** Nova - Agentic tổng hợp và nhắc thông báo Discord cho học viên

## 1. Vai trò của tôi trong nhóm

Trong nhóm, tôi phụ trách chính phần **[điền phần bản làm: spec / evidence / prompt + golden set / code prototype / demo + slide]**. Công việc của tôi gắn với mục tiêu chung là giúp sản phẩm không chỉ “tóm tắt thông báo”, mà phải tạo ra một bản tin cho học viên có thể dùng để quyết định việc cần làm trong ngày.

Nếu phải tóm tắt một câu: tôi đóng góp vào việc biến vấn đề “bị trôi thông báo Discord” thành một prototype có luật rõ ràng, có AI chạy đúng, có guard chống bịa, và có bộ eval để đo xem agent có đang tin hay không.

## 2. Những việc tôi đã làm

Những việc cụ thể tôi đã tham gia:

- Đọc đề bài và rubric để cắt đúng format: một học viên đã tắt Discord, cuối ngày nhận một bản tin tối đa 5 mục, trong đó AI quyết định tin nào là NGAY, HOM_NAY, GHI_NHO hay BO_QUA.
- Tham gia chốt problem statement dựa trên evidence: 17/20 người từng trễ deadline hoặc bị trừ điểm, 7/11 người từng đi nhầm phòng hoặc đến lớp khi đã hủy, và 15/20 người đã mute server vì spam.
- Góp phần xây bộ tiêu chí “tốt”: đúng mục, có căn cứ truy vét được, và đường lùi đúng khi mở hộ/ngoài phạm vi thẩm quyền.
- Tham gia tạo hoặc kiểm tra golden set 28 case, bao gồm case thường, case hiếm và 4 lớp khó: nguồn sự thật, mở hộ/thiếu thông tin, ngoài phạm vi/thẩm quyền, và đặc thù domain.
- Theo dõi các lượt eval. Kết quả hiện tại ở lượt 06 đạt quality bar: 27/28 case đúng mục = 96,4%, recall NGAY = 100%, và 0 case bịa căn cứ.
- Góp ý/kiểm tra hành vi guard: khi trích dẫn không khớp, hạn chót không có căn cứ, hoặc nguồn không chính thức, agent không được đẩy kết luận lên như thông báo chắc chắn.

## 3. AI đã hỗ trợ tôi như thế nào

Tôi dùng AI như một công cụ tăng tốc, không phải người quyết định thay nhóm.

AI hỗ trợ tốt nhất ở ba việc:

- Viết và lặp lại prompt: từ prompt ban đầu, nhóm đọc output thật, đặt tên lỗi, rồi sửa prompt thành v4. Ví dụ case G17 cho thấy tin vừa có link tài liệu vừa có việc phải làm trong ngày bị xếp mở hộ; sau đó nhóm thêm luật “tài liệu kèm việc phải làm thì tính theo việc, không tính theo tài liệu”.
- Sinh và đọc nhanh các biến thể case: AI giúp nghĩ ra nhiều tình huống biến thể như tin định chính, deadline đã qua, tin chỉ có ảnh, học viên xin đáp án, hoặc thông báo chung không có việc cần làm.
- Hỗ trợ code/prototype/eval: AI giúp đẩy nhanh việc viết hàm phân loại, guard và format kết quả, nhưng nhóm vẫn phải chạy eval và đọc từng case fail để quyết định sửa cái gì.

Điểm quan trọng tôi học được là AI có thể tạo ra output nhìn rất hợp lý, nhưng nếu không có rubric chấm rõ thì nhóm rất dễ chấm theo cảm tính. Vì vậy phần “định nghĩa tốt” và golden set mới là chỗ giữ sản phẩm đúng hướng.

## 4. Một case fail đáng nhớ của nhóm

Case fail đáng nhớ nhất với tôi là G17 (M02). Tin này vừa có link slide/tài liệu mới, vừa dẫn học viên tải và dùng trước khi vào lớp. Ở các lượt đầu, agent bị kéo về GHI_NHO vì thấy đây là tài liệu mới, trong khi đúng ra nó phải là HOM_NAY vì có việc cần làm trong ngày.

Lỗi này nguy hiểm vì nó không phải “model kém” kiểu trả lời vô nghĩa. Nó sai vì chính định nghĩa trong prompt còn mờ: cùng một tin khớp hai dòng trong bảng mục, nhưng nhóm chưa nói dòng nào thắng. Nếu chỉ nhìn tỷ lệ đúng chung, lỗi này có thể bị bỏ qua; nhưng khi đọc case fail, nhóm thấy đây là lỗi định nghĩa sản phẩm.

Sau case này, nhóm thêm luật 8 vào prompt v4: nếu tài liệu/link mới đi kèm việc phải làm trong ngày thì xếp theo mốc thời gian của việc, không xếp GHI_NHO. Sau khi chạy lại, G17 đúng và tổng kết quả tăng lên 27/28. Bài học của tôi: với sản phẩm AI, sửa prompt tốt không phải thêm thật nhiều câu, mà là làm rõ đúng một ranh giới đang gây sai.

## 5. Điều tôi sẽ làm khác nếu có thêm thời gian

Nếu có thêm một tuần, tôi sẽ ưu tiên hai việc:

1. Triển khai thực tế vào discord
2. Hoàn thành validation với ít nhất 5 học viên ngoài nhóm, ghi quote nguyên văn để biết người dùng có thật sự tin bản tin và hiểu mục “Chưa chắc – nên hỏi TA” hay không.
3. Đưa thêm dữ liệu Discord thật vào eval sau khi chuẩn hóa được các trường ts, vai, tác giả, trả lời cho, để golden set gần với dữ liệu thực hơn nhưng vẫn giữ được 4 lớp khó.


## 6. Bài học cá nhân

Bài học lớn nhất của tôi là: xây dựng sản phẩm AI không bắt đầu bằng “AI làm được gì”, mà bắt đầu bằng “nếu AI sai thì ai bị mất gì”. Với bài toán thông báo Discord, lỗi nguy hiểm nhất không phải tóm tắt chưa hay, mà là bỏ sót tin khẩn, bịa deadline, hoặc đẩy tin đơn thành thông báo chính thức. Khi nhóm đạt quality bar gồm recall NGAY = 100% và 0 case bịa căn cứ, tôi thấy rõ hơn cách biến một prototype AI từ chỗ “có vẻ thông minh” thành một thứ có thể tranh luận, đo lường và cải tiến.
