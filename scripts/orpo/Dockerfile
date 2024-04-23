FROM pytorch

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN conda install conda-forge::pyarrow
RUN pip install -r requirements
COPY . .

# ENTRYPOINT [ "bash", "train.sh" ]