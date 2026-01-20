EXAMPLE = """
Bạn sẽ được cung cấp một câu hỏi bao gồm 2 chủ thể pháp lý và một đoạn văn chứa điều/khoản trong một hợp đồng liên quan đến hai chủ thể đó.
Format của câu hỏi sẽ như sau:
BÊN A: <Tên bên A>
BÊN B: <Tên bên B>
ĐIỀU/KHOẢN: <Nội dung điều/khoản trong hợp đồng>
Dựa trên điều/khoản được cung cấp, bên nào có lợi hơn trong hợp đồng này?
A. Có lợi cho bên A B. Có lợi cho bên B C. Công bằng
Nhiệm vụ của bạn là đọc và xác định xem bên nào là bên có lợi hơn trong hợp đồng dựa trên điều/khoản được cung cấp.
Chỉ trả lời bằng một chữ cái duy nhất: A, B, hoặc C.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.
Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.
"""

EXAMPLE_FEWSHOT = """
Bạn sẽ được cung cấp một câu hỏi bao gồm 2 chủ thể pháp lý và một đoạn văn chứa điều/khoản trong một hợp đồng liên quan đến hai chủ thể đó.
Format của câu hỏi sẽ như sau:
BÊN A: <Tên bên A>
BÊN B: <Tên bên B>
ĐIỀU/KHOẢN: <Nội dung điều/khoản trong hợp đồng>
Dựa trên điều/khoản được cung cấp, bên nào có lợi hơn trong hợp đồng này?
A. Có lợi cho bên A B. Có lợi cho bên B C. Công bằng
Nhiệm vụ của bạn là đọc và xác định xem bên nào là bên có lợi hơn trong hợp đồng dựa trên điều/khoản được cung cấp.
Chỉ trả lời bằng một chữ cái duy nhất: A, B, hoặc C.
KHÔNG được giải thích, KHÔNG được thêm bất kỳ text nào khác.
Không thêm các token thuộc về giải thích, suy luận như </think> hoặc ***Giải thích***.

Dưới đây là một ví dụ để bạn tham khảo:
Instruction: Đánh giá xem điều khoản hợp đồng này có công bằng cho hai bên không. Chọn đáp án đúng nhất trong các lựa chọn A, B, C, D được cung cấp, chỉ chọn đáp án và không giải thích gì thêm."
Câu hỏi: Trong hợp đồng giữa VĂN PHÒNG THỬA PHÁT LẠI và BÊN YÊU CẦU THỰC HIỆN TỐNG ĐẠT, điều khoản về thủ tục thực hiện việc tống đạt quy định như thế nào và nó có lợi cho bên nào hơn? Bên A phải thực hiện tống đạt các giấy tờ trong vòng 24 giờ đối với yêu cầu từ Cơ quan thi hành án dân sự và 48 giờ đối với yêu cầu từ Tòa án hoặc Viện Kiểm sát nhân dân. Trong trường hợp không thể tống đạt trực tiếp, Bên A phải niêm yết công khai giấy tờ tại các địa điểm liên quan và báo cáo kết quả định kỳ 1 tuần/lần cho Bên B, trong khi chi phí phát sinh sẽ do Bên B thanh toán.
Đáp án: 'A': 'Có lợi cho bên A vì điều khoản này cho phép Bên A lựa chọn các biện pháp tống đạt linh hoạt mà không bị ràng buộc bởi thời gian.', 'B': 'Công bằng vì điều khoản này yêu cầu cả hai bên hợp tác chặt chẽ và chia sẻ trách nhiệm trong quá trình thực hiện tống đạt.', 'C': 'Có lợi cho bên A vì điều khoản này cho phép bên A có quyền từ chối các trường hợp không thể tống đạt trực tiếp mà không chịu trách nhiệm.', 'D': 'Có lợi cho bên B vì điều khoản này quy định rõ thời hạn và thủ tục tống đạt, giúp bên B kiểm soát và đảm bảo quá trình tống đạt được thực hiện đúng theo thỏa thuận.'
Đáp án đúng: "D"
"""