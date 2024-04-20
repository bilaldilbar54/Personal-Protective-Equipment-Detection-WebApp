FROM python:3.9
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx
ADD . /app
WORKDIR /app
RUN pip install v4l2ctl
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["main.py"]