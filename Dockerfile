FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    git clang make pkg-config flex bison \
    libprotobuf-dev protobuf-compiler \
    libnl-3-dev libnl-genl-3-dev libnl-route-3-dev \
    libcap-dev libseccomp-dev libelf-dev zlib1g-dev \
    && apt-get clean

WORKDIR /app

COPY . /app
RUN pip3 install Flask

# Build nsjail inside container
RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && make && cp nsjail /usr/local/bin/ && cd .. && rm -rf nsjail

EXPOSE 8080
CMD ["python3", "app.py"]
