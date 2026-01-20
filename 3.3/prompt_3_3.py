PROMPT_CREATE_DATASET = """
Bạn là một chuyên gia soạn câu hỏi pháp luật. Nhận vào ba nguồn dữ liệu: Example Question, Example Answer, và Reference Source (tập hợp các văn bản luật: Điều, Khoản, Điểm). Hãy thực hiện theo các bước và đầu ra bắt buộc dưới đây.

## Nhiệm vụ
1. Đọc & hiểu
   - Đọc kỹ Example Question, Example Answer và toàn bộ các văn bản trong Reference Source.
   - Xác định những Điều/Khoản/Điểm trong Reference Source được Example Answer dựa vào (nếu có).

2. Tạo câu hỏi tình huống nâng cấp (Advanced Question)
   - Từ Example Question, nâng cấp thành một tình huống pháp lý mới đòi hỏi suy luận chéo giữa nhiều điều khoản trong Reference Source để trả lời đúng.
   - Câu hỏi phải cụ thể, rõ ràng về dữ kiện (ai, khi nào, ở đâu, xảy ra hành vi gì) và gợi ý rằng người trả lời cần đối chiếu ít nhất hai văn bản/điều khoản khác nhau trong Reference Source.
   - Ngôn ngữ: Tiếng Việt chuẩn, không dùng từ mơ hồ.

3. Soạn 4 phương án trắc nghiệm (Answer A – D)
   - Tạo 1 đáp án đúng (Ground Truth Answer). Ground Truth phải là kết luận hợp lý duy nhất dựa trên sự liên kết rõ ràng giữa các Điều/Khoản/Điểm trong Reference Source và phù hợp với Example Answer.
   - Phải ghi rõ trong phần giải thích của Ground Truth: liệt kê các Điều/Khoản/Điểm cụ thể đã sử dụng và mô tả ngắn gọn cách các văn bản này liên kết để dẫn tới kết luận.
   - Tạo 3 đáp án sai (paraphrase từ Ground Truth nhưng theo hướng trả lời sai). Sai vì thiếu điều kiện pháp lý, diễn giải sai, hoặc áp dụng chưa đầy đủ — không được bịa đặt điều luật.
   - Không thêm chi tiết pháp lý sai lệch nghiêm trọng hoặc tạo ra Điều/Khoản giả.

## Ràng buộc & Tiêu chí chất lượng
- Viết bằng Tiếng Việt chuẩn.
- 1 đáp án đúng duy nhất; 3 đáp án còn lại không quá dễ loại.
- Ground Truth có giải thích pháp lý rõ ràng (2–5 câu), trích dẫn Điều/Khoản/Điểm.
- Các phương án sai giữ ngôn ngữ gần giống đáp án đúng nhưng mắc lỗi lập luận tự nhiên.
- Mỗi phương án dài tối đa 2–3 câu.
- Không trích dẫn nguồn ngoài Reference Source.

## Định dạng đầu ra
```json 
{
    "Advanced Question": "<nội dung câu hỏi tình huống nâng cấp>",
    "Answers": {
    "A": "<phương án A>",
    "B": "<phương án B>",
    "C": "<phương án C>",
    "D": "<phương án D>"
  },
    "Ground Truth": "<ghi một trong 4 phương án A/B/C/D>",
    "Giải thích pháp lý": {
    "Liệt kê các Điều/Khoản/Điểm sử dụng": "<danh sách các Điều/Khoản/Điểm>",
    "Viết 2–5 câu giải thích lập luận pháp lý và cách các văn bản liên kết với nhau": "<nội dung giải thích>"
  }
}
```
## Ghi chú
- Không hỏi lại người dùng.
- Không tạo Điều/Khoản/Điểm giả.
- Nếu thiếu dữ kiện, suy luận hợp lý dựa trên Example Question/Answer và Reference Source.
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

EEXAMPLE_REASONING = """
Nhiệm vụ của bạn là đọc câu hỏi trắc nghiệm pháp luật tiếng Việt và chọn 1 đáp án đúng (A, B, C hoặc D). 
Để trả lời được câu hỏi, bạn phải suy nghĩ và đưa ra lập luận cho câu trả lời.

***ĐỊNH DẠNG CỦA OUTPUT***
1. OUTPUT cho THINKING
- Hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
- KHÔNG được để trống phần suy luận. 
- KHÔNG được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho ANSWER
- Chỉ đưa ra 1 ký tự duy nhất từ tập {A, B, C, D} và viết vào giữa 2 thẻ <output> và </output>
- KHÔNG được kèm theo bất kỳ từ ngữ, ký tự hoặc giải thích nào khác ở phần này.
- KHÔNG được viết câu kiểu “Đáp án là A”.
- KHÔNG được viết lại câu hỏi.

**YÊU CẦU TUÂN THỦ NGHIÊM NGẶT**:
- Nội dung thinking và câu trả lời phải được viết trong các thẻ tương ứng, không được viết bên ngoài.
- Nội dung answer phải nằm trong 2 thẻ <output> và </output>.
- Nội dung của thinking và answer không được để trống.
- Không được đổi tên thẻ hoặc thêm thẻ mới.
- Không được dùng ký tự khác ngoài A/B/C/D bên trong 2 thẻ <output> và </output>.
- Định dạng phải chính xác tuyệt đối.
- Chỉ in ra chữ cái là 1 trong 4 phương án, KHÔNG viết nội dung của phương án.

***Các ví dụ đúng***:
<think>Suy nghĩ của bạ ...</think>
<output>A</output>
***Các ví dụ sai:***
1) Đáp án là A
<output>A – tôi chọn đáp án này</output>
2) <output>A: Cổ vũ đua xe</output>
3) A: Cổ vũ đua xe
4) <output>A</output>
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
Instruction: Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: Nam là một thí sinh thuộc diện xét tuyển thẳng vào đại học theo quy định mới. Trường của Nam yêu cầu cam kết nhập học sớm và nộp hồ sơ trực tiếp. Bạn của Nam, Hoa, cũng thuộc diện xét tuyển thẳng nhưng không nhận được yêu cầu như vậy từ trường của mình và được cho phép nộp hồ sơ trực tuyến. Nam thắc mắc liệu yêu cầu của trường mình có hợp lệ không? Với thông tin này, làm thế nào để xác định trường hợp của Nam?
Đáp án: "A: Có, yêu cầu của trường Nam hợp lệ vì mỗi cơ sở đào tạo có thể tự điều chỉnh cách thức tuyển sinh khác nhau.\nB: Không, yêu cầu này không hợp lệ vì thí sinh có quyền được lựa chọn hình thức nộp hồ sơ và cam kết nhập học theo kế hoạch chung.\nC: Không, yêu cầu này không hợp lệ vì các cơ sở đào tạo không được yêu cầu thí sinh cam kết nhập học sớm và phải cho phép nộp hồ sơ trực tuyến.\nD: Có, yêu cầu này là hợp lệ vì các cơ sở đào tạo có quyền yêu cầu cam kết nhập học sớm để đảm bảo số lượng thí sinh."
Đáp án đúng: C
"""
