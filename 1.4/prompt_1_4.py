PROMPT_CREATE_DATASET = """
Bạn là một chuyên gia xây dựng ngân hàng câu hỏi trắc nghiệm pháp luật Việt Nam.  
Dưới đây là dữ liệu về một điều luật, bao gồm vị trí, tiêu đề, nội dung, và các thông tin metadata khác.  

Hãy tạo ra **một câu hỏi trắc nghiệm duy nhất** (hoặc nhiều câu nếu được yêu cầu) theo cấu trúc sau:  

• Instruction: “Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.”  
• Question: [viết một câu hỏi tự nhiên, rõ ràng, có thể hỏi về nội dung, phạm vi điều chỉnh, đối tượng áp dụng, hiệu lực, cơ quan ban hành, v.v.]  
• Answers: [Tạo 4 phương án A, B, C, D — chỉ 1 đúng, 3 sai nhưng hợp lý]  
• Ground truth: [ghi chữ cái của đáp án đúng]  

Nội dung của câu hỏi: 
Câu hỏi có thể hỏi về các khía cạnh sau tùy theo thông tin có trong dữ liệu:
- Nội dung quy định chính trong điều luật
- Phạm vi điều chỉnh của điều luật
- Đối tượng áp dụng của điều luật
- Hiệu lực của điều luật
- Cơ quan ban hành điều luật

Yêu cầu khi tạo câu hỏi:  
1. Tận dụng tối đa các thông tin trong các trường `position`, `title`, `raw_content`, `loai_van_ban`, `so_hieu`, `co_quan_ban_hanh`, `ngay_co_hieu_luc`.  
2. Nếu `position` có chứa “Điều”, “Khoản”, “Điểm” thì hãy đưa chúng vào câu hỏi.  
3. Câu hỏi phải mang tính khái quát hoặc nhận biết nội dung quy định chính.  
4. Đáp án sai phải cùng ngữ cảnh, tránh quá lộ liễu.  
5. Ngôn ngữ: tiếng Việt, rõ ràng, mang phong cách chính thống như trong các đề thi công chức.  

Hãy xuất kết quả theo đúng định dạng ví dụ sau:  

```json
{
  "Instruction": “Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.”,
  "Question": “Điều 1 Luật Đất đai số 31/2024/QH15 quy định về nội dung nào sau đây?”,
  "Answers": {
    "A": “Về quyền và nghĩa vụ của người nước ngoài khi sử dụng đất tại Việt Nam.”,
    "B": “Về phạm vi điều chỉnh của Luật, bao gồm chế độ sở hữu, quản lý và sử dụng đất đai.”,
    "C": “Về trình tự, thủ tục cấp Giấy chứng nhận quyền sử dụng đất.”,
    "D": “Về cơ quan nhà nước có thẩm quyền thu hồi đất và bồi thường.”
  },
  "Ground truth": "B"
```
"""

EXAMPLE = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không lặp lại câu hỏi

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác. Không lặp lại câu hỏi

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi trắc nghiệm sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Điểm a Khoản 1 Điều 1 Nghị định số 113/2007/NĐ-CP quy định về nội dung nào sau đây?
Đáp án: {'A': 'Quy định về quyền sở hữu và quản lý đê điều.', 'B': 'Hướng dẫn về việc phân loại và phân cấp đê theo Điều 4 Luật Đê điều.', 'C': 'Quy định về các hình thức xử phạt vi phạm liên quan đến đê điều.', 'D': 'Hướng dẫn về việc bảo vệ đê điều trong mùa lũ.'}
Đáp án đúng: B
"""



EXAMPLE_EN = """
• Instruction: “Read the following question and choose the correct answer. Only select the answer; no explanation is needed.”
• Question: “According to Clause 1, Article 2 of the 2015 Civil Code, what is stipulated regarding the scope of application and the effectiveness of the Civil Procedure Code?”
• Answers:
A. It applies to all civil procedure activities in certain special localities.
B. It applies to all civil procedure activities within the mainland territory of the Socialist Republic of Vietnam.
C. It applies to certain civil procedure activities within the territory of the Socialist Republic of Vietnam as specifically provided in Clause 2 of this Code.
D. It applies to all civil procedure activities within the territory of the Socialist Republic of Vietnam, including the mainland, islands, sea areas, and airspace.
• Ground truth: B
"""
