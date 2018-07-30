py3dtiles_merger
================

    **Disclaimer:**

    This project is under active development and has been created to generate data as fast as possible at Jakarto (rush time). It doesn't cover either unit test, well-written documentation, or a sufficient level of abstraction to be used in different contexts. However, I will be more than happy to remove this disclaimer when improvements will be done. Feel free to open an issue to help the project.

Convert `.las` files to `3dtiles` in batch using `py3dtiles <https://github.com/Oslandia/py3dtiles>`_.

You can then easily visualize your supersized `.las` files on the Internet thanks to 3d viewers like `Cesium <https://github.com/AnalyticalGraphicsInc/cesium>`_ or `Itowns <https://github.com/iTowns/itowns>`_.


Requirements
#############

This project needs a docker image of py3dtiles. Please follow the instructions :

    .. code-block:: shell

        $ git clone https://github.com/Tofull/py3dtiles
        $ cd py3dtiles
        $ git fetch && git checkout lasTo3dtiles  # Required until the PR is merged
        $ docker build -t py3dtiles .

Installation
#############

- Local installation *(recommanded until the project support pypi integration)*

    .. code-block:: shell

        git clone https://github.com/Tofull/py3dtiles_batcher
        cd py3dtiles_batcher
        pip install .


Usage
###########

    .. code-block:: shell

        usage: py3dtiles_batcher [-h] [--dryrun] [--incremental] [--srs_in SRS_IN]
                         [--srs_out SRS_OUT] [--cache_size CACHE_SIZE]
                         [--docker_image DOCKER_IMAGE] [--verbose]
                         output_folder [input_folder [input_folder ...]]

        Convert .las file to 3dtiles in batch.

        positional arguments:
        output_folder         Directory to save tiles.
        input_folder          Directory to watch. (default: .)

        optional arguments:
            -h, --help                  show this help message and exit
            --dryrun                    Active dryrun mode. No tile will be generated in this mode. (default: False)
            --incremental               Active incremental mode. Skip tile if <output_folder>/<tile>/tileset.json exists. (default: False)
            --srs_in SRS_IN             Srs in. (default: 2959)
            --srs_out SRS_OUT           Srs out. (default: 4978)
            --cache_size CACHE_SIZE     Cache size in MB. (default: 3135)
            --docker_image DOCKER_IMAGE py3dtiles docker image to use. (default: py3dtiles)
            --verbose, -v               Verbosity (-v simple info, -vv more info, -vvv spawn info) (default: 0)

        Working example (remove --dryrun when you want to generate tiles) :
        py3dtiles_batcher.exe "D:\data_py3dtiles\output" "D:\data_py3dtiles\raw" --dryrun -v


Examples
##########


If you want to convert all `.las` from "D:\data_py3dtiles\raw" directory and save result into "D:\data_py3dtiles\output":

    .. code-block:: shell

        # On windows
        py3dtiles_batcher.exe -v "D:\data_py3dtiles\output" "D:\data_py3dtiles\raw"


You can select specific files or folder you want to convert:

    .. code-block:: shell

        # On windows
        py3dtiles_batcher.exe -v "D:\data_py3dtiles\output" "D:\data_py3dtiles\raw" "D:\folder1\file1.las" "D:\folder2"


Notes :
#############

- Think to specify the `srs_in` option if its differs from EPSG:2959

- output path will be written in base64 encodage, to respect URL’s standard (which will be useful for 3d webviewer [Read What's next section]). Don't be surprised.


What's next ?
##############

* Visualize 3dtiles individually

    Once yours `.las` files have been converted into 3dtiles, you can expose them individually over the Internet with any http server, like :

        .. code-block:: shell

            # using https://www.npmjs.com/package/http-server
            npm install http-server -g
            http-server D:\data_py3dtiles\output --cors -p 8080

    Then, each tileset in subfolder is available over the Internet, and you can visualize it one by one using a 3d viewer, for example Cesium sandcastle : 

    1. Go to https://cesiumjs.org/Cesium/Build/Apps/Sandcastle/index.html
    2. Insert the following code on Javascript Code section. Replace <base64_name> by the name of the directory of the tileset.json you want to visualize.

        .. code-block:: javascript
        
            var viewer = new Cesium.Viewer('cesiumContainer');
            var tileset = viewer.scene.primitives.add(new Cesium.Cesium3DTileset({
                url : 'http://127.0.0.1:8080/<base64_name>/tileset.json'
            }));

    3. Click Run (or F8) and enjoy.

        .. image:: doc/assets/example_3dtiles_on_cesium.png
            :width: 200px
            :align: center
            :height: 100px
            :alt: Example on cesium

* Visualize merged 3dtiles

    If you want to visualize all your 3dtiles at the same time, some steps are required to merge them into one tileset.json.
    Hopefully, I created the merger tool. Please refer to it by clicking on the following link : https://github.com/Tofull/py3dtiles_merger

Contribution
#############

Contributions are welcome. Feel free to open an issue for a question, a remark, a typo, a bugfix or a wanted feature.



Licence
##########

Copyright © 2018 Loïc Messal (@Tofull) and contributors

Distributed under the MIT Licence.