=====
Usage
=====

Connect to a TM1 server
------------------------

.. code-block:: python

    from airflow_tm1.hooks.tm1 import TM1Hook

    tm1_hook = TM1Hook(conn_id="tm1_default")

    tm1 = tm1_hook.get_conn()


