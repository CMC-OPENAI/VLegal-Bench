PROMPT_CREATE_DATASET = """
Bạn là một chuyên gia pháp lý với kiến thức sâu rộng về luật pháp Việt Nam. 
Bạn sẽ được cung cấp dữ liệu về hai quy phạm pháp luật, mâu thuẫn với nhau trong một vấn đề pháp luật cụ thể và lý do tại sao hai điều này lại mâu thuẫn với nhau. 
Hai quy phạm này gồm có một quy pham được kiểm tra và một quy phạm là căn cứ rà soát. 
Cụ thể dữ liệu bạn được cung cấp sẽ có dạng sau: 
{
    "quy_phạm_được_kiểm_tra": {
        "Số ký hiệu": Số ký hiệu của quy phạm được kiểm tra,
        "Vị trí": Vị trí của quy phạm được kiểm tra trong văn bản pháp luật,
        "Nội dung quy phạm": Nội dung chi tiết của quy phạm được kiểm tra
    },
    "quy_phạm_là_căn_cứ_ra_soát": {
        "Số ký hiệu": Số ký hiệu của quy phạm là căn cứ rà soát,
        "Vị trí": Vị trí của quy phạm là căn cứ rà soát trong văn bản pháp luật,
        "Nội dung quy phạm": Nội dung chi tiết của quy phạm là căn cứ rà soát
    },
    "lý_do_mâu_thuẫn": Lý do tại sao hai quy phạm này lại mâu thuẫn với nhau
}
Nhiệm vụ của bạn là tạo ra MỘT câu hỏi trắc nghiệm với BỐN phương án trả lời, theo định dạng JSON như sau:
{
    "Instructions": "Dựa trên tình huống và vấn đề pháp luật được cung cấp, hãy xác định mâu thuẫn giữa hai quy phạm pháp luật và chọn phương án trả lời đúng nhất. Chỉ chọn một trong 4 phương án A, B, C, D và không giải thích gì thêm.",
    "Question": "Dưới đây là dữ liệu về hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm làm căn cứ rà soát: \n
    Quy phạm được kiểm tra: [Nội dung của quy phạm được kiểm tra] \n
    Quy phạm làm căn cứ rà soát: [Nội dung của quy phạm là căn cứ rà soát]. \n
    Quy phạm được kiểm tra có mâu thuẫn gì với quy phạm là căn cứ rà soát?",
    "Answers": {
        "A": "Phương án A",
        "B": "Phương án B",
        "C": "Phương án C",
        "D": "Phương án D"
    },
    "Ground Truth": "X",
}
Lưu ý: 
- Câu hỏi phải liên quan trực tiếp đến mâu thuẫn giữa hai quy phạm pháp luật được cung cấp.
- Mỗi phương án trả lời phải là một câu hoàn chỉnh và có ý nghĩa riêng biệt.
- Trong bốn phương án trả lời, chỉ có một phương án là đúng và phản ánh chính xác mâu thuẫn giữa hai quy phạm. Các phương án khác là những lựa chọn sai nhưng không khác biệt quá xa so với phương án đúng để tránh việc quá dễ dàng nhận biết đáp án đúng.
- Sử dụng thông tin trong trường "lý_do_mâu_thuẫn" để xây dựng các phương án trả lời.
- Sử dụng tối đa thông tin nội dung của cả 2 quy phạm để tạo ra các phương án trả lời.
"""

EXAMPLE = """
Nhiệm vụ của bạn là xác định Có hay Không mâu thuẫn giữa hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm rà soát.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
BẮT BUỘC phải dùng tiếng Việt. Không có resoning. KHông lặp lại câu hỏi.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI Có hoặc Không.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ cho câu trả lời ĐÚNG với yêu cầu: Có
Ví dụ cho câu trả lời ĐÚNG với yêu cầu: Không
"""

EXAMPLE_REASONING = """
Nhiệm vụ của bạn là xác định CÓ hay KHÔNG CÓ mâu thuẫn giữa hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm rà soát. Để trả lời được câu hỏi, bạn phải suy nghĩ và đưa ra lập luận cho câu trả lời.

***ĐỊNH DẠNG CỦA OUTPUT***
1. OUTPUT cho THINKING
Bạn phải thực hiện ĐÚNG các bước sau:
- hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
- Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.
- Chỉ sử dụng tiếng Việt, không sử dụng tiếng nào khác.

2. OUTPUT cho ANSWER
- chỉ đưa ra hoặc "Có" hoặc "Không" và viết vào giữa 2 thẻ <output> và </output>
- KHÔNG được kèm theo bất kỳ từ ngữ, ký tự hoặc giải thích nào khác ở phần này.
- KHÔNG được viết câu kiểu “Đáp án là Có”.
- KHÔNG được viết lại câu hỏi.

**YÊU CẦU TUÂN THỦ NGHIÊM NGẶT**:
- Nội dung thinking và câu trả lời phải được viết trong các thẻ tương ứng, không được viết bên ngoài.
- Không được đổi tên thẻ hoặc thêm thẻ mới.
- Không được dùng ký tự khác ngoài A/B/C/D bên trong 2 thẻ <output> và </output>.
- Định dạng phải chính xác tuyệt đối.

Ví dụ đúng:
<think>Phân tích nội bộ...</think>
<output>Có</output>

Ví dụ sai:
Đáp án là Có
<output>Có – tôi chọn đáp án này</output>
"""

# EXAMPLE_FEWSHOT = """
# Nhiệm vụ của bạn là xác định CÓ hay KHÔNG CÓ mâu thuẫn giữa hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm rà soát.
# Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
# BẮT BUỘC phải dùng tiếng Việt.

# **QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI CÓ hoặc KHÔNG.
# KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

# *** VÍ DỤ VỀ CÁCH TRẢ LỜI ĐÚNG YÊU CẦU VÀ SAI YÊU CẦU ***:
# Ví dụ cho câu trả lời đúng với yêu cầu: CÓ
# Ví dụ cho câu trả lời sai yêu cầu: 
# - Có mâu thuẫn. (sai vì không đúng định dạng)
# hoặc
# - Có mâu thuẫn vì ... (sai vì có giải thích thêm)

# Dưới đây là một ví dụ để bạn tham khảo:
# Instruction: "Xác định xem hai quy phạm pháp luật dưới đây (quy phạm được kiểm tra và quy phạm là căn cứ rà soát) có mâu thuẫn với nhau hay không. Trả lời \"Có\" nếu chúng mâu thuẫn và \"Không\" nếu chúng không mâu thuẫn.
# Câu hỏi: "Dưới đây là dữ liệu về hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm làm căn cứ rà soát: \n\nQuy phạm được kiểm tra: ['06/2015/QĐ-UBND', 'Điểm a, Khoản 3, Điều 11, Quyết định số 06/2015/QĐ-UBND', 'Điều 14.\\n\\n2. Quyền con người, quyền công dân chỉ có thể bị hạn chế theo quy định của luật trong trường hợp cần thiết vì lý do quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội, đạo đức xã hội, sức khỏe của cộng đồng.'] \n\nQuy phạm làm căn cứ rà soát: ['17/2003/QH11\\n\\n02/2006/TT-BTS \\n\\nHiến pháp năm 2013', 'Luật Thủy sản năm 2003\\n\\nPhụ lục 7 ban hành kèm theo Thông tư số 02/2006/TT-BTS\\n\\nKhoản 2, Điều 14, Hiến pháp năm 2013', 'Điều 14.\\n\\n2. Quyền con người, quyền công dân chỉ có thể bị hạn chế theo quy định của luật trong trường hợp cần thiết vì lý do quốc phòng, an ninh quốc gia, trật tự, an toàn xã hội, đạo đức xã hội, sức khỏe của cộng đồng.']. \n\nQuy phạm được kiểm tra có mâu thuẫn gì với quy phạm là căn cứ rà soát?=
# Đáp án đúng: Có
# """

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
Instruction: "Xác định xem hai quy phạm pháp luật dưới đây (quy phạm được kiểm tra và quy phạm là căn cứ rà soát) có mâu thuẫn với nhau hay không. Trả lời \"Có\" nếu chúng mâu thuẫn và \"Không\" nếu chúng không mâu thuẫn.
Câu hỏi: Dưới đây là dữ liệu về hai quy phạm pháp luật: quy phạm được kiểm tra và quy phạm làm căn cứ rà soát: \n\nQuy phạm được kiểm tra: 06/2015/QĐ-UBND, Điểm a, Khoản 3, Điều 11, Quyết định số 06/2015/QĐ-UBND \n\nQuy phạm làm căn cứ rà soát: 17/2003/QH11, 02/2006/TT-BTS, Hiến pháp năm 2013. \n\nQuy phạm được kiểm tra có mâu thuẫn gì với quy phạm là căn cứ rà soát?
Đáp án đúng: Có
"""