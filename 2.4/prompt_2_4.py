# Phai luu lai id cua ban an de tien trong viec kiem tra

PROMPT_CREATE_DATASET = """
Bạn được cung cấp 2 phần trong một bản án của Tòa án Việt Nam: 
(1) Nội dung vụ án và (2) Nhận định của tòa án.

## NHIỆM VỤ
Hãy tạo **hai câu hỏi Đúng/Sai** dựa trên bản án theo hướng dẫn sau:

### Bước 1. Chọn dữ kiện
- Chỉ sử dụng thông tin trong hai phần: **Nội dung vụ án** và **Nhận định của tòa án**.
- Tập trung vào những tình tiết có **liên quan trực tiếp đến lập luận và đánh giá của Tòa án**.
- Không được thêm dữ kiện hoặc kết luận ngoài bản án.

### Bước 2. Tạo câu hỏi
Mỗi câu hỏi phải có cấu trúc JSON như sau:

{
  "description": "Viết một đoạn tóm tắt ngắn, chỉ gồm các tình tiết trong Nội dung vụ án có liên quan trực tiếp đến nhận định của Tòa án. Không thêm thông tin ngoài bản án. Không phân tích pháp lý.",
  "court_judgement": "Một đoạn mô tả ngắn gọn, đầy đủ về Nhận định của Tòa án. Có thể là nhận định đúng (phản ánh trung thực nội dung bản án) hoặc nhận định sai (bị thay đổi chi tiết, hoặc hiểu sai ý của Tòa).",
  "ground_truth": "Đúng hoặc Sai, biểu thị xem đoạn court_judgement ở trên có phản ánh chính xác nhận định thật của Tòa án hay không."
}

### YÊU CẦU
- Tạo **chính xác 2 câu hỏi Đúng/Sai** cho mỗi bản án.
- Ít nhất 1 câu hỏi có đáp án **“Đúng”**, và 1 câu hỏi có đáp án **“Sai”**.
- Phần **description** chỉ tóm tắt các tình tiết thực tế trong phần **Nội dung vụ án**, không chứa nhận xét hoặc đánh giá pháp lý.
- Phần **court_judgement** phải được viết ngắn gọn, đầy đủ , bám sát cách diễn đạt trong phần **Nhận định của Tòa**, nhưng:
  - Nếu là “Sai”: thay đổi chi tiết nhỏ (về thời gian, hành vi, hậu quả, hoặc trách nhiệm pháp lý).
  - Nếu là “Đúng”: diễn đạt lại chính xác, có thể paraphrase, nhưng không làm sai nội dung.

### RÀNG BUỘC ĐẦU RA
- **Chỉ trả về một mảng JSON hợp lệ duy nhất** (bắt đầu bằng `[` và kết thúc bằng `]`).
- Mảng này phải chứa **chính xác 2 object JSON**, mỗi object có 3 trường: `"description"`, `"court_judgement"`, `"ground_truth"`.
- Không in thêm văn bản, lời giải thích, hoặc markdown (` ``` `).
- Đầu ra phải có thể parse trực tiếp bằng `json.loads()` trong Python mà không cần xử lý chuỗi.

### VÍ DỤ OUTPUT CHUẨN

[
  {
    "description": "Ngày 10/3/2022, bà Nguyễn Thị B cho ông Trần Văn A vay 300 triệu đồng để mở cửa hàng buôn bán vật liệu xây dựng. Hai bên lập giấy vay viết tay, có chữ ký của ông A, thời hạn trả nợ là 6 tháng kể từ ngày vay. Sau nhiều lần được nhắc nhở, ông A vẫn chưa trả số tiền trên.",
    "court_judgement": "Tòa án nhận định rằng việc vay tiền giữa bà B và ông A là có thật, có đủ căn cứ chứng minh. Do ông A không thực hiện nghĩa vụ trả nợ đúng hạn, Tòa buộc ông A phải hoàn trả toàn bộ số tiền 300 triệu đồng cùng lãi suất theo quy định của pháp luật.",
    "ground_truth": "Đúng"
  },
  {
    "description": "Ngày 10/3/2022, bà Nguyễn Thị B cho ông Trần Văn A vay 300 triệu đồng để mở cửa hàng buôn bán vật liệu xây dựng. Hai bên lập giấy vay viết tay, có chữ ký của ông A, thời hạn trả nợ là 6 tháng kể từ ngày vay. Sau nhiều lần được nhắc nhở, ông A vẫn chưa trả số tiền trên.",
    "court_judgement": "Tòa án nhận định rằng việc vay tiền giữa bà B và ông A không có đủ căn cứ chứng minh, do giấy vay không có chữ ký của người làm chứng, nên bác toàn bộ yêu cầu khởi kiện của bà B.",
    "ground_truth": "Sai"
  }
]
"""

EXAMPLE = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và tóm tắt về nhận định của tòa án liên quan đến bản án đó.
Nhiệm vụ của bạn là xác định xem nhận định của tòa án có phản ánh chính xác nội dung bản án hay không.
Chỉ đưa ra đáp án "Đúng" hoặc "Sai". Không giải thích gì thêm. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
"""

EXAMPLE_REASONING = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và tóm tắt về nhận định của tòa án liên quan đến bản án đó.
Nhiệm vụ của bạn là hãy xác định xem nhận định của tòa án có phản ánh chính xác nội dung bản án hay không.
Bạn cần suy nghĩ và lập luận để trả lời câu hỏi.

Bạn phải thực hiện ĐÚNG các bước sau:

***ĐỊNH DẠNG CỦA OUTPUT***
1. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho ANSWER
chỉ đưa ra Đúng hoặc Sai và viết vào giữa 2 thẻ <output> và </output>
KHÔNG được kèm theo bất kỳ từ ngữ, ký tự hoặc giải thích nào khác ở phần này.
KHÔNG được viết câu kiểu như "Nhận định trên đúng".
KHÔNG được viết lại câu hỏi.

YÊU CẦU TUÂN THỦ NGHIÊM NGẶT:
- Không được thêm văn bản ngoài hai thẻ <think> và <output>.
- Không được đổi tên thẻ hoặc thêm thẻ mới.
- Không được dùng ký tự khác ngoài Đúng/Sai bên trong thẻ <output>.
- Định dạng phải chính xác tuyệt đối.

Ví dụ đúng:
<think>Phân tích nội bộ...</think>
<output>Đúng</output>

Ví dụ sai:
Đáp án là Đúng
<output>Đúng – tôi chọn đáp án này</output>
Nhận định trên Đúng vì...
"""

EXAMPLE_FEWSHOT = """
Bạn được cung cấp nội dung tóm tắt một bản án của Tòa án Việt Nam và tóm tắt về nhận định của tòa án liên quan đến bản án đó.
Nhiệm vụ của bạn là xác định xem nhận định của tòa án có phản ánh chính xác nội dung bản án hay không.
Chỉ đưa ra đáp án "Đúng" hoặc "Sai". Không giải thích gì thêm. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Từ nội dung bản án được cho, xác định nhận định của tòa án dưới đây là đúng hay sai. Chỉ cần trả lời Đúng hoặc Sai, không cần giải thích gì thêm.
Tình huống: Chị Lò Thị V và anh Cà Văn L kết hôn, có hai con chung, nhưng do mâu thuẫn và anh L hiện đang chịu án phạt tù, chị V yêu cầu ly hôn và giành quyền nuôi con. Chị không yêu cầu anh L cấp dưỡng nuôi con và không yêu cầu chia tài sản hay giải quyết nợ. Anh L cũng nhất trí ly hôn nhưng đề nghị giao quyền nuôi con cho ông bà nội. 
Nhận định của toàn án: "Tòa án quyết định cho chị Lò Thị V được ly hôn anh Cà Văn L và giao quyền nuôi hai con cho chị V, miễn anh Cà Văn L nghĩa vụ cấp dưỡng do chị V không yêu cầu.", 
Đáp án: Đúng
"""