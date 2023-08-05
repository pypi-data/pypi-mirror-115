boom.py
=======

.. image:: https://img.shields.io/pypi/v/boompy.svg
    :target: https://pypi.python.org/pypi/boompy

``boom.py`` is a simple command line utiilty for storing text snippets under simple, memorable key names.
It is conceptually similar to `boom`_ by `Zach Holman`_.


Installation
------------

The easiest way to install `boom.py`_ is via `pip`_:

.. code-block:: console

    pip install boompy

You can also install it the old-fashioned way, if that's more your speed:

.. code-block:: console

    git clone https://github.com/epochblue/boom.py
    cd boom.py
    python setup.py install


Usage
-----

To create a new snippet, provide both the key name and a value for the key.

.. code-block:: console

    $> boom new_key new_value
    'new_key' is now 'new_value'.

To retrieve the value for a key once it's been set, simply provide the key name. The value will be automatically copied to the system clipboard.

.. code-block:: console

    $> boom new_key
    'new_key' successfully copied to clipboard.

If you attempt to set a value for an existing key, ``boom.py`` will return with an error.

.. code-block:: console

    $> boom new_key new_value
    Error: Key 'new_key' already exists.

If you'd like to update an existing key, use the ``--overwrite`` or ``-o`` flag:

.. code-block:: console

    $> boom --overwrite new_key updated_value
    'new_key' is now 'updated_value'.

And if you'd like to delete a key/value pair, use the ``--delete`` or ``-d`` flag.

.. code-block:: console

    $> boom --delete new_key
    'new_key' has been removed.

By default, ``boom.py`` stores its "database" in a file located at ``$HOME/.config/boom/boomdb``.
If you'd like to save your snippets to a different location, you can use the ``-db`` or ``--database`` flag:

.. code-block:: console

    $> boom --database ./snip.db new_key new_value
    'new_key' is now 'new_value'

If you provide no argument or options to ``boom.py``, it will print all the currently-stored records to the screen.

.. code-block:: console

    $> boom
    new_key     new_value
    new_key2    new_value2
    example     example_value

It's not much, but that's all there is to ``boom.py``.


License
-------

``boom.py`` is MIT licensed. Please see the included ``LICENSE`` file.

Authors
-------

* Bill Israel - `@epochblue`_ - `http://billisrael.info/`_

.. _boom: https://github.com/holman/boom
.. _Zach Holman: https://zachholman.com
.. _boom.py: https://github.com/epochblue/boom.py
.. _pip: https://pypi.python.org/
.. _@epochblue: https://twitter.com/epochblue
.. _http://billisrael.info/: http://billisrael.info/
