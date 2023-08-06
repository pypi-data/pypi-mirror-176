#######
Install
#######

You can install nspyre from `conda-forge <https://conda-forge.org/docs/>`_:

.. code-block:: bash
   
   $ conda install -c conda-forge nspyre

or PyPI:

.. code-block:: bash

   $ pip install nspyre

Conda Basics
============

If you do not already have conda installed, we recommend using the Miniconda distribution (instead of the Anaconda distribution) because it contains fewer default packages, many of which are unnecessary for the vast majority of users. The latest release of Miniconda for your platform is available here: `Miniconda installers <https://docs.conda.io/en/latest/miniconda.html>`__. The default installation options are appropriate for most users.

Once conda is installed, you'll want to add the conda-forge channel as a repository and update conda with the latest packages from conda-forge:

.. code-block:: bash

   $ conda activate
   (base) $ conda config --add channels conda-forge
   (base) $ conda config --show channels
   channels:
     - conda-forge
     - defaults
   (base) $ conda update -n base conda

Notice that you now have two channels from which conda will search for packages: *conda-forge* and *defaults*. The channels are listed in order of priority - conda will search the first repository when updating or installing a package unless explicitly told otherwise. The *defaults* channel is the one conda is bundled with and from which the initial set of packages are installed; this is the *Anaconda* channel for their managed repository of curated packages. However, this is non-exhaustive and *conda-forge* is an open-source alternative of community maintained packages (and the channel on which nspyre is published). Running the update command above reinstalls the core packages from conda-forge. You can confirm this by running the following:

.. code-block:: bash

   (base) $ conda list
   # packages in environment at /path/to/base/env/miniconda3:
   #
   # Name                    Version                   Build    Channel
   anaconda-client           1.7.2                      py_0    conda-forge
   anaconda-project          0.8.3                      py_0    conda-forge
   attrs                     20.2.0             pyh9f0ad1d_0    conda-forge
   beautifulsoup4            4.9.2                      py_0    conda-forge
   ...
   zipp                      3.2.0                      py_0    conda-forge
   zlib                      1.2.11            h7795811_1009    conda-forge
   zstd                      1.4.5                h289c70a_2    conda-forge

You will see that everything is installed from *conda-forge*. It is desirable to have all the packages come from the same repository due to compiling complexities, ABI compatibility, and consistent build environments (beyond the scope of discussion).

Once you have conda itself installed, create and activate a new conda environment for running nspyre:

.. code-block:: bash

   (base) $ conda env create --name my-env
   (base) $ conda activate my-env

Whenever creating a new conda environment, we recommend that you first install pip to the environment:

.. code-block:: bash

   (my-env) $ conda install pip

This ensures that any future calls to ``pip`` will install packages to your conda environment, rather than the system installation (which would defeat the purpose of conda). You may need to restart your terminal application for this to take effect. To confirm that ``pip`` will be called from your conda environment, you can run ``which pip`` on \*nix (Mac, Linux), or ``where pip`` on Windows to reveal its location. The location should be ``.../miniconda3/envs/<your_env>/bin/pip`` and NOT ``.../miniconda3/bin/pip`` or, e.g., ``/usr/bin/pip``.

Finally, install nspyre:

.. code-block:: bash

   (my-env) $ conda install nspyre
