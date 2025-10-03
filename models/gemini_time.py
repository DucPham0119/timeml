# import google.generativeai as genai
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_KEY")

genai.configure(api_key=api_key)

def tag_timex3_gemini(sentence: str) -> str:
    """
    Dùng Gemini để gán <TIMEX3> cho biểu thức thời gian trong câu tiếng Việt.
    Trả về câu đã được đánh dấu.
    """

    prompt = f"""
            Bạn là một công cụ trích xuất thời gian tiếng Việt theo tiêu chuẩn ISO-TIMEML. 
            Nhiệm vụ của bạn: Nhận một câu tiếng Việt và đánh dấu tất cả biểu thức thời gian bằng thẻ <TIMEX3>.

            Ví dụ:
            Input: "Ngày 20 tháng 9 năm 2025 tôi phải hoàn thành công việc"
            Output: "Ngày <TIMEX3 tid="t1" type="DATE" value="2025-09-20">20 tháng 9 năm 2025</TIMEX3> tôi phải hoàn thành công việc."

            Input: "{sentence}"
            Output:
    """

    model = genai.GenerativeModel(model_name='gemini-2.5-flash')
    response = model.generate_content(prompt)

    # Lấy kết quả
    tagged_sentence = response.text.strip()
    return tagged_sentence


# Ví dụ sử dụng
# sentence = "Tôi sẽ đi làm vào ngày mai"
# result = tag_timex3_gemini(sentence)
# print(result)
