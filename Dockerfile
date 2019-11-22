FROM python:3.7
ENV DEBIAN_FRONTEND noninteractive

RUN pip install numpy==1.16.4
RUN pip install pandas==0.24.2
RUN pip install biopython
RUN pip install argparse
RUN pip install networkx==2.3
COPY swigg.py /usr/bin/
RUN chmod a+x /usr/bin/*

CMD ["swigg.py"]
