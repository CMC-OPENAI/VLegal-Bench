PROMPT_CREATE_DATASET = """
Bạn là một chuyên gia xây dựng ngân hàng câu hỏi trắc nghiệm pháp luật Việt Nam.
Dưới đây là thông tin dạng lược đồ về một cặp văn bản pháp luật Việt Nam, 
bao gồm thông tin của văn bản ban hành trước, thông tin của văn bản ban hành sau và mối quan hệ của chúng.

Hãy tạo ra một câu hỏi trắc nghiệm duy nhất với 4 lựa chọn dựa trên thông tin này. 
**Yêu cầu**:
- Nội dung câu hỏi: liên quan đến mối quan hệ giữa văn bản trước và văn bản sau (ví dụ: văn bản sau sửa đổi, bổ sung văn bản trước; văn bản sau thay thế văn bản trước; văn bản sau được ban hành để thi hành văn bản trước; v.v.)
- Câu hỏi phải có:
  • Instruction: “Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.”  
  • Question: [Một câu hỏi tự nhiên, rõ ràng về mối quan hệ giữa hai văn bản pháp luật. Văn bản được đề cập trong câu hỏi phải nêu rõ số liệu.]
  • Answers: [Đáp án là số hiệu của các văn bản quy phạm pháp luật khác nhau.Tạo 4 phương án A, B, C, D - gồm 1 đáp án đúng và 3 đáp án sai.]
  • Ground truth: chỉ ra đáp án đúng bằng chữ cái A, B, C hoặc D.
- Câu hỏi viết bằng tiếng Việt, rõ ràng, mang phong cách chính thống như trong các đề thi công chức.
- Tận dụng tối đa thông tin trong thông tin lược đồ được cung cấp:
• Thông tin văn bản ban hành trước: loai_van_ban, so_hieu, trich_yeu, ngay_ban_hanh, ngay_co_hieu_luc.
• Thông tin văn bản ban hành sau: so_hieu, loai_van_ban, ngay_ban_hanh, ngay_hieu_luc, tinh_trang.
- Đảm bảo rằng các lựa chọn đáp án là các văn bản pháp luật hợp lệ và khác nhau.
- Đa dạng mối quan hệ chủ động và bị động giữa hai văn bản trong câu hỏi.

Ví dụ đầu ra mong muốn: 
```json
{
  "Instruction": "Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.",
  "Question": "Luật 90/2025/QH15 sửa đổi, bổ sung những văn bản quy phạm pháp luật nào?",
  "Answers": {
    "A": "Luật 48/2024/QH15",
    "B": "Luật 72/2025/QH15",
    "C": "Luật 56/2024/QH15",
    "D": "Luật 09/VBHN-VPQH"
    }
  },
  "Ground truth": "C"
}
```
"""
EXAMPLE = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Question: Thông tư 11/2025/TT-BTP có mối quan hệ như thế nào với Văn bản hợp nhất 5796/VBHN-BTP?
Answers: {"A": "Thông tư là cơ sở để ban hành Văn bản hợp nhất 5796/VBHN-BTP", "B": "Thông tư là văn bản hợp nhất từ Văn bản hợp nhất 5796/VBHN-BTP", "C": "Thông tư sửa đổi Văn bản hợp nhất 5796/VBHN-BTP", "D": "Thông tư hợp nhất các nội dung của Văn bản hợp nhất 5796/VBHN-BTP"}
Ground truth: C
"""