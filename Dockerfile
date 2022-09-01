FROM tomcat:10-jdk11-temurin-focal
LABEL maintainer="https://github.com/oracle/opengrok"

# install dependencies and Python tools
RUN apt update && \
    apt install --no-install-recommends -y git subversion unzip inotify-tools python3 python3-pip \
    vim gpg gpg-agent tree htop\
    python3-venv python3-setuptools openssh-client

# compile and install universal-ctags
RUN apt install --no-install-recommends -y pkg-config automake build-essential && \
    git clone https://github.com/universal-ctags/ctags /root/ctags && \
    cd /root/ctags && ./autogen.sh && ./configure && make && make install && \
    apt remove -y automake build-essential && \
    apt -y autoremove && apt -y autoclean && \
    cd /root && rm -rf /root/ctags && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# prepare OpenGrok binaries and directories
# COPY --from=build opengrok.tar.gz /opengrok.tar.gz
RUN curl -L https://github.com/oracle/opengrok/releases/download/1.7.35/opengrok-1.7.35.tar.gz -o /opengrok.tar.gz

# hadolint ignore=DL3013
RUN mkdir -p /opengrok /opengrok/etc /opengrok/data /opengrok/src && \
    tar -zxvf /opengrok.tar.gz -C /opengrok --strip-components 1 && \
    rm -f /opengrok.tar.gz


# environment variables
ENV SRC_ROOT /opengrok/src
ENV DATA_ROOT /opengrok/data
ENV URL_ROOT /
ENV CATALINA_HOME /usr/local/tomcat
ENV CATALINA_BASE /usr/local/tomcat
ENV CATALINA_TMPDIR /usr/local/tomcat/temp
ENV PATH $CATALINA_HOME/bin:$PATH
ENV CLASSPATH /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar

#install opengrok_tools
COPY tools/dist/*.gz /opengrok/tools/opengrok-tools.tar.gz
RUN python3 -m pip install --no-cache-dir /opengrok/tools/opengrok-tools* && \
python3 -m pip install --no-cache-dir Flask Flask-HTTPAuth waitress # for /reindex REST endpoint handled by start.py

# disable all file logging
COPY docker/scripts/logging.properties /usr/local/tomcat/conf/logging.properties
RUN sed -i -e 's/Valve/Disabled/' /usr/local/tomcat/conf/server.xml

#add config
COPY docker/config /opengrok/etc

# add our scripts
COPY docker/scripts /scripts
RUN chmod -R +x /scripts

RUN mkdir -p /root/.gnupg && cp /opengrok/etc/gpg-agent.conf /root/.gnupg/gpg-agent.conf
#COPY config/gpg-agent.conf /root/.gnupg/gpg-agent.conf

# run
WORKDIR $CATALINA_HOME
EXPOSE 8080
CMD ["/scripts/start.py"]
