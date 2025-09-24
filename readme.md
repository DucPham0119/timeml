# Run code
streamlit run app.py

# Run Backend
uvicorn backend:app --reload --port 8000


# RUN SERVER
python3 -m streamlit run app.py --server.address=0.0.0.0 --server.port=8080

uvicorn backend:app --host 0.0.0.0 --port 8050

http://118.70.176.240:8501