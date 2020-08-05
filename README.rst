========================
ECF grades database
========================

* Django project - python>=3.5, PostgreSQL>=10

* Use ``setenv_example`` as a template to set relevant environment variables

* Contains routines to import grading lists from the ECF website (CSV files, freely available),
  and store the entries in a PostgreSQL database

* I wrote a Django management command to load a set of CSVs, but it's very slow
  - so as an alternative I've written a script which generates a PostgreSQL data dump
  for imports, in ``scripts/generate_pgload.py``. This can then be imported directly

* **TODO**: add statistics and graphs for selected players, also reports for
  timepoints/players etc.
