FROM fcpindi/c-pac:latest
MAINTAINER The C-PAC Team <cnl@childmind.org>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# Install Docker
RUN apt-get install -y docker-cli

# Install Singularity
# v2.5.2
RUN apt-get install -y \
      flawfinder \
      squashfs-tools \
      uuid-dev \
      libuuid1 \
      libffi-dev \
      libssl-dev \
      libssl1.0.0 \
      libarchive-dev \
      libgpgme11-dev \
      libseccomp-dev && \
      git clone -b 2.5.2 https://github.com/sylabs/singularity && \
      cd singularity && \
      ./autogen.sh && \
      ./configure --prefix=/opt/singularity-2.5.2 --sysconfdir=/etc && \
      make && \
      make install

# set default Singularity @ 2.5.2
ENV PATH="/opt/singularity-2.5.2/bin:${PATH}"

# v.3.5.3
RUN apt-get install -y \
      build-essential \
      libgpgme-dev \
      wget \
      pkg-config \
      cryptsetup-bin && \
      export VERSION=1.14.4 OS=linux ARCH=amd64 && \
      wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
      tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
      rm go$VERSION.$OS-$ARCH.tar.gz && \
      echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
      echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
      . ~/.bashrc && \
      cd singularity && \
      git checkout v3.5.3 && \
      ./mconfig --prefix=/opt/singularity-3.5.3 && \
      make -C ./builddir && \
      make -C ./builddir install && \
      cd ..
      
RUN wget --content-disposition \
      https://s3.amazonaws.com/fcp-indi/resources/benchmark_package.tar.gz && \
      tar -xvf benchmark_package.tar.gz && \
      rm benchmark_package.tar.gz
      
# Get sample BIDS data
RUN mkdir -p /home/circleci/ && \
       git clone https://github.com/bids-standard/bids-examples.git \
       /home/circleci/bids-examples
      
ENTRYPOINT ["/bin/bash"]

# Link libraries for Singularity images
RUN ldconfig

RUN apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*