MYSTRAN validation
==================


![pypi](https://img.shields.io/pypi/v/mystran_validation.svg "https://pypi.python.org/pypi/mystran_validation")


Python framework for [MYSTRAN](http://https://github.com/dr-bill-c/MYSTRAN) validation.


* Free software: MIT license

[[_TOC_]]

Features
--------

* [declarative framework](#a-declarative-framework)
* [flexible](#a-flexible-framework)
* built on top of [pytest](https://pytest.org/), [femap-neutral-parser](https://pypi.org/project/femap-neutral-parser/) and [PyNastran](https://pypi.org/project/pyNastran/).
* tests-results are summarized within a [JUnitXML](https://junit.org/junit5/docs/current/user-guide) file, therefore compatible with Jenkins/Travis or other CI tools.
* Automatic reporting based on the JUnitXML file based on [junit2html](https://pypi.org/project/junit2html) 

Limitations
-----------

* for now, only [a few vectors](#vectors) are implemented 
* Mystran results are based on `.NEU` result file, therefore, somewhere limited with available results. Plan is to migrate to OP2 parsing once it will have been developped.


Vectors
-------

Currently implemented vectors:

- [x] Displacements (3 translations, 3 rotations)
- [x] Reactions (6-dof reactions)
- [x] CBAR internal forces
- [x] CBUSH internal forces

Next in the pipe:

- [ ] CQUAD4 internal forces
- [ ] CTRIA3 internal forces

A declarative Framework
-----------------------

`mystran_validation` is a python **declarative** framework dedicated to MYSTRAN test cases.

**declarative** means that end-user do not need to know python **at-all**. Test cases are declared as `ini` text files, pointing to relevant files, and describing the test itself.

Example::

        [DEFAULT]
        title = test 00
        bulk = bulk_model.nas
        reference = test_case_03.op2
        
        [Checking Displs]
        # we check all nodes displacements
        description = check all displacements
        vector = displacements

        [Reactions]
        # we check all nodes displacements
        description = this is a multi-lines
        	description
        vector = reactions

The above configuration file describes **two tests** performed on ``bulk_model.nas`` (named "Checking Displs"). This test will check **all displacements** and **all ractions** against ``test_case_03.op2`` file. 


A flexible framework
--------------------

Event though [many limitations] still remain, the framework features:

### tolerance management

The above example may be tweaked as follows::

     [...]
     
     [Displacements]
     # we check all nodes displacements
     description = check all displacements
     vector = displacements
     ## we can reduce / increase tolerance
     rtol = 1e-05 # default relative tolerance
     atol = 1e-08 # default absolute tolerance 

### checking data subset

Data subset can be checked by specifying `gids`, `SubcaseIDs`::

     [...]
     
     [Displacements]
     # we check all nodes displacements
     description = check all displacements
     vector = displacements
     ## we can restrict checked data:
     gids = 1, 2
     SubcaseIDs = 1,2

### Manual references

Beside reference results file, one can specify a value *by-hand* as follows::

        [Displacements II]
        description = Check one single value
        vector = displacements
        ## restrict check to MYSTRAN subset:
        gids = 1
        SubcaseIDs = 2
        axis = 6
        reference = 0.00513
        atol = 1e-06 
        



  


