sysplan: quick system configuration tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``sysplan apply`` command in the fashion of netplan.

Overview
========

CLI configuration
-----------------

``sysplan`` automates host configuration and requires root privilege. If you
install sysplan with ``pip install --user`` then you will need to run

Optionnal: install ``pygments`` for syntax highilightning.

Host configuration
------------------

``sysplan`` will parse ``/etc/sysplan.d/*.yaml`` for configuration and execute
python or shell plugins.

You can dump the configuration with: ``sysplan conf``.

YAML schema
-----------

The basic structure of the yaml configuration is like this:

.. code-block:: yaml

    plugin_name:
      your-first-plan-name:
        any: config
        for:
        - your plan

Examples
--------

The ``sysplan.d.example`` directory of the git repository contains reference
implementations which you can copy at will.

.. note:: They should work as-is, except for modules that are only documented
          but not yet implemented, all examples in this directory are tested in
          CI.

Testing
-------

You may use the example configuration for testing by exporting the
``SYSPLAN_D`` env var:

.. code-block:: shell

    export SYSPLAN_D=/path/to/git/clone/sysplan.d.example

The ``SYSPLAN_ROOT`` env var is nice to make sure ``sysplan`` won't write your
host:

.. code-block:: shell

    export SYSPLAN_ROOT=/tmp/test-sysplan-1

You may then use the example configuration, examples::

.. code-block:: shell

    sudo -sE sysplan conf
    sudo -sE sysplan diff
    sudo -sE sysplan test
    sudo -sE sysplan apply
    sudo -sE sysplan destroy

Tutorial
========

Basics and systemd
------------------

Try adding the following content into ``/etc/sysplan.d/example_systemd.yaml``:

.. code-block:: yaml

    services:
      sysplan-test-service:
        TEST_ENV_VAR: 2
        Unit:
          Description: Example Service
        Service:
          Type: oneshot
          ExecStart: /bin/bash -c 'echo nice!'
          WorkingDirectory: /tmp

    timers:
      sysplan-test-service:
        Timer:
          OnCalendar: '*-*-* 23:00:00'

    mounts:
      mnt-backups:
        Unit:
          Description: Mount NFS Share
        Mount:
          What: 172.24.0.5:/srv/backups
          Where: /mnt/backups
          Type: nfs
          Options: defaults
          TimeoutSec: 10
        Install:
          WantedBy: multi-user.target

Then, try the following commands:

- ``sysplan diff``
- ``sysplan apply``
- ``sysplan destroy``
- ``sysplan help``

Custom bash modules
-------------------

Add the following to ``/etc/sysplan.d/bash_example.yaml``:

.. code-block:: yaml

    bash_example.sh:
      plan-one:
        somevar: date
        nested:
        - item: /tmp/$plan_name

      plan-two:
        somevar: uname -a

Add the following to ``/etc/sysplan.d/bash_example.sh``:

.. code-block:: bash

    write() {
        $somevar > /tmp/$plan_name
        cat /tmp/$plan_name
    }

    diff() {
        if [ ! -f $nested_0_item ]; then
            echo + $nested_0_item TO CREATE
        else
            $somevar | $(which diff) -u $nested_0_item -
        fi
    }

    activate() {
        echo activated >> /tmp/$plan_name
    }

    destroy() {
        rm -rf /tmp/$plan_name
    }

Then again, play with the ``sysplan`` commands.

Builtin modules
===============

files
-----

You can also have files as such:

.. code-block:: yaml

    files:
      /etc/profile.d/pipuser.sh:
        mode: '0755'
        owner: root
        group: root
        content: |
          export PATH=$HOME/.local/bin:$PATH

docker & docker_compose
-----------------------

Docker has a special plan generation because of the variety of resources it has
to offer, example configuration:

.. code-block:: yaml

    docker:
      networks:
        web:
        test:

      volumes:
        test:

Custom python modules
=====================

Custom Python modules are registered on the ``sysplan`` entry points. For
example, this is how the systemd plans are registered is ``setup.py``:

.. code-block:: python

    entry_points={
        'sysplan': [
            'services = sysplan.systemd:ServicePlan',
            'mounts = sysplan.systemd:MountPlan',
            'timers = sysplan.systemd:TimerPlan',
        ],
    },

As such, the pointed python plan classes will be used for the ``services``,
``mounts`` and ``timers`` keys in sysplan yaml. Your plan classes should
inherit from the ``sysplan.plan.Plan`` class which is basically.

Each plan class defines 4 async methods that will be directly called:

- ``diff``: return the diff between current and target configuration
- ``write``: write the target configuration
- ``activate``: enable and start services
- ``destroy``: disable and remove everything

Another thing a Plan class can do, is change the ``Plan.factory()`` classmethod
to override how plans are generated from a plugin configuration. The
``DockerPlan`` plugin is a good example.
