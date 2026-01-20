PROMPT_CREATE_DATASET = """
"""

EXAMPLE = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRẢ LỜI bằng MỘT hoặc NHIỀU CHỮ CÁI (A, B, C, hoặc D) cách nhau bằng dấu phẩy nếu có nhiều đáp án đúng.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: [A, B]
Ví dụ sai: Đáp án là [A, B]
Ví dụ sai: A. Đây là đáp án đúng vì..., B. Đây là đáp án đúng vì...
"""

EXAMPLE_REASONING = """
Nhiệm vụ của bạn là đọc câu hỏi trắc nghiệm pháp luật tiếng Việt và chọn 1 hoặc nhiều đáp án đúng trong 4 đáp án A/B/C/D. 
Để trả lời được câu hỏi, bạn phải suy nghĩ và đưa ra lập luận cho câu trả lời.

***ĐỊNH DẠNG CỦA OUTPUT***
1. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. 
Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho ANSWER
- Bạn chỉ được phép đưa ra 1 hoặc nhiều hơn 1 kí tự từ 4 kí tự A, B, C và D.
- Các phương án được viết dưới dạng list. Ví dụ: ["A"], ["C", "D"].
- List không được gồm các phần tử không phải A/B/C/D.
- yêu cầu viết câu trả lời vào giữa 2 thẻ <output> và </output>
- KHÔNG được trả ra tên thực thể
- KHÔNG được trả ra nhãn phân loại (ví dụ: legal_query, document_retrieval, v.v.)
- KHÔNG được trả ra nội dung đáp án
- KHÔNG được viết câu kiểu “Đáp án là A”.
- KHÔNG được viết lại câu hỏi.
- Bắt buộc phải chọn đáp án nếu không chọn được cái nào. Không in nội dung của đáp án.
- Phải in ra chữ cái đại diện cho phương án.

**YÊU CẦU TUÂN THỦ NGHIÊM NGẶT**:
- Nội dung thinking và câu trả lời phải được viết trong các thẻ tương ứng, không được viết bên ngoài.
- Câu trả lời chỉ được phép là list các chữ cái A, B, C, D. Nếu output chứa bất kỳ chuỗi nào khác ngoài A/B/C/D → CÂU TRẢ LỜI BỊ COI LÀ SAI
- Không được đổi tên thẻ hoặc thêm thẻ mới.
- Định dạng phải chính xác tuyệt đối.

🚫 TUYỆT ĐỐI KHÔNG:
- KHÔNG được trả ra tên thực thể
- KHÔNG được trả ra nhãn phân loại (ví dụ: legal_query, document_retrieval, v.v.)
- KHÔNG được trả ra nội dung đáp án
- KHÔNG được tạo phương án mới
- KHÔNG được suy đoán loại câu hỏi
- KHÔNG được viết chữ ngoài A/B/C/D

⚠️ Nếu output chứa bất kỳ chuỗi nào khác ngoài A/B/C/D → CÂU TRẢ LỜI BỊ COI LÀ SAI.

Ví dụ đúng:
<think>Phân tích nội bộ...</think>
<output>["C", "D"]</output>

Ví dụ sai:
Đáp án là C và D
<output>["C", "D"] – tôi chọn đáp án này</output>
C và D. Đây là đáp án đúng vì...

Ví dụ sai:
<think>
Phân tích quy định tại điều luật cho thấy...
</think>
<output>["legal_query", "general"]</output>
"""

EXAMPLE_FEWSHOT = """
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRẢ LỜI bằng MỘT hoặc NHIỀU CHỮ CÁI (A, B, C, hoặc D) cách nhau bằng dấu phẩy nếu có nhiều đáp án đúng.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: [A, B]
Ví dụ sai: Đáp án là [A, B]
Ví dụ sai: A. Đây là đáp án đúng vì..., B. Đây là đáp án đúng vì...

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc query sau và xác định đúng intent của câu hỏi đó. Chỉ cần chọn đáp án và không cần giải thích gì thêm. Danh sách các intent: \n- chitchat: Câu hỏi không liên quan đến pháp luật (ví dụ chào hỏi, cảm ơn, off-topic)\n- comparative_analysis: So sánh nội dung giữa hai văn bản, điều khoản, nội dung, ...\n- document_relationship: Câu hỏi về mối quan hệ giữa các văn bản. ví dụ về sửa đổi, bổ sung - hướng dẫn - dẫn chiếu - căn cứ\n- document_retrieval:  Truy xuất toàn văn bản pháp luật\n- external_analysis: Tác động kinh tế, xã hội, xu hướng thay đổi, lịch sử, tác động, ảnh hưởng, xu hướng.\n- general: Câu hỏi tổng quát, có nội dung liên quan đến pháp luật, chưa thuộc intent nào cụ thể\n- legal_query: Tìm và trả lời từ nội dung cụ thể của điều / khoản / mục / điểm cụ thể\n- stats_summary: Thống kê số lượng văn bản/quy định.
Câu hỏi: Hãy xem kỹ mục 2 từ điều 20 đặc biệt mục 3 từ điều 23 về hỗ trợ bằng voucher, cho tôi nhận xét cần góp ý gì cho dự thảo này dưới góc độ một doanh nghiệp công nghệ thông tin đang đầu tư phát triển sản phẩm về ai 
Đáp án: A. legal_query B. comparative_analysis C. stats_summary D. external_analysis, 
Đáp án đúng: ["A", "D"]
"""
