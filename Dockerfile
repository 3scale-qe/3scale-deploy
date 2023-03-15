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
    yum install -y tar gzip pip gettext

RUN curl https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz -o /root/oc.tar.gz
COPY --from=BUILDER /opt/workdir/3scale_deploy/dist/3scale_deploy* /root/

RUN tar xzf /root/oc.tar.gz \
    && cp {oc,kubectl} /usr/local/bin/ \
    && rm -r /root/oc.tar.gz oc kubectl \
    && useradd -m user -U \
    && pip3 --no-cache-dir install /root/3scale_deploy*.whl


ENTRYPOINT [ "trdpl" ]
USER user
CMD ["install"]

