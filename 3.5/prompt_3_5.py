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
Nhiệm vụ của bạn là đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D
"""

EXAMPLE_REASONING = """
Nhiệm vụ của bạn là đọc câu hỏi trắc nghiệm pháp luật tiếng Việt và chọn đáp án đúng (A, B, C hoặc D). Để trả lời được câu hỏi, bạn phải suy nghĩ và đưa ra lập luận cho câu trả lời.

***ĐỊNH DẠNG CỦA OUTPUT***
1. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
- hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
- Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho ANSWER
- chỉ đưa ra một hoặc nhiều ký tự trong tập {A, B, C, D} và viết vào giữa 2 thẻ <output> và </output>
- KHÔNG được kèm theo bất kỳ từ ngữ, ký tự hoặc giải thích nào khác ở phần này.
- KHÔNG được viết câu kiểu “Đáp án là A”.
- KHÔNG được viết lại câu hỏi.

**YÊU CẦU TUÂN THỦ NGHIÊM NGẶT**:
- Nội dung thinking và câu trả lời phải được viết trong các thẻ tương ứng, không được viết bên ngoài.
- Không được đổi tên thẻ hoặc thêm thẻ mới.
- Không được dùng ký tự khác ngoài A/B/C/D bên trong 2 thẻ <output> và </output>.
- Định dạng phải chính xác tuyệt đối.

Ví dụ đúng:
<think>Phân tích nội bộ...</think>
<output>A</output>

Ví dụ sai:
Đáp án là A
<output>A – tôi chọn đáp án này</output>
A. Đây là đáp án đúng vì...
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
Câu hỏi: Theo quy định, án lệ được hiểu như thế nào?
Câu hỏi: Do uống rượu say nên tôi và K có xảy ra xô xát vì tranh cãi nhau về việc quan điểm của bọn trẻ con thời nay. Vì có  hơi men nên K có cầm gậy đánh tôi nhưng không đánh được. K rất tức giận nên ngay sau đó K gọi bạn đến để đập phá quán của tôi cho bõ tức. Xin hỏi theo quy định của pháp luật mức xử phạt cho hành vi của K là bao nhiêu?
Đáp án: "A. Hành vi gọi bạn đến để đạp phá quán là hành vi lôi kéo người khác gây rối, làm mất trật tự công cộng, mức phạt từ 2.000.000 - 3.000.000 đồng.\nB. K cầm gậy đánh người là hành vi xâm hại đến sưc khỏe người khác, mức phạt từ 2.000.000 - 3.000.000 đồng.\nC. Cả hai hành vi đều bị xử phạt theo mức 2.000.000 – 3.000.000 đồng.\nD. Không xử phạt hành vi cầm gậy đánh người vì chưa gây thương tích, chỉ hành vi thuê người quấy phá cửa hàng mới bị phạt; mức từ 5.000.000 – 7.000.000 đồng."
Đáp án đúng: "A"}
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

