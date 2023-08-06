# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   core.py
@Time    :   2022/10/26 17:17:15
@Author  :   Frank.Xu
"""
import os
import click
import shutil
import linecache
import subprocess
from .scripts.sync_repo import _sync
from .scripts.mapping import mapping
from .__version__ import __version__ as version

HERE = os.path.abspath(os.path.dirname(__file__))
OTA_FOLDER_PATH = "/home/ginger/grpc_ota_tmp"
GATEWAY_FILE_PATH = "/etc/network/interfaces"
DATA_SAVE_PATH = "/data/user/ginger/smart_world"



@click.group()
@click.version_option(version=version)
def sw():
    """ Tools Collection of SmartWorld.\n
    Documentation link: https://df54vg7fe0.feishu.cn/docx/EmajdGEJ2oqAArxzyxlcFJcznSb \n
    Usage: sw [command] --help"""


@click.command()
@click.option("-p", "--package", help="package path", prompt="Please input the path of OTA package",type=click.Path(exists=True))
def ota(package):
    """ Complete ota with the specified package.\n
    Usage: sw ota -p or --package """
    # if not os.path.exists(package):
    #     raise FileNotFoundError

    if not os.path.isfile(package):
        raise NotADirectoryError("package should be a file")

    if not os.path.exists(OTA_FOLDER_PATH):
        os.mkdir(OTA_FOLDER_PATH)
    
    shutil.copy(package, os.path.join(OTA_FOLDER_PATH, "ginger_lite-ota.zip"))
    os.system("cd {} && md5sum ginger_lite-ota.zip > md5.txt".format(OTA_FOLDER_PATH))
    os.system("roslaunch test_client test_client.launch")



def _switch_gateway():
    try:
        _type, gateway = linecache.getline(GATEWAY_FILE_PATH, 8).split()
    except ValueError:
        raise click.FileError("{}".format(GATEWAY_FILE_PATH))
    if not _type == "gateway":
        raise ValueError("The file has been modified, line 8 is no longer the gateway")

    if click.confirm('Current gateway is {}, do you want to continue?'.format(gateway)):
        subprocess.call("sudo python3 {}".format(os.path.join(HERE, "scripts/switch_gateway.py")), shell=True)

@click.command()
def sg():
    """ Short for switch-gateway. \n 
    Usage: sw sg """
    _switch_gateway()

@click.command()
def switch_gateway():
    """ Switch the gateway from 192.168.137.200 to 192.168.137.1 or from 192.168.137.1 to 192.168.137.200. \n
        Usage: sw switch-gateway
    """
    _switch_gateway()

@click.command()
@click.option("-t","--to",help="save path",prompt="Please input the path")
def clone(to):
    """  Clone code to the specified path.\n
    Usage: sw clone -t or --to """
    _sync(save_path=to)
    
@click.command()
@click.option("-p", "--path", help="output path",default=DATA_SAVE_PATH)
def vrecord(path):
    """ Record vslam data. \n
    Usage: sw vrecord  or use the -p parameter to specify the save path, the default is /data/user/ginger/smart_world.

    """
    if not os.path.exists(path):
        os.makedirs(path)
    os.system("rosbag record -o {}/vslam \
        /camera/camera_info \
        /camera/image_raw \
        /camera/imu \
        /camera/infra1/camera_info \
        /camera/infra1/image_rect_raw \
        /camera/infra2/camera_info \
        /camera/infra2/image_rect_raw \
        /hd_map_init_pose \
        /imu/data \
        /occ_map \
        /odom \
        /scan \
        /tf \
        /tf_static \
        ".format(path))
 
@click.command()
@click.option("-p", "--path", help="output path",default=os.path.join(DATA_SAVE_PATH,"depth_detect"))
def drecord(path):
    """ Record depth_detect data. \n 
    Usage: sw drecord or use the -p parameter to specify the save path, the default is /data/user/ginger/smart_world/depth_detect.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    os.system("rosbag record -o {} \
        /camera/depth/camera_info \
        /camera/depth/image_rect_raw \
        /camera/infra1/image_rect_raw \
        /odom \
        /scan \
        /Ultrasonic \
        /VisualDrop \
        /VisualDropSwitch \
        /special_areas \
        /tf \
        /tf_static \
        ".format(path))
 



sw.add_command(ota)
sw.add_command(switch_gateway)
sw.add_command(mapping)
sw.add_command(clone)
sw.add_command(sg)
sw.add_command(vrecord)
sw.add_command(drecord)
