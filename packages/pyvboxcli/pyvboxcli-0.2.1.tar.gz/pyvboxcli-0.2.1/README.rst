.. SPDX-License-Identifier: MIT

PYthon wrapper for VirtualBOX Command-Line Interface
====================================================

This is a small tool providing a python wrapper around virtualbox command-line
tools. It does not depend on any SDK, instead it mostly just parses the output
of ``VBoxManage --machinereadable``

It is also executable by itself providing small helpers on top of VBoxManage
itself.

Usage
-----

``pipx run pyvboxcli --help``

Documentation
-------------

* Published via `gitlab pages <https://cdleonard.gitlab.io/pyvboxcli/sphinx>`_
* Generate: ``tox -e docs``

Testing
-------

* Run ``tox`` or ``pytest``
* CI: https://gitlab.com/cdleonard/pyvboxcli/-/pipelines

Some tests use vagrant to create a target VM, they are skipped if vagrant or
virtualbox is missing. The gitlab pipeline runs python tests in two jobs:

* "mini-test", only relying on python
* "full-test", relying on vagrant and a priviledged gitlab runner.

Other notes:

* Full Test Coverage: https://gitlab.com/cdleonard/pyvboxcli/-/jobs/artifacts/main/file/htmlcov/index.html?job=mini-test
* Mini Test Coverage: https://gitlab.com/cdleonard/pyvboxcli/-/jobs/artifacts/main/file/htmlcov/index.html?job=full-test

Some tests use vagrant to create a real virtualbox VM. The target VM is
automatically started and halted by the test session. If the target is already
running it is kept running after the test, so to reduce test time you can do::

    ( cd vagrant-target && vagrant up)
