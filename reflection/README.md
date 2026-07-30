# Reflection cá nhân

Mỗi thành viên **một file riêng**: `reflection/<ten-cua-ban>.md`. Chấm riêng theo rubric reflection của khoá.

Sao chép khung dưới đây vào file của mình.

---

```markdown
# Reflection — [Tên] · [Mã HV]

## Vai trò của mình trong nhóm

## Phần mình trực tiếp làm
*(Ghi cụ thể tới file/hàm. Vibe-coding rule: bị hỏi ngẫu nhiên tại CP5/CP6 mà
không giải thích được phần có tên mình → 0 điểm phần cá nhân liên quan.)*

## Mình dùng AI thế nào để làm phần đó
*(Nhắc gì, AI làm được gì, chỗ nào mình phải tự sửa lại vì AI làm sai.)*

## Một bài học từ case fail của chính nhóm
*(Lấy từ một case cụ thể — ví dụ một case trong `eval/run-0N.md` không đạt,
hoặc một feedback trong `validation/feedback-log.md`. Không viết bài học chung chung.)*
```

---

## Câu hỏi cả nhóm phải trả lời được trước CP6

*(guide §5.2 — TA và giám khảo hỏi ngẫu nhiên)*

1. **Augment hay automate — vì sao?** → `conditional`; lý do theo cost-of-error nằm ở `spec.md` §4.
2. **Failure nguy hiểm nhất là gì?** → bỏ sót một tin đổi phòng/huỷ buổi. Hậu quả không sửa được, và 7/11 người khảo sát đã từng dính.
3. **Phần bạn làm là gì, nó hoạt động thế nào?**
4. **Vì sao guard nằm trong code chứ không nằm trong prompt?** → prompt có thể bị thuyết phục bởi một tin nhắn viết chắc nịch; hàm kiểm `vai` và kiểm chuỗi con thì không.
5. **Vì sao quality bar có hai điều kiện cứng chứ không chỉ một con số %?** → `eval/rubric-cham.md`.
