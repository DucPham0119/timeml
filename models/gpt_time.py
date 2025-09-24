import os

from openai import OpenAI

# Khởi tạo client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT_KEY")
client = OpenAI(api_key=api_key)


def tag_timex3(sentence: str) -> str:
    """
    Dùng GPT để gán <TIMEX3> cho các biểu thức thời gian trong câu.
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # hoặc model GPT bạn có quyền dùng
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )

    tagged_sentence = response.choices[0].message["content"].strip()
    return tagged_sentence

