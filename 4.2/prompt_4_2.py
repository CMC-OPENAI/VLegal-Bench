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
Nhiệm vụ của bạn là trích xuất các yếu tố dựa trên quy tắc IRAC để trả lời câu hỏi tình huống dưới đây.  
Bạn bắt buộc phải tuân thủ format chuẩn IRAC và không được thêm phần thừa. Trả lời bằng tiếng Việt, không sinh ngôn ngữ khác.

Định nghĩa:
- Issue: Xác định câu hỏi pháp lý cốt lõi cần giải quyết từ tình huống thực tế.
- Rule: Nêu ra các quy định pháp luật, điều luật, hoặc nguyên tắc pháp lý có liên quan.
- Application: Áp dụng các quy định pháp luật vào các sự kiện cụ thể của vụ việc để phân tích.
- Conclusion: Đưa ra kết luận cuối cùng dựa trên quá trình phân tích. 

Ràng buộc:
- Không được bổ sung, suy diễn ngoài nội dung cho sẵn.
- Không thêm bất kỳ giải thích nào ngoài yêu cầu.
- Không được tạo thêm nhân vật hay diễn biến.
- Không được sử dụng các token thuộc về suy diễn như </think> hay ***GIẢI THÍCH***, **LÝ DO**
- Không được viện dẫn luật không xuất hiện trong dữ kiện (trừ khi yêu cầu).
- Phải tách 4 phần rõ ràng.
- CHỈ CÓ 1 IRAC trong 1 tình huống.
- Phải có đủ 4 yếu tố, không được để trống.

****QUAN TRỌNG****
Đầu ra phải có:
Issue: ...\n
Rule: ...\n
Application: ..\n 
Conclusion: ...
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
Instruction: Đọc câu hỏi trắc nghiệm sau và chọn đáp án đúng thể hiện quy trình IRAC để giải quyết vấn đề pháp lý, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Khi sinh ra, em A (10 tuổi) đã có vết bớt to màu đen che gần nửa khuôn mặt. Cô H không muốn nhận A vào lớp cô chủ nhiệm và đề xuất  Ban Giám hiệu nhà trường chuyển em A sang lớp khác. Hành vi của cô H có vi phạm pháp luật không?
Đáp án: {"A": "Rule: Khoản 8 Điều 6 Luật Trẻ em 2016 nghiêm cấm kỳ thị, phân biệt đối xử với trẻ em.\nApplication: Áp dụng khoản 8 Điều 6: việc cô H từ chối nhận A vì vết bớt là hành vi kỳ thị dựa trên đặc điểm cá nhân, vi phạm nghĩa vụ không phân biệt đối xử theo Điều 4 Luật Trẻ em 2016.\nConclusion: Hành vi của cô H vi phạm Luật Trẻ em 2016.", "B": "Rule: Điều 7 Luật Trẻ em 2016 về nguyên tắc bảo đảm môi trường giáo dục an toàn cho trẻ em.\nApplication: Áp dụng Điều 7: cô H muốn chuyển A đi lớp khác để “đảm bảo tâm lý tập thể”, nên không xem là phân biệt đối xử mà là biện pháp tổ chức lớp học.\nConclusion: Hành vi của cô H không vi phạm luật.", "C": "Rule: Điều 12 Luật Giáo dục 2019 về quyền bình đẳng của người học trong tiếp cận giáo dục.\nApplication: Áp dụng Điều 12 theo hướng mềm: cô H chỉ “sắp xếp lại lớp” chứ không từ chối quyền học tập, nên hành vi không cấu thành vi phạm quyền trẻ em.\nConclusion: Cô H không bị xem là vi phạm pháp luật.", "D": "Rule: Khoản 8 Điều 6 Luật Trẻ em 2016 cấm phân biệt đối xử theo dân tộc, giới tính.\nApplication: Áp dụng sai phạm vi Điều 6: vì việc từ chối nhận A không liên quan tới dân tộc hay giới tính nên không thuộc hành vi bị nghiêm cấm.\nConclusion: Cô H không vi phạm khoản 8 Điều 6."}
Đáp án đúng: A
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

