# docker build -t yvvidolov/linux-benchmark-cli:latest .
# docker run -it yvvidolov/linux-benchmark-cli:latest
# docker login
# docker push yvvidolov/linux-benchmark-cli:latest
# NOTE: mount volumes on disks you want to benchmark

FROM debian:bullseye-slim

# avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y wget unzip sysbench curl libncurses5 fio gawk

RUN apt-get install -y python3-minimal
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /home

RUN wget -O passmark.zip https://www.passmark.com/downloads/pt_linux_x64.zip && \
    wget -O fio.zip https://github.com/xlucn/fio-cdm/archive/refs/heads/master.zip && \
    wget -O prime95.tar.gz https://download.mersenne.ca/gimps/v30/30.19/p95v3019b20.linux64.tar.gz

RUN unzip passmark.zip && \
    unzip fio.zip && \
    mkdir prime95 && tar -xzf prime95.tar.gz -C prime95

RUN rm /home/passmark.zip /home/fio.zip
RUN rm -rf /var/lib/apt/lists/*

# Enable MOTD (does not work for portainer, as console exec issues clear)
RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/motd' >> /etc/bash.bashrc 
COPY motd /etc/motd

COPY help help
RUN chmod +x help

COPY bench_disk_dd.sh /home/fio-cdm-master/

# Entry point - does not
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["bash"]
