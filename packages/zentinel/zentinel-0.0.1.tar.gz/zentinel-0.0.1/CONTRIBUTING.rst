Contributing
----

 .. code-block:: sh

    git clone git@github.com:symonk/zentinel.git
    cd restpite
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[tests]"
    pre-commit install
    # make a branch and apply changes
    tox -e linting, py38
    push changes to upstream branch and open a pull request!
