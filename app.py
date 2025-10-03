import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
from backend2 import process_request
# Logo giữa
logo = Image.open("./image/Logo-HUS.png")
buffered = BytesIO()
logo.save(buffered, format="PNG")
encoded_logo = base64.b64encode(buffered.getvalue()).decode()

st.markdown(
    f"""
    <div style="text-align: center; top: 5px; padding-bottom: 10px;">
        <img src="data:image/png;base64,{encoded_logo}" style=" height: 100px" />
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .st-emotion-cache-12fmjuu {
            height: 2px;
        }
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .st-emotion-cache-mtjnbi {
            width: 100%;
            padding: 1rem 1rem 1rem !important;
            max-width: 98% !important;
        }
        .st-emotion-cache-16tyu1 h6{
            padding: 0.25rem 0px 0.25rem !important;
        }

        /* Căn giữa tiêu đề */
        .stTitle, h1 {
            text-align: center !important;
        }
        
        .st-bz {
            height: 3px !important;
        }
        .st-emotion-cache-1s2v671 {
            min-height: 1.5px !important;
        }
        .st-emotion-cache-ocsh0s {
            margin: 1px !important;
            padding: 0.5rem 0.75rem !important;
            background-color: rgb(255, 255, 255) !important;
        }
        /* Căn giữa phần tử trong layout */
        .centered {
            text-align: center;
        }

        .title {
            font-size: 48px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 20px;
            color: #888;
            margin-bottom: 30px;
        }

        /* Chỉnh chiều rộng cho các khối input */
        .stTextArea, .stSelectbox, .stMultiSelect, .stButton {
            width: 100% !important;
        }
        
        /* Đặt màu nền trắng cho text_area, selectbox, và button */
        .st-bc   {
            background-color: rgb(255, 255, 255) !important; */
            border: 3px solid black !important; /* Tùy chọn: thêm viền nhẹ */
        }
        .st-b1 {
            background-color: rgb(255, 255, 255) !important; */
            border: 3px solid black !important; /* Tùy chọn: thêm viền nhẹ */
        }

        .stButton > button {
            background-color: rgb(240, 242, 246) !important;
            border: 3px solid rgb(200, 200, 200) !important; 
        }
        /* Đảm bảo các khối nằm ngang đúng */
        .stColumn {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Tiêu đề
st.title("Trích xuất TIME & EVENT")

# Ô nhập văn bản giống Stanford NLP demo
st.markdown("###### — Văn bản cần trích xuất —")
text = st.text_area(" ", placeholder="Nhập câu tiếng Việt cần xử lý...", height=120)

col1, col2, col3 = st.columns([4, 4, 1.5])

with col1:
    st.markdown("###### — Mô hình TIME —")
    time_model = st.selectbox(" ", ["", "GPT", "Gemini", "Heidel-Time", "Our-Model"])

with col2:
    st.markdown("###### — Mô hình EVENT —")
    event_model = st.selectbox(" ", ["", "GPT", "Gemini", "Our-Model"])

with col3:
    st.markdown("###### ")
    submitted = st.button("Submit")

# Xử lý submit
if submitted:
    if not text:
        st.error("❌ Bạn cần nhập câu tiếng Việt.")
    elif not time_model and not event_model:
        st.warning("⚠️ Bạn cần chọn ít nhất một mô hình TIME hoặc EVENT.")
    else:
        payload = {
            "text": text,
            "model_time": time_model if time_model != "" else None,
            "model_event": event_model if event_model != "" else None
        }

        # print(payload)

        try:
            # Gọi backen
            
            # response = requests.post("http://127.0.0.1:8000/extract", json=payload)
            respone = process_request(**payload)
            print('respone - done')
            # response.raise_for_status()

            # data = response.json()
            data = respone
            print('data-1')

            st.subheader("Kết quả:")

            # Xử lý hiển thị theo số lượng kết quả
            if data.get("time") or data.get("event"):
                # Có cả hai kết quả: chia làm 2 cột
                col_time, col_event = st.columns(2)
                with col_time:
                    st.markdown("##### 🕒 Thời gian")
                    st.text_area("", data["time"], height=150, key="time_result")
                with col_event:
                    st.markdown("##### 📌 Sự kiện")
                    st.text_area("", data["event"], height=150, key="event_result")
            elif data.get("time"):
                # Chỉ có kết quả thời gian
                st.markdown("##### 🕒 Thời gian")
                st.text_area("", data["time"], height=150, key="time_result_only")
            elif data.get("event"):
                # Chỉ có kết quả sự kiện
                st.markdown("##### 📌 Sự kiện")
                st.text_area("", data["event"], height=150, key="event_result_only")


        except requests.exceptions.RequestException as e:
            st.error(f"❌ Lỗi khi gọi backend: {e}")
        except Exception as e:
            st.error(f"❌ Lỗi hệ thống: {e}")
