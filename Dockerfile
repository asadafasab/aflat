from python:latest

WORKDIR /app
COPY . /app/aflat
RUN python3 -m pip --no-cache-dir install -r aflat/requirements.txt
EXPOSE 7777 
RUN sed -i "s/TODO_to_replace/`python -c 'import random;from string import ascii_letters;print("".join([random.choice(ascii_letters+"1234567890") for _ in range(32)]))'`/g" aflat/main.py
ENTRYPOINT ["waitress-serve"]
CMD ["--port=7777", "--call", "aflat.main:create_app"]
