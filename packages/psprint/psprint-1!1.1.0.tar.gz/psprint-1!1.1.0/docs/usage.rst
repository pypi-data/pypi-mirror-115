#####
USAGE
#####

Substitute python's print
=========================

Import in your script.

.. code:: python

          from psprint import print

Supply value for ``mark`` kwarg or for any of the custom kwargs as described.

.. code:: python

          print("", mark="info")


.. note::

    You may have to add exception to ``${XDG_CONFIG_HOME}/pylintrc`` if you use linter

.. code:: ini

    [VARIABLES]
    redefining-builtins-modules=psprint


Configure frequently used ``mark`` in a suitably `located <configure.html#location-of-configuration-files>`__ configuration file.


Formatted string
===================

``psfmt`` `returns` prefixed args rather than `psprint`\ ing them.



Use similar to ``psprint``
------------------------------

.. code:: python

          from psprint import psfmt

          print(psfmt("The Quick Brown Fox", sep='', mark='list'))
          print(*psfmt("The Quick Brown Fox", mark='list'))


.. note::

   Notice that without separator `sep` argument,
   ``psfmt`` returns a ``list`` of args, prefixed.
   With the separator, ``psfmt`` returns them as ``str``, prefixed and separated.


Useful with `__format__`
-------------------------

Get fstring to process ``mark``

.. code:: python

    from psprint import psfmt

    class MyFmtClass():
        """My Test Class with format string"""
        def __init__(self):
            self.attr = 'data\ndata line 1\ndata line 2'

        def __repr__(self) -> str:
            return f'{self:info}'

        def __str__(self) -> str:
            return f'data: {self.attr!s}'

        def __format__(self, spec):
            fmt_out = []
            for line_no, line in enumerate(str(self).split("\n")):
                if line_no == 0:
                    fmt_out.extend(psfmt(line, mark=spec))
                else:
                    fmt_out.extend(psfmt(line, mark='cont'))
            return '\n'.join(fmt_out)


    if __name__ == "__main__":
        myobj = MyFmtClass()
        print(f'{myobj:list}')
        print(repr(myobj))


