# import google.generativeai as genai


import google.generativeai as genai
genai.configure(api_key="AIzaSyDfgc7Ukz_8aLJA7I3M2nJWLTCkXBIcbDk")

def tag_event_gemini(sentence: str) -> str:
    """
    Dùng Gemini để gán <TIMEX3> cho biểu thức thời gian trong câu tiếng Việt.
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

    model = genai.GenerativeModel(model_name='gemini-2.5-flash')
    response = model.generate_content(prompt)

    # Lấy kết quả
    tagged_sentence = response.text.strip()
    return tagged_sentence


# Ví dụ sử dụng
# sentence = "Tôi sẽ đi làm vào ngày mai"
# result = tag_event_gemini(sentence)
# print(result)
