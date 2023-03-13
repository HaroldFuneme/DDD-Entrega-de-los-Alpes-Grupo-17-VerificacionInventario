FROM python:3.9

EXPOSE 8000/tcp

COPY requirements.txt ./
RUN pip install --upgrade --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR "/src"

CMD [ "uvicorn", "verifica_invenratio.main:app", "--host", "localhost", "--port", "8000", "--reload"]