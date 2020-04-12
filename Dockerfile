FROM python:3.7.7-slim-stretch

RUN apt update && \
    apt install -y python3-dev gcc

WORKDIR app 
# Install pytorch and fastai
#RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html

ADD requirements.txt .
RUN pip install -r requirements.txt
#pip install --no-cache-dir -r
ADD models models
ADD . .

# Run it once to trigger resnet download
RUN python main.py prepare

#EXPOSE 5000

# Start the server
CMD ["python", "main.py", "serve"]
