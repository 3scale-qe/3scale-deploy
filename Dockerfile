FROM quay.io/centos/centos:stream9 as BUILDER

RUN yum update -y \
    && yum install -y tar gzip pip gettext

RUN   pip3 install poetry \
      && mkdir -p /opt/workdir/3scale_deploy

WORKDIR /opt/workdir/3scale_deploy

COPY . .

RUN poetry build

FROM quay.io/centos/centos:stream9

RUN yum update -y &&\
    yum install -y tar gzip pip gettext &&\
    yum clean all

RUN curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz | tar xz -C /usr/local/bin
COPY --from=BUILDER /opt/workdir/3scale_deploy/dist/3scale_deploy* /root/

RUN pip3 --no-cache-dir install /root/3scale_deploy*.whl \
    && rm /root/3scale_deploy*.whl \
    && useradd -m user -U

USER user

ENTRYPOINT [ "trdpl" ]
CMD ["install"]

