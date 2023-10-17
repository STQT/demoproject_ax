FROM python:3.8.10

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN CURRENT_USER=$(whoami) && chown -R $CURRENT_USER:$CURRENT_USER /app/db

# Use the user command to switch to the current local OS user
USER $CURRENT_USER

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
