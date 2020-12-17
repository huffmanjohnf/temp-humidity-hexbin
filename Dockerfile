FROM python:3.7
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
EXPOSE 8501