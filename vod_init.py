
import os
import configparser

from volcengine.vod.VodService import VodService

def init_vod_service(region='cn-north-1'):
    config_path = os.path.join(os.path.expanduser("~"), ".volc", "config")
    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        exit(1)
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)
    # 从配置文件中获取 AK 和 SK
    ak = config.get('default', 'ak')
    sk = config.get('default', 'sk')

    vod_service = VodService(region=region)
    vod_service.set_ak(ak)
    vod_service.set_sk(sk)
    return vod_service

if __name__ == '__main__':
    init_vod_service()
    print('接口配置成功!')
