
EXAMPLE = """
Nhiệm vụ của bạn là đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

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
Instruction: Đọc câu hỏi trắc nghiệm sau và chọn một hoặc nhiều đáp án đúng, chỉ cần chọn đáp án mà không cần giải thích gì thêm
Câu hỏi: "Trong tuần đầu tiên của năm học mới, T là lớp trưởng được cô chủ nhiệm giao nhiệm vụ thu thập thông tin cá nhân của các bạn trong lớp để lập sổ liên lạc điện tử. T lập một mẫu khảo sát online yêu cầu các thông tin cơ bản như Họ tên, Ngày sinh, Địa chỉ, Số điện thoại phụ huynh và Địa chỉ email cá nhân (cho việc nhận tài liệu học tập). T giải thích rõ ràng đây là yêu cầu của giáo viên chủ nhiệm và mục đích là để phục vụ công tác quản lý và liên lạc trong học tập. Tuy nhiên, khi gửi link khảo sát vào nhóm chat của lớp, một số bạn tỏ ra ngần ngại và băn khoăn về tính bảo mật của dữ liệu. Một thành viên trong lớp hỏi T: \"Lỡ thông tin cá nhân của tụi mình bị lộ ra ngoài thì sao?\". Hành vi nào là phản ánh đúng tình huống trên?"
Đáp án: "A: Lớp trưởng T được thu thập và sử dụng thông tin cá nhân của các bạn để phục vụ mục đích học tập nếu các bạn đồng ý cung cấp thông tin\nB: Nhà trường và giáo viên chủ nhiệm cần có trách nhiệm bảo vệ dữ liệu thông tin đã thu thập \nC: Người thu thập trực tiếp T mới là người chịu trách nhiệm chính và phải bồi thường nếu thông tin bị lộ\nD: Trách nhiệm bảo mật thuộc về các thành viên đã điền thông tin vì họ đã tự nguyện cung cấp, do đó họ phải chấp nhận rủi ro thông tin bị rò rỉ."
Đáp án đúng: A
"""