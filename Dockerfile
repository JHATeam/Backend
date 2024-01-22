FROM rockylinux:8

ENV LANG en_US.UTF-8
ARG CODE_HOME=/code

RUN dnf -y update && \
    dnf -y install \
        bzip2-devel \
        file \
        gcc \
        gcc-c++ \
        gettext \
        jq \
        libffi-devel \
        libxml2-devel \
        make \
        openssl-devel \
        postgresql \
        sqlite-devel \
        tar \
        tmux \
        wget \
        zlib-devel \
        && \
    dnf clean all 

ENV LD_LIBRARY_PATH "/usr/local/lib"

RUN cd /opt && \
    curl -O https://www.sqlite.org/2022/sqlite-autoconf-3370200.tar.gz && \
    tar -xzf sqlite-autoconf-3370200.tar.gz && \
    cd sqlite-autoconf-3370200 && \
    CPPFLAGS="-DSQLITE_ENABLE_FTS3 -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_MATH_FUNCTIONS" ./configure 1>/dev/null && \
    make 1>/dev/null && \
    make install 1>/dev/null && \
    cd /opt && \
    rm -rf sqlite-autoconf-3370200 && \
    rm -f sqlite-autoconf-3370200.tar.gz

RUN mkdir -p ${CODE_HOME}
WORKDIR ${CODE_HOME}
ARG PYTHON_VERSION=3.10.13

RUN curl -fsSO "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz" \
    && tar -xzf "Python-$PYTHON_VERSION.tgz" \
    && cd "Python-$PYTHON_VERSION" \
    && ./configure --enable-optimizations 1>/dev/null \
    && make -j4 altinstall 1>/dev/null \
    && ln -s \
        "/usr/local/bin/python${PYTHON_VERSION%.*}" \
        /usr/local/bin/python3 \
    && /usr/local/bin/python3 -c \
        "import sys; " \
        "print('Running python', sys.version);" \
        "assert sys.version == '${PYTHON_VERSION}', 'wrong python version'" 
    
# ################################
# # PYTHON PACKAGES
# ################################

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade --no-cache-dir $(grep -E "^pip==|^setuptools==|^wheel==" requirements.txt) && \
    python3 -m pip install --disable-pip-version-check --user --no-cache-dir "$(grep '^cython==' requirements.txt)" && \
    python3 -m pip install --disable-pip-version-check --user --no-cache-dir "$(grep '^numpy==' requirements.txt)" && \
    python3 -m pip install --disable-pip-version-check --user --no-cache-dir -r requirements.txt && \
    cd ${CODE_HOME} && \
    rm -rf "Python-$PYTHON_VERSION" && \
    rm -f "Python-$PYTHON_VERSION.tgz"

# ######################
# # PROJECT FILES
# ######################

COPY --chown==user:group scripts scripts
COPY --chown=user:group src src

CMD ["scripts/docker/entrypoint.sh"]



