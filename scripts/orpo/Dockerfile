FROM pytorch

WORKDIR /app
RUN conda install conda-forge::pyarrow
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# ENTRYPOINT [ "bash", "train.sh" ]
