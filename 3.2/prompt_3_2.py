# Phai luu lai id cua ban an de tien trong viec kiem tra

PROMPT_CREATE_DATASET = """
Bạn được cung cấp 2 phần trong một bản án của Tòa án Việt Nam: 
(1) Nội dung vụ án và (2) Quyết định của Tòa án.

## NHIỆM VỤ
Hãy tạo **một câu hỏi trắc nghiệm** dựa trên bản án theo hướng dẫn sau:

### Bước 1. Chọn dữ kiện
- Chỉ sử dụng thông tin trong hai phần: **Nội dung vụ án** và **Quyết định của Tòa án**.

### Bước 2. Tạo câu hỏi
Cấu trúc câu hỏi như sau (trả về dưới dạng JSON):

{
  "description": "Viết một đoạn tóm tắt ngắn, chỉ gồm các tình tiết trong Nội dung vụ án có liên quan trực tiếp đến quyết định của Tòa án. Không thêm thông tin ngoài bản án. Không phân tích pháp lý.",
  "answers": {
    "A": "Đáp án A — một khả năng phán quyết của Tòa.",
    "B": "Đáp án B — một khả năng phán quyết của Tòa.",
    "C": "Đáp án C — một khả năng phán quyết của Tòa.",
    "D": "Đáp án D — một khả năng phán quyết của Tòa."
  },
  "ground_truth": "Ký hiệu A/B/C/D cho đáp án đúng, được paraphrase từ Quyết định thật của Tòa án."
}

### YÊU CẦU
- Chỉ có **1 câu hỏi duy nhất** được tạo ra cho mỗi bản án.
- Không sử dụng thông tin liên quan đến hành động/quyết định của tòa trong phần description.
- description cần là một đoạn tóm tắt ngắn gọn NHƯNG đầy đủ về các tình tiết liên quan đến quyết định của tòa án trong phần Nội dung vụ án.
- Đáp án đúng được paraphrase trung thực từ Quyết định thật của Tòa án.
- Ba đáp án còn lại phải **sai nhưng hợp lý**, có độ dài tương đương, và đều liên quan đến cùng chủ đề.
- Không thêm lời giải thích hoặc phân tích pháp lý.
- Không dùng nội dung từ phần “Nhận định của Tòa án”.

### GỢI Ý
Hãy đảm bảo format đầu ra JSON hợp lệ (có thể parse được bằng Python json.loads).
"""

EXAMPLE = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và 4 đáp án thể hiện quyết định của tòa án.
Nhiệm vụ của bạn là chọn đáp án đúng dựa trên nội dung bản án.
Chỉ đưa ra ký hiệu của đáp án đúng (A, B, C hoặc D). Không giải thích gì thêm. 
Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
"""

EXAMPLE_REASONING = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và 4 đáp án thể hiện quyết định của tòa án.
Nhiệm vụ của bạn là chọn đáp án đúng dựa trên nội dung bản án.

Bạn phải thực hiện ĐÚNG HAI bước sau:

1. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

YÊU CẦU TUÂN THỦ NGHIÊM NGẶT:
Không được thêm văn bản ngoài hai thẻ <think> và <output>.
Không được đổi tên thẻ hoặc thêm thẻ mới.
Không được dùng ký tự khác ngoài A/B/C/D bên trong thẻ <output>.
Định dạng phải chính xác tuyệt đối.

Ví dụ đúng:
<think>Phân tích nội bộ...</think>
<output>A</output>

Ví dụ sai:
Đáp án là A
<output>A – tôi chọn đáp án này</output>
A. Đây là đáp án đúng vì...
"""

EXAMPLE_FEWSHOT = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và 4 đáp án thể hiện quyết định của tòa án.
Nhiệm vụ của bạn là chọn đáp án đúng dựa trên nội dung bản án.
Chỉ đưa ra ký hiệu của đáp án đúng (A, B, C hoặc D). Không giải thích gì thêm. 
Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

Dứới đây là một ví dụ để bạn tham khảo:
Instruction: Từ nội dung bản án được cho, chọn đáp án thể hiện đúng phán quyết của tòa án. Chỉ cần chọn đáp án và không cần giải thích gì thêm.
Tình huống: Chị Lò Thị V và anh Cà Văn L kết hôn ngày 05/12/2016. Họ có 2 con chung là Cà Thị Tiến và Cà Chí T. Do mâu thuẫn và anh L hiện đang chấp hành án, hai bên không còn tình cảm. Chị V đề nghị ly hôn và giữ quyền nuôi dưỡng con mà không yêu cầu cấp dưỡng từ anh L. Anh L yêu cầu giao quyền nuôi con cho ông bà nội. Không có nợ chung hay tài sản chung cần giải quyết.
Đáp án: "A: Tòa án quyết định cho chị Lò Thị V được ly hôn, giao quyền nuôi con cho chị V và miễn anh L cấp dưỡng.\nB: Tòa án quyết định cho ly hôn nhưng yêu cầu anh L cấp dưỡng hàng tháng cho con chung.\nC: Tòa án quyết định giao quyền nuôi con cho ông bà nội theo yêu cầu của anh L.\nD: Tòa án quyết định không đồng ý cho ly hôn và yêu cầu cả hai bên hòa giải."
Đáp án đúng: A 
"""
