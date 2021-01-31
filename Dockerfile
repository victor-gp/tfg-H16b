FROM python:3.6.9 as install-less
RUN apt update
RUN apt install less

FROM python:3.6.9
COPY --from=install-less /bin/less /bin/less

# create a user so result/log files aren't attributed to "root"
RUN useradd -m user
USER user
ENV HOME=/home/user

ENV \
   # make poetry create the virtual environment in the project's root as `.venv`
   POETRY_VIRTUALENVS_IN_PROJECT=true \
   # do not ask any interactive question
   POETRY_NO_INTERACTION=1

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=$HOME/.poetry/bin:$PATH

# install project dependencies
COPY --chown=user pyproject.toml poetry.lock $HOME/tfg-H16b/
WORKDIR $HOME/tfg-H16b
RUN poetry install

# load poetry shell automatically
RUN echo 'poetry shell' >> $HOME/.bashrc

COPY --chown=user . $HOME/tfg-H16b

CMD ["bash"]
