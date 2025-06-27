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

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

#Expose Streamlit defualt port
EXPOSE 8501

#Run the app
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
CMD ["streamlit","run","Get_data_from_NCES.py", "--server.port=8501", "--server.address=0.0.0.0","--browser.gatherUsageStats=false"]

