        usage: bcrawl [-h] -n NUM -k KEYWORD -d DEST [--xshear XSHEAR [XSHEAR ...]]
                    [--yshear YSHEAR [YSHEAR ...]] [--rotate ROTATE [ROTATE ...]]
                    [--flip FLIP] [--zoom ZOOM [ZOOM ...]]
                    [--resize RESIZE [RESIZE ...]]

        optional arguments:
        -h, --help            show this help message and exit
        -n NUM, --number NUM  Number of images
        -k KEYWORD, --keyword KEYWORD
                                Keyword
        -d DEST, --dest DEST  Destination folder
        --xshear XSHEAR [XSHEAR ...]
                                xshear range
        --yshear YSHEAR [YSHEAR ...]
                                yshear range
        --rotate ROTATE [ROTATE ...]
                                rotate range
        --flip FLIP           flip
        --zoom ZOOM [ZOOM ...]
                                zoom range
        --resize RESIZE [RESIZE ...]
                                Resize

        Example: bcrawl -n 100 -k 'dogs' -d './dogs' --xshear -2 2 --yshear -2 2 --rotate -60 60 --flip True --zoom 0.5 1.5 --resize 300 300