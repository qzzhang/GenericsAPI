FROM kbase/kbase:sdkbase2.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update

RUN pip uninstall numpy -y \
    && pip install numpy==1.14.5

RUN pip install pandas \
    && pip install xlrd \
    && pip install openpyxl \
    && pip install xlsxwriter \
    && pip install dotmap

RUN pip uninstall networkx -y \
    && pip install networkx==2.1

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
