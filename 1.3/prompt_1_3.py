PROMPT_PARAPHRASE = """
Bạn là một chuyên gia tạo câu hỏi pháp lý.
Bạn sẽ được cung cấp dữ liệu gồm 1 câu hỏi, 4 câu trả lời trắc nghiệm (A, B, C, D), và đáp án đúng.
Nhiệm vụ của bạn là viết lại câu hỏi và các câu trả lời trắc nghiệm sao cho khác biệt về mặt ngôn ngữ so với dữ liệu gốc, nhưng vẫn giữ nguyên ý nghĩa và đảm bảo rằng đáp án đúng vẫn là đáp án đúng trong câu hỏi mới.
Hãy chắc chắn rằng câu hỏi và các câu trả lời trắc nghiệm mới không giống với câu hỏi và các câu trả lời trắc nghiệm gốc về mặt từ ngữ và cấu trúc câu.
Hãy đảm bảo câu trả lời đúng phải khó phân biệt với các câu trả lời sai để tăng tính thử thách.
Chỉ trả lời bằng định dạng JSON như sau, không thêm bất kỳ lời giải thích nào:
{
  "Paraphrased Question": "<Câu hỏi được viết lại>",
  "Paraphrased Answers": {
    "A": "<Câu trả lời A được viết lại>",
    "B": "<Câu trả lời B được viết lại>",
    "C": "<Câu trả lời C được viết lại>",
    "D": "<Câu trả lời D được viết lại>"
  },
  "Ground Truth": "<Đáp án đúng (A, B, C, hoặc D)>"
}
LƯU Ý QUAN TRỌNG: Phản hồi của bạn PHẢI LÀ MỘT ĐỐI TƯỢNG JSON HỢP LỆ THEO CẤU TRÚC Ở TRÊN. KHÔNG ĐƯỢC THÊM BẤT KỲ LỜI GIẢI THÍCH NÀO KHÁC. KHÔNG thay ĐỔI CẤU TRÚC JSON.
"""
EXAMPLE = """
Nhiệm vụ của bạn là đọc câu hỏi sau và xác định khái niệm được hỏi trong câu hỏi là gì, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token </think> hoặc ***Giải thích***. Không lặp lại câu hỏi

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác. Không lặp lại câu hỏi

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là đọc câu hỏi sau và xác định khái niệm được hỏi trong câu hỏi là gì, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Theo quy định, Giao dịch dân sự được hiểu là gì?
Đáp án: {"A": "A. Giao dịch dân sự là giao dịch pháp lý đơn phương làm phát sinh, thay đổi hoặc chấm dứt quyền, nghĩa vụ dân sự.", "B": "B. Giao dịch dân sự là hợp đồng hoặc hành vi pháp lý đơn phương làm phát sinh, thay đổi hoặc chấm dứt quyền, nghĩa vụ dân sự.", "C": "C. Giao dịch dân sự là hợp đồng hoặc hành vi pháp lý đơn phương làm phát sinh, thay đổi quyền, nghĩa vụ dân sự.", "D": "D. Giao dịch dân sự là hợp đồng hoặc hành vi pháp lý làm phát sinh, thay đổi hoặc chấm dứt quyền, nghĩa vụ dân sự."}
Đáp án đúng: B
"""

EXAMPLE_EN = """
• Instruction: “Read the following question and choose the correct answer. Only select the answer; no explanation is needed.”
• Question: “According to regulations, what is the definition of a legal precedent (án lệ)?”
• Answers:
A. A legal precedent refers to the reasoning and judgments in a court’s legally effective judgments or decisions on a specific case, which are selected by the Council of Judges of the Supreme People’s Court and published by the Chief Justice of the Supreme People’s Court as precedents for other courts to study and apply in adjudication.
B. A legal precedent refers to the reasoning and judgments in a court’s legally effective judgments or decisions, which are selected by the Supreme People’s Procuracy and published by the Procurator General for judicial agencies to apply in adjudication.
C. A legal precedent refers to the reasoning and judgments in a court’s legally effective judgments or decisions on a specific case, which are selected by the National Assembly and published by the Chairperson of the National Assembly for courts to refer to during adjudication.
• Ground truth: A
"""

