FROM ubuntu:22.04
WORKDIR /workdir

COPY apt-requirements.txt .
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        dumb-init \
        $(cat apt-requirements.txt) \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade flit pip
COPY README.rst pyproject.toml ./
RUN touch pyvboxcli.py && \
    FLIT_ROOT_INSTALL=1 flit install --only-deps --extras test,mypy,dev && \
    rm -rf pyvboxcli.py

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
