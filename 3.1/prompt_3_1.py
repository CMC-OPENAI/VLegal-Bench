PROMPT_CREATE_MULTIPLE_CHOICES = """
Bạn là một chuyên gia pháp luật. Dựa vào câu hỏi và danh sách các điều khoản văn bản pháp luật được cung cấp, hãy tạo ra một câu hỏi trắc nghiệm 4 lựa chọn (1 đúng, 3 sai) và trả về **chỉ** một chuỗi JSON theo định dạng sau (không có thêm văn bản nào khác):

'''json
{
    "Answer": {
        "A": "[đáp án A]",
        "B": "[đáp án B]",
        "C": "[đáp án C]",
        "D": "[đáp án D]"
    },
    "Ground Truth": "[A/B/C/D]"
}
'''

QUY TẮC CHÍNH (bắt buộc):
1. Tất cả **4 đáp án phải có cùng một cấu trúc** — tức **toàn bộ** đều ở một trong hai dạng sau (không trộn):
   - Dạng 1 (không có khoản): `Điều <số> <Tên văn bản>`  
     - regex: `^Điều \d+ .+$`
   - Dạng 2 (có khoản): `Khoản <số> Điều <số> <Tên văn bản>`  
     - regex: `^Khoản \d+ Điều \d+ .+$`

2. Quy trình chọn đáp án:
   a) Trước hết, hãy kiểm tra **toàn bộ danh sách điều khoản được cung cấp**.
   b) Chọn làm đáp án đúng (một mục từ danh sách được cung cấp) sao cho **có thể** tìm thêm ba đáp án sai (không trùng nhau, không trùng đáp án đúng) **cùng dạng** trong phạm vi các điều khoản **không nằm** trong danh sách được cung cấp (như yêu cầu ban đầu) — tức là đáp án sai không được là cùng mục chính xác từ danh sách nguồn.

3. Quy tắc về nguồn đáp án:
   - **Đáp án đúng**: phải là điều khoản **chính xác** lấy từ **danh sách điều khoản được cung cấp** trong đề bài.
   - **Đáp án sai** (3 cái): phải là các mục **không nằm trong danh sách điều khoản được cung cấp** (có thể là các điều khoản hợp lý, cùng cấu trúc nhưng giả định/không dùng các mục thực sự trùng với danh sách nguồn). Tuy nhiên **vẫn phải giữ cùng dạng** với đáp án đúng (xem mục 1).

4. Định dạng nghiêm ngặt:
   - Không thêm chữ/đoạn phụ không thuộc hai dạng trên (không dùng `Điểm`, `Mục`, `Phần`, ký tự thừa, dấu phẩy, ngoặc).
   - Không thêm khoảng trắng thừa ở đầu/cuối.
   - Mỗi đáp án phải là một chuỗi khớp **chính xác** với một trong hai regex đã nêu.

5. Kiểm tra và sửa tự động trước khi trả về:
   - Kiểm tra rằng đáp án đúng nằm trong danh sách điều khoản được cung cấp.
   - Kiểm tra rằng 3 đáp án sai **không** nằm trong danh sách điều khoản được cung cấp.
   - Kiểm tra rằng **tất cả** 4 đáp án đều khớp cùng một regex (chỉ 1 trong 2).
   - Nếu bất kỳ kiểm tra nào thất bại, **tự động sửa** bằng cách lặp lại bước chọn đáp án (thay đáp án đúng nếu cần) cho tới khi mọi điều kiện thỏa mãn.

6. Ví dụ minh họa:
   - Nếu bạn chọn đáp án đúng là `Điều 30 Nghị định 99/2024/NĐ-CP` (dạng `Điều ...`), thì 3 đáp án sai phải có dạng tương tự:
     - `Điều 15 Nghị định 66/2022/NĐ-CP`
     - `Điều 20 Nghị định 88/2023/NĐ-CP`
     - `Điều 45 Nghị định 77/2025/NĐ-CP`
   - Nếu đáp án đúng là `Khoản 2 Điều 15 Nghị định 66/2022/NĐ-CP` (dạng `Khoản ... Điều ...`), thì 3 đáp án sai phải có dạng tương ứng:
     - `Khoản 1 Điều 10 Nghị định 11/2020/NĐ-CP`
     - `Khoản 3 Điều 22 Nghị định 55/2021/NĐ-CP`
     - `Khoản 4 Điều 30 Nghị định 99/2024/NĐ-CP`

BẮT BUỘC: Trả về **chỉ** JSON theo cấu trúc đã nêu, không có bất kỳ giải thích hoặc văn bản nào khác.
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
Nhiệm vụ của bạn là trả lời câu hỏi trắc nghiệm sau, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: "Đọc câu hỏi sau và trả về các điều - khoản - văn bản liên quan hoặc hỗ trợ trả lời câu hỏi. Chỉ cần chọn một trong 4 đáp án đúng, không cần giải thích gì thêm.
Câu hỏi: Hình thức xử lý tài sản do chủ sở hữu tự nguyện chuyển giao quyền sở hữu cho Nhà nước Việt Nam?
Đáp án: "A: Khoản 4 Điều 10 Nghị định 88/2023/NĐ-CP\nB: Khoản 1 Điều 20 Nghị định 66/2022/NĐ-CP\nC: Khoản 1 Điều 8 Nghị định 77/2025/NĐ-CP\nD: Khoản 2 Điều 15 Nghị định 88/2023/NĐ-CP", 
Đáp án đúng: "C"
"""