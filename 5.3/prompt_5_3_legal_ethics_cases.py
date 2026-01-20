EXAMPLE = """
Nhiệm vụ của bạn là đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

****CHỈ TRẢ VỀ CHỮ CÁI HOẶC A, HOẶC B, HOẶC C, HOẶC D*****

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi trắc nghiệm sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Trong một lần tham gia giao thông , Q lạng lách gây va quẹt với H, đã không xin lỗi Q\ncòn hung hăng nhào đến đánh H. Do H có võ, nên H đã đá Q một cú vào chân làm gãy xương chân, tỷ lệ thương tật 18% (theo kết quả giám định). Do vậy, H bị khởi tố về tội \"Cố ý gây thương tích\" nên H đến nhờ luật sư A bào chữa cho mình. Luật sư A hứa với H sẽ bào chữa cho H không phải ở tù với thù lao là 100 triệu đồng. Sau đó, Tòa án nhân dân huyện T đã xử H mức án 2 năm tù nhưng cho hưởng án treo,\nvề tội: \" Cố ý gây thương tích\" . Tuy nhiên, bản án này bị Viện Kiểm sát nhân dân\nhuyện T kháng nghị, Tòa án cấp tỉnh đã xét xử phúc thẩm, tuyên phạt H mức án 2 năm tù giam về tội: \"Cố ý gây thương tích\". Gia đình H đến gặp luật sư A đòi lại tiền. Luật sư A không trả lại tiền và nói: \" Luật sư đã thực hiện đúng hợp đồng và không trả lại tiền.\". Anh (chị) có ý kiến gì về thái độ ứng xử của luật sư A? Phân tích rõ\ntại sao?"
Đáp án: "A. Luật sư A đã hứa hẹn kết quả, không tận tâm và không ứng xử phù hợp khi có tranh chấp, vi phạm Khoản 9.8 Điều 9, Quy tắc 2, Quy tắc 5 và Quy tắc 12.3.\nB. Luật sư A đã tư vấn chưa đầy đủ, thiếu giải thích rủi ro và xử lý tranh chấp chưa hợp lý, chủ yếu liên quan đến Quy tắc 2 và Quy tắc 12.3 nhưng không vi phạm Quy tắc 5.\nC. Luật sư A chỉ không giải thích rõ khả năng thay đổi bản án và đã phản hồi chưa mềm mỏng khi xảy ra tranh chấp, có dấu hiệu liên quan Quy tắc 12.3 nhưng không thuộc Khoản 9.8 Điều 9.\nD. Luật sư A vẫn thực hiện công việc nhưng thiếu linh hoạt trong giao tiếp và chưa trao đổi trước về kết quả dự kiến, chủ yếu liên quan Quy tắc 5 và Quy tắc 12.3 nhưng không phải vi phạm Quy tắc 2."
Đáp án đúng: A
"""