Unreleased changes
------------------


Version 0
---------
0.4.2 / 2021-08-06
~~~~~~~~~~~~~~~~~~
* Default parameters for ``oscillationprobabilities`` updated

0.4.1 / 2021-05-05
~~~~~~~~~~~~~~~~~~
* Hotfix

0.4.0 / 2021-05-05
~~~~~~~~~~~~~~~~~~
* Remove template artifacts
* Add the ability to configure servers
* ``km3services.oscprob`` now holds the class ``OscProb`` which has to be used
  to access the ``oscillationprobablities``, see the ``README.md`` for an
  updated example.

0.3.0 / 2020-11-05
~~~~~~~~~~~~~~~~~~
* OscProb ``oscillationsprobabilities`` now takes PDG IDs as input and also
  accepts scalars and arrays for each input (flavor in, flavour out, energies
  and cos_zeniths)

0.2.0 / 2020-10-29
~~~~~~~~~~~~~~~~~~
* First prototype of OscProb wrapper

0.1.0 / 2020-10-28
~~~~~~~~~~~~~~~~~~
* Project generated using the cookiecutter template from
  https://git.km3net.de/templates/python-project
