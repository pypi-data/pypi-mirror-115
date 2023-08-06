import requests
from requests_toolbelt import MultipartEncoder
import json

# -*- coding: utf-8 -*-
# @Time    : 2021-08-04
# @Author  : yangfan
# @FileName: keyin_plm.py
# @Software: pycharm


plm_token = "eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJSKspPyi9R0lEqLU4tCsrPSQUKBfn7uMY7uvh6-g" \
            "HFUysKlKwMzYwszAxNTIzMawGeVH5POAAAAA.QPh5zX8uBRYjxdWJ13BIsn3MTjcQ3LRz-7EShsL7lh6jIYXR1ZNxlcPdnm" \
            "sqNRNPV7bkB8t-5W-NdtqqvGfgaw"


class PublishBuild:
    def __init__(self, ip, port):
        r""" 发布Build

        :param ip: PLM 服务器ip
        :param port: PLM 服务器port
        """
        self.ip = ip
        self.port = port

    def publish_build(self, product_id: str, project_id: str, version_name: str, scm_path: str, desc: str,
                      zip_file_path: str, file_name: str) -> dict:
        r"""发布build记录

        :param product_id: 项目ID
        :param project_id: 迭代ID
        :param version_name: 版本号
        :param scm_path: 源码地址
        :param desc: 描述信息
        :param zip_file_path: 压缩文件路劲
        :param file_name: 文件名
        :return: 新建build对象
        """
        url = f'http://{self.ip}:{self.port}/plm/build/create'
        data = MultipartEncoder({
            'product': product_id,
            'branch': '0',
            'project': project_id,
            'name': version_name,
            'scmPath': scm_path,
            'desc': desc,
            'file': (file_name, open(zip_file_path, 'rb'), 'application/octet-stream'),
        })
        headers = {
            "Content-Type": data.content_type,
            "token": plm_token
        }
        res = requests.post(url, data=data, headers=headers, verify=False)
        if res.status_code != 200:
            raise Exception("response error !", res.status_code)
        json_res = json.loads(res.text)
        print(json_res)
        if json_res['code'] != 0:
            raise Exception("response error !", json.dumps(json_res))
        return json_res


class PublishRelease:
    def __init__(self, ip, port):
        r""" 推送Release

        :param ip: PLM 服务器ip
        :param port: PLM 服务器port
        """
        self.ip = ip
        self.port = port

    def publish_release(self, git_project_id: str, commit_hash: str, product: str, build: str,
                        name: str, desc: str) -> dict:
        r"""发布Release

        :param git_project_id: gitLab 项目ID
        :param commit_hash: commit Hash
        :param product: zentao 项目ID
        :param build: zentao build id
        :param name: release 版本号
        :param desc: 描述信息
        :return:
        """
        url = f'http://{self.ip}:{self.port}/plm/release/create'
        form_data = {
            'gitProjectId': git_project_id,
            'commitHas': commit_hash,
            'product': product,
            'branch': '0',
            'build': build,
            'name': name,
            'desc': desc
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "token": plm_token
        }
        res = requests.post(url, data=form_data, headers=headers, verify=False)
        if res.status_code != 200:
            raise Exception("response error !", res.status_code)
        json_res = json.loads(res.text)
        if json_res['code'] != 0:
            raise Exception("response error !", json.dumps(json_res))
        return json_res

    def publish_release_build(self, git_project_id: str, commit_hash: str, product: str, project_id: str, scm_path: str,
                        name: str, desc: str, zip_file_path: str, file_name: str) -> dict:
        r"""自动提交build 然后发布Release

        :param git_project_id:  gitLab 项目ID
        :param commit_hash: gitLab 项目ID
        :param product: zentao 项目ID
        :param project_id: zentao 迭代ID
        :param scm_path:  源码地址
        :param name:  build && release 版本号
        :param desc: 描述信息
        :param zip_file_path: 压缩文件
        :param file_name:  文件名
        :return: release 对象
        """
        pb = PublishBuild(self.ip, self.port)
        pb_res = pb.publish_build(product, project_id, name, scm_path, desc, zip_file_path, file_name)
        build_id = pb_res['data']['id']
        return self.publish_release(git_project_id, commit_hash, product, build_id, name, desc)


class ZentaoProject:
    def __init__(self, ip, port):
        r""" 禅道项目迭代信息

        :param ip: PLM 服务器ip
        :param port: PLM 服务器port
        """
        self.ip = ip
        self.port = port

    def list_project(self, product: str) -> dict:
        r"""获取项目的所有迭代信息

        :param product: 项目ID
        :return: 迭代信息 array
        """
        url = f'http://{self.ip}:{self.port}/plm/project/{product}/list'
        headers = {
            "token": plm_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("response error !", response.status_code)
        json_res = json.loads(response.text)
        if json_res['code'] != 0:
            raise Exception("response error !", json.dumps(json_res))
        return json_res





