FROM python:3.12.6

# Set up the app
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir log/
RUN mkdir result/
COPY data/ .
COPY pages/ .
COPY src/ .
COPY template/ .
COPY Home.py .

# Expose the port Streamlit uses
EXPOSE 8501

# Entrypoint and command
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501"]
