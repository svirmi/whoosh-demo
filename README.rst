Whoosh demo application
=======================

Overview
--------

This is a version of the quick demo application I made for my PyCon 2013 presentation.

The demo source has two halves. It contains code to index the Python documentation, and a simple Flask web app to search and inspect a Whoosh index.


Requirements
------------

* `Whoosh`_ search library.
* `Flask`_ WSGI microframework.
* `Mako`_ templating engine.
* tzellman's `Flask Mako plugin`_ to integrate Mako with Flask. NOTE: the Flask-Mako package on PyPI will not work.

.. _Whoosh: https://bitbucket.org/mchaput/whoosh
.. _Flask: http://flask.pocoo.org/
.. _Mako: http://www.makotemplates.org/
.. _Flask Mako plugin: https://github.com/tzellman/flask-mako/


Get the demo source code
------------------------

Use Mercurial to clone the demo source code::

    % hg clone https://bitbucket.org/mchaput/whoosh-demo
    % cd whoosh-demo


Index the Python documentation
------------------------------

Use Mercurial to fetch the Python source code (this can take a while)::

    % hg clone http://hg.python.org/cpython

The demo code includes the ability to search by revision number and/or date (to show the use of ``NUMERIC`` and ``DATETIME`` fields). Use the ``list_revisions.py`` script to generate a file mapping filenames to revision numbers::

    % python scripts/list_revisions.py cpython/Doc >revs.txt

Run the ``index_python.py`` script to index the Python documentation::

    % mkdir index
    % python scripts/index_python.py cpython/Doc index revs.txt

The index has the following fields.

* ``path`` - the path to the document.
* ``title`` - the document title.
* ``tgrams`` - the document title as N-grams.
* ``content`` - the document content (including the title).
* ``chapter`` - the directory name containing the document.
* ``size`` - the size of the original file in bytes.
* ``rev`` - the Mercurial revision number in which the file was last committed.
* ``revised`` - the date of the revision in which the file was last committed.
* ``modref`` - a reference to a module. For example, searching for ``modref:hashlib`` will find files that reference the ``hashlib`` module.
* ``clsref`` - a reference to a class.
* ``funcref`` - a reference to a function.
* ``pep`` - a reference to a PEP.
* ``cls`` - the documentation for a class. For example, searching for ``cls:zipfile`` will find the documentation for the ``ZipFile`` class.
* ``mod`` - the documentation for a module.


Start the web server
--------------------

Set the WHOOSHINDEX environment variable to the index directory you want to search::

    % export DEMOSOURCE=cpython/Doc
	% export DEMOINDEX=index

On Windows::

    > set demosource=cpython/Doc
	> set whooshindex=index

Run the ``present.py`` script to start the web server::

	% python present.py

In a browser go to the following address for the search interface::

	http://127.0.0.1:5000/

There are two additional server apps available:

* ``http://127.0.0.1:5000/analyzer`` - choose a field and enter text to see the tokens produced by that field's analyzer.
* ``http://127.0.0.1:5000/lexicon`` - choose a field to see a list of all the indexed terms in that field. WARNING: can produce enourmous, slow-loading pages for fields with thousands of terms (such as ``tgrams``).










