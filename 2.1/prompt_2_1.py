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
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token </think> hoặc ***Giải thích***.

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
hãy viết toàn bộ phần suy luận chi tiết nằm giữa 2 thẻ <think> và </think>. Đây là nơi bạn phân tích câu hỏi và đưa ra suy luận cho câu trả lời.
Không được để trống. Không được viết nội dung suy luận nằm bên ngoài 2 thẻ.

2. OUTPUT cho ANSWER
chỉ đưa ra một hoặc nhiều ký tự trong tập {A, B, C, D} và viết vào giữa 2 thẻ <output> và </output>
KHÔNG được kèm theo bất kỳ từ ngữ, ký tự hoặc giải thích nào khác ở phần này.
KHÔNG được viết câu kiểu “Đáp án là A”.
KHÔNG được viết lại câu hỏi.

**YÊU CẦU TUÂN THỦ NGHIÊM NGẶT**:
Nội dung thinking và câu trả lời phải được viết trong các thẻ tương ứng, không được viết bên ngoài.
Không được đổi tên thẻ hoặc thêm thẻ mới.
Không được dùng ký tự khác ngoài A/B/C/D bên trong 2 thẻ <output> và </output>.
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
Nhiệm vụ của bạn là đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Chỉ đưa ra kết quả, không cần giải thích. Không thêm các token </think> hoặc ***Giải thích***.

**QUAN TRỌNG**: Bạn CHỈ ĐƯỢC TRÀ LỜI bằng MỘT CHỮ CÁI duy nhất: A, B, C, hoặc D.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.

Ví dụ đúng: A
Ví dụ sai: Đáp án là A
Ví dụ sai: A. Đây là đáp án đúng vì...

Chỉ trả lời: A hoặc B hoặc C hoặc D

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đọc câu hỏi sau và chọn đáp án đúng, chỉ cần chọn đáp án và không cần giải thích gì thêm.
Câu hỏi: "Tình huống sau có bao nhiêu quan hệ pháp luật? \nTheo đơn khởi kiện và trong quá trình giải quyết vụ án và tại phiên tòa, nguyên đơn trình bày:\nBà có phần đất toạ lạc tại ấp L, xã H, huyện C, tỉnh Cà Mau (nay là Ấp L, xã H, tỉnh Cà Mau), diện tích 500m2 (ngang 10m, dài 50m), do bà nhận chuyển nhượng từ bà Lưu Thu T3 vào năm 2019. Đến ngày 20/9/2020 bà phát hiện ông Võ Quốc M cặp ranh đã lấn sang phần đất của bà, theo đo đạc thực tế thì phấn đất của bà bị ông M và bà B lấn chiếm là 8,9m2 (điểm M4, M5, M6, M7). Đối với hàng rào ông M và bà B xây dựng trên phần đất thì bà yêu cầu ông M và bà B phải tự tháo dỡ, di dời, bà không bồi thường hoặc hỗ trợ, di dời. Đồng thời, ông M và bà B cho V – Chi nhánh Tập đoàn C (V) thuê đất cắm cột điện để dẫn điện vào trạm Viettel trên phần đất của bà nên bà không thể bán đất làm thiệt hại cho bà. Do đó, bà yêu cầu ông M và bà B phải trả lại 50% giá trị hợp đồng thuê đất giữa V với ông M và bà B, thời gian tính từ ngày 20/9/2020 đến 22/11/2022 làm tròn 02 năm 02 tháng, mỗi tháng là 1.000.000 đồng với số tiền là 26.000.000 đồng; Từ ngày 23/11/2022 đến ngày 20/9/2023 làm tròn 09 tháng mỗi tháng là 1.150.000 đồng với số tiền là 10.350.000 đồng. Tổng số tiền bà yêu cầu ông M và bà B bồi thường cho bà là 36.350.000 đồng.\nBà thống nhất biên bản xem xét, thẩm định tại chỗ ngày 07/4/2023 và Biên bản định giá tài sản ngày 31/01/2024 của Toà án nhân dân huyện Cái Nước. Bà cũng thống nhất kết quả đo đạc của Công ty TNHH T4 và Chứng thư thẩm định giá của Công ty Cổ phần T5.\nNay ngoài việc yêu cầu ông M và bà B1 tháo dỡ, di dời hàng rào trả lại cho bà phần đất lấn chiếm như nêu trên, bà còn yêu cầu ông M và bà B bồi thường cho bà số tiền 36.350.000 đồng.\nDo sau khi khởi kiện thì ông M và bà B đã di dời 02 cây cột điện đi nên bà rút lại yêu cầu khởi kiện về việc buộc bị đơn di dời 02 cột điện.\nTrong quá trình giải quyết vụ án, bị đơn ông Võ Quốc M trình bày: Ông không có cắm trụ Viettel trên phần đất của bà H mà ông và V có cắm 02 cột dẫn điện kéo vào trụ V, tuy nhiên khi cắm 02 cột điện để dẫn điện vào trạm V thì ông có liên hệ với bà H để xác định ranh giới giữa ông và bà H nhưng không liên hệ được, do đó ông có nhờ chủ đất cũ đã bán cho ông là ông Ú (Không biết họ và chữ lót) ra chỉ ranh. Khi cắm cột điện thì ông không biết cắm lấn sang phần đất của bà H, sau đó thì bà H có đến cho rằng ông cắm cột điện lấn sang phần đất của bà H và bà H yêu cầu địa phương giải quyết. Tại buổi hoà giải của Ủy ban nhân dân xã H ông thừa nhận cắm cột điện dẫn điện vào trụ Viettel lấn sang phần đất của bà H và đồng ý di dời theo yêu cầu của bà H trong thời hạn 01 tháng. Sau đó ông có liên hệ với V để phối hợp di dời nhưng do không thống nhất được thời gian nên chưa di dời được. Đến năm 2022 khi bà H làm thủ tục để đổi lại giấy chứng nhận quyền sử dụng đất thì bà H có nói với ông từ từ dời cũng được, do đó ông cũng chưa dời liền. Sau khi ông nhận được thông báo thụ lý vụ án của Toà án nhân dân huyện Cái Nước thì ông đã phối hợp với V và di dời 02 cột điện khỏi phần đất của bà H. Do đó, bà H yêu cầu ông và bà B phải bồi thường 50% giá trị hợp đồng thuê đất giữa V với ông và bà B, tổng số tiền là 36.350.000 đồng thì ông không đồng ý.\nĐối với yêu cầu của bà H về việc buộc ông và bà B tháo dỡ, di dời hàng rào để trả lại phần đất có diện tích 8,9m2 thì ông không đồng ý. Ông và bà B làm hàng rào trên phần đất của ông, không có lấn chiếm đất của bà H. Theo đo đạc của Công ty T4 thì diện tích đất của ông vẫn thiếu so với diện tích được cấp.\nÔng thống nhất với biên bản xem xét, thẩm định tại chỗ ngày 07/4/2023 và Biên bản định giá tài sản ngày 31/01/2024. Ông cũng thống nhất với kết quả đo đạc của Công ty TNHH T4 và Chứng thư thẩm định giá của Công ty Cổ phần T5.\nNếu trường hợp có cơ sở để xác định ông xây dựng hàng rào trên phần đất của bà H thì ông sẽ tự di dời hàng rào, không yêu cầu bà H bồi thường, hỗ trợ di dời.\nĐại diện Viettel Cà M1 – Chi nhánh Tập đoàn C ông Nguyễn Chí T2 trình bày:"
Đáp án: "A. 4\nB. 3\nC. 5\nD. 2"
Đáp án đúng: "A"
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

