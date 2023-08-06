import os
from pathlib import Path
import shutil
import sys
import logging
import logging.config

import depthmap
import exporter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s: line %(lineno)d'))
logger.addHandler(handler)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logger.info('You did not enter depthmap_dir folder and calibration file path')
        logger.info('E.g.: python convertdepth2pcd.py depthmap_dir calibration file')
        sys.exit(1)

    depthmap_dir = sys.argv[1]
    calibration_file = sys.argv[2]

    depth_filenames = []
    for (dirpath, dirnames, filenames) in os.walk(depthmap_dir + '/depth'):
        depth_filenames.extend(filenames)
    depth_filenames.sort()
    try:
        shutil.rmtree('export')
    except BaseException:
        print('no previous data to delete')
    os.mkdir('export')
    for filename in depth_filenames:
        depthmap_dir = Path(depthmap_dir) / 'tests' / 'huawei_p40pro'
        dmap = depthmap.Depthmap.create_from_zip(depthmap_fpath=Path(depthmap_dir) / 'depth' / filename,
                                                 rgb_fpath=None,
                                                 calibration_fpath=calibration_file)
        output_filename = f'export/output{filename}.pcd'
        exporter.export_pcd(output_filename, dmap)

    logger.info('Data exported into folder export')
