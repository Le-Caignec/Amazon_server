FROM python:3.6
WORKDIR /
COPY . /
RUN pip install -r requirements.txt
EXPOSE 8050
CMD ["python3","menu_temps_reel.py"]