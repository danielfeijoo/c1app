#Base image
FROM python:3.11-slim 

#Set Enviroment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

#Install system dependencies
RUN apt-get update && apt-get install -y  \
    wget  \
    unzip \ 
    curl  \
    chromium-driver  \
    chromium  \
    && rm -rf /var/lib/apt/lists/* 

#Set display port for Streamlit 
ENV DISPLAY=:99 

#Set working directory
WORKDIR /app

#Copy project files intp the container
COPY . /app
COPY .streamlit/  /app/.streamlit/
#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

#streamlit config
RUN mkdir -p /root/.streamlit && \ 
    echo "\ 
[server]\n\ 
headless = true\n\ 
port = 8501\n\ 
enableCORS = false\n\ 
enableXsrfProtection = false\n\ 
address = \"0.0.0.0\"\n\ 
\n\ 
[browser]\n\ 
gatherUsageStats = false\n\ 
" > /root/.streamlit/config.toml 

#Expose Streamlit defualt port
EXPOSE 8501

#Run the app
CMD ["streamlit","run","Get_data_from_NCES.py"]

