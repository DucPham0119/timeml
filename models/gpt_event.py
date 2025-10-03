import os

from openai import OpenAI
from openai import OpenAIError
import time

# Khởi tạo client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT_KEY")
client = OpenAI(api_key=api_key)


def tag_event(sentence: str) -> str:
    prompt = f"""
    Bạn là một công cụ trích xuất thời gian tiếng Việt theo tiêu chuẩn ISO-TIMEML. 
    Nhiệm vụ của bạn: Nhận một câu tiếng Việt và đánh dấu tất cả sự kiện bằng thẻ <EVENT>.

    Ví dụ:
    Input: "Tôi sống ở Hà Nội"
    Output: "Tôi <EVENT eid="e1" class="STATE" pos="VERB" tense="PRESENT" aspect="NONE" polarity="POS">sống</EVENT> ở Hà Nội."

    Input: "{sentence}"
    Output:
    """
    for attempt in range(3):  # thử tối đa 3 lần
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=200,
                timeout=60  # timeout 60 giây
            )
            return response.choices[0].message["content"].strip()
        except OpenAIError as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return "[ERROR] Failed to tag event"
