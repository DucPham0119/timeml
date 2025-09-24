import os

from openai import OpenAI

# Khởi tạo client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT_KEY")
client = OpenAI(api_key=api_key)


def tag_event(sentence: str) -> str:
    """
    Dùng GPT để gán <TIMEX3> cho các biểu thức thời gian trong câu.
    Trả về câu đã được đánh dấu.
    """

    prompt = f"""
                Bạn là một công cụ trích xuất thời gian tiếng Việt theo tiêu chuẩn ISO-TIMEML. 
                Nhiệm vụ của bạn: Nhận một câu tiếng Việt và đánh dấu tất cả sự kiện bằng thẻ <EVENT>.

                Ví dụ:
                Input: "Tôi sống ở Hà Nội"
                Output: "Tôi <EVENT eid="e1" class="STATE" pos="VERB" tense="PRESENT" aspect="NONE" polarity="POS">sống</EVENT> ở Hà Nội."

                Input: "{sentence}"
                Output:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # hoặc model GPT bạn có quyền dùng
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )

    tagged_sentence = response.choices[0].message["content"].strip()
    return tagged_sentence


