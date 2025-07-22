FROM tobix/pywine:3.11

# install required dependencies (pip package adi-reader needs vcrun2015)
RUN apt-get update && apt-get install -y wget cabextract && \
    wget -O /usr/local/bin/winetricks https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks && \
    chmod +x /usr/local/bin/winetricks

RUN set -xe	&& \
    WINEDLLOVERRIDES="mscoree,mshtml=" xvfb-run wine wineboot && \
    xvfb-run wineserver -w && \
    xvfb-run winetricks -q vcrun2015

RUN apt-get update && apt-get install -y python3-full python3-pip python3-opencv iproute2 net-tools procps lsof

ENV TZ='Europe/Prague'

COPY requirements.txt requirements.txt

RUN python3 -m venv /venv

RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install --upgrade setuptools
#debugging only
#RUN /venv/bin/pip install --upgrade debugpy
RUN /venv/bin/pip install -r requirements.txt

ENV PATH="/venv/bin:$PATH"

COPY requirements.windows.txt requirements.windows.txt

RUN wine python -m pip install --upgrade pip
RUN wine python -m pip install --upgrade setuptools
#debugging only
#RUN wine python -m pip install --upgrade debugpy

RUN wine cmd /c setx PATH "C:\\Python\\Scripts;%PATH%" && \
    wine pip install -r requirements.windows.txt

COPY . /src/

WORKDIR /src

EXPOSE 5000
#debugging only
#EXPOSE 5678

#debugging only
#CMD ["python", "-Xfrozen_modules=off", "-m", "debugpy", "--listen", "0.0.0.0:5678", "app.py"]

#CMD ["python", "app.py"]
CMD ["bash"]