PROMPT_CREATE_DATASET = """
Bạn là một hệ thống tạo dữ liệu huấn luyện cho mô hình phân loại câu hỏi theo lĩnh vực.

Cho trước một dictionary JSON có dạng: 
- Key: Tên lĩnh vực
- Value: Nội dung một câu hỏi thuộc lĩnh vực đó

Yêu cầu:
Từ câu hỏi đã cho, bạn hãy tạo ra câu hỏi mới, có tình huống thực tế giả định liên quan mật thiết đến nội dung câu hỏi đã cho, sao cho câu hỏi mới vẫn thuộc cùng lĩnh vực với câu hỏi ban đầu.
Hãy đảm bảo rằng câu hỏi mới:
1. Vẫn giữ nguyên lĩnh vực của câu hỏi gốc.
2. Có tình huống thực tế giả định mang tính thực tiễn cao.
3. Độ dài câu hỏi mới ít nhất 50 từ.
4. Làm nhiễu câu hỏi bằng cách thay đổi cấu trúc câu, sử dụng từ đồng nghĩa, và thêm các chi tiết phụ trợ liên quan đến tình huống thực tế.
5. Hạn chế dùng các từ liên quan trực tiếp đến lĩnh vực trong câu hỏi mới để tránh lộ đáp án.
6: Đảm bảo văn phong chuyên nghiệp và phù hợp với ngữ cảnh pháp lý.

Đầu ra của bạn chỉ là câu hỏi mới, KHÔNG thêm bất kỳ chú thích hay giải thích nào khác.

*Ví dụ đầu ra*: 
Input: ```json
{
    "tien-te-ngan-hang": "Dịch vụ cho thuê két an toàn của tổ chức tín dụng là gì?"
}
```
Output: "Ông A muốn bảo vệ tài sản quý giá của mình tại nhà riêng. Ông ta đang cân nhắc việc sử dụng dịch vụ cho thuê két an toàn từ một tổ chức tín dụng uy tín. Vậy, ông A cần hiểu rõ những quy định và lợi ích liên quan đến dịch vụ cho thuê két an toàn này là gì?"
"""

EXAMPLE = """
Nhiệm vụ của bạn là đọc câu hỏi sau và cho biết nó thuộc lĩnh vực nào, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chọn đáp án chứa đúng lĩnh vực của câu hỏi. Phải sử dụng tiếng Việt.
Chỉ đưa ra kết quả, không cần giải thích. Không lặp lại câu hỏi.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.
KHÔNG lặp lại câu hỏi.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là đọc câu hỏi sau và cho biết nó thuộc lĩnh vực nào, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chọn đáp án chứa đúng lĩnh vực của câu hỏi. 
Chỉ đưa ra kết quả, không cần giải thích.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi sau và cho biết nó thuộc lĩnh vực nào, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Anh B thường xuyên tổ chức hát karaoke di động và sử dụng loa kẹo kéo để phục vụ cho hoạt động giải trí cá nhân tại nhà. Gần đây, nhà anh nhận được phản ánh từ những người xung quanh vì âm lượng quá lớn gây ảnh hưởng đến sinh hoạt hàng ngày. Trong trường hợp này, nếu anh B tiếp tục duy trì hoạt động như vậy vào năm 2025, thì những quy định hiện hành có thể dẫn đến hình thức xử phạt nào không?
Đáp án: A. Dịch vụ pháp lý B. Bộ máy hành chính C. Chứng khoán D. Tiền tệ ngân hàng E. Vi phạm hành chính F. Lĩnh vực khác
Đáp án đúng: E
"""

EXAMPLE_EN = """
Instruction: “Read the following question and determine which field it belongs to. Only choose the answer, and do not provide any explanation.”
Question: “What are the guidelines in Official Dispatch No. 8935/BNV-CTTN&BĐG 2025 regarding the Action Month for Gender Equality and Prevention of Gender-Based Violence in 2025?”
Answer: A. Business B. Securities C. Civil Rights D. Legal Services
Ground truth: C
"""
