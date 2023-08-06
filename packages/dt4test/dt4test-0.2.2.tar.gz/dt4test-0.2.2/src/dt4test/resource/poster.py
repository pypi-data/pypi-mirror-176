import json
import os.path
import requests
from urllib3 import encode_multipart_formdata

from ..lib.network import Network as nt
from ..lib.helper import Helper
from ..lib.logger import Logger


log = Logger().get_logger(__name__)


def show_cli_help():
    """
    显示 客户端帮助
    """
    print(">> poster master|slave|role :显示所有role的信息")
    print(">> poster master|slave|role[1] cmd \"command\" :远程执行命令")
    print(">> poster master|slave|role[1] fcmd command_file :远程执行脚本")
    print(">> poster role ufile here.txt there.txt :按role发送文件")
    print(">> poster role dfile file_path des_dir : 拉取role上的文件到本地")
    print(">> poster : 显示topology信息")


class Poster(Helper):
    """
    Poster for cia
    """
    def __init__(self, host="127.0.0.1", port="8081"):
        self.host = host
        self.port = port
        self.path = "/api/v1/cia/"
        self.file_path = "/api/v1/cia_file"
        self.addr = "http://" + host + ":" + port

        self.role_ids = []
        self.group_roles = ["poster"]

    def init(self, conf_file):
        """
        For cli invoker, using conf_file to init host,port
        :param conf_file: Should be like 12.12.12.12:8081
        :return: None
        """
        if not os.path.exists(conf_file):
            log.error("找不到配置文件:".format(conf_file))
            log.error("配置文件格式:   ip:port ".format(conf_file))
            exit(1)

        # TODO: Add try-except for ValueError
        with open(conf_file, 'r') as cf:
            line = cf.readline().strip()
            self.host, self.port = line.split(":")

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_api_path(self):
        return self.path

    def get_file_api_path(self):
        return self.file_path

    def get_addr(self):
        return self.addr

    def get_role_ids(self):
        return self.role_ids

    def register(self):
        payload = {"method": "register", "group_roles": ','.join(self.group_roles), "ip": nt.get_local_ip()}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        role_ids = body["role_ids"]
        self.role_ids = role_ids
        log.info("RegisterOK, role_ids: {}".format(self.role_ids))
        return body

    def get_env(self):
        payload = {"method": "get_env"}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def get_targets(self, target: str):
        payload = {"method": "get_target", "target": target}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def put_command(self, cmd_type, target, cmd_arg):
        payload = {"method":"put_command", "cmd_type": cmd_type, "target": target, "cmd_arg": cmd_arg}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status":"fail", "msg":"return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def send_command(self, cmd_type, target, cmd_arg):
        return self.put_command(cmd_type, target, cmd_arg)

    def get_result(self, cmd_id):
        payload = {"method":"get_result", "cmd_id": cmd_id}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status":"fail", "msg":"return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def drop_command(self, cmd_id):
        payload = {"method": "drop_command", "cmd_id": cmd_id}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def clear_commands(self):
        payload = {"method": "clear_commands"}
        res = nt.send_post_request(self.addr, self.path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def upload_file(self, target, local_file, des_path):
        file_path, file_name = os.path.split(local_file)
        payload = {"method": "get_result", "data": "some data"}
        with open(local_file, 'rb') as f:
            file = {
                    "files": (file_name, f.read()),
                    "method": "upload_c",
                    "target": target,
                    "des_path": des_path
                    }
            encode_data = encode_multipart_formdata(file)
            file_data = encode_data[0]
            header = {"Content-Type": encode_data[1]}
            res = requests.post(self.addr+self.path, headers=header, data=file_data, json=payload)

        if not res.status_code == 201:
            return {"status":"fail", "msg":"return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def download_file(self, file_path, local_path):
        """
        通用下载方法，下载文件
        Download from: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        :param file_path:
        :param local_path:
        :param target:
        :return:
        """

        file_dir, file_name = os.path.split(local_path)
        # NOTE the stream=True parameter below
        file = {
            "files": ("my_name", "x"),
            "method": "download",
            "des_path": file_path
        }
        encode_data = encode_multipart_formdata(file)
        file_data = encode_data[0]
        header = {"Content-Type": encode_data[1]}

        try:
            with requests.post(self.addr + self.path, headers=header, data=file_data, stream=True) as r:
                r.raise_for_status()
                file_dir, file_name = os.path.split(local_path)
                os.makedirs(file_dir)
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        f.write(chunk)
        except Exception as e:
            log.error("Down load File Fail:{}".format(e))
            return "failed"
        return local_path

    def download_command_file(self, cmd_id, local_path):
        """
        通用下载方法，下载文件
        Download from: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
        :param file_path:
        :param local_path:
        :param target:
        :param cmd_id:
        :return:
        """

        file, ext = os.path.splitext(local_path)
        if not ext == "zip":
            log.error("{} 必须已zip结尾".format(local_path))
            return ""

        # NOTE the stream=True parameter below
        file = {
            "files": ("my_name", "x"),
            "method": "download_c",
            "target": "",
            "cmd_id": cmd_id
        }
        encode_data = encode_multipart_formdata(file)
        file_data = encode_data[0]
        header = {"Content-Type": encode_data[1]}

        try:
            with requests.post(self.addr + self.path, headers=header, data=file_data, stream=True) as r:
                r.raise_for_status()
                file_dir, file_name = os.path.split(local_path)
                os.makedirs(file_dir) if not os.path.exists(file_dir) else None
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        f.write(chunk)
        except Exception as e:
            log.error("Down load File Fail:{}".format(e))
            return "failed"
        return local_path

    def cli(self, argv: []):
        """
        客户端接口程序
        """
        log.info("Argv: {}".format(','.join(argv)))
        if len(argv) == 2:
            show_cli_help()
            return 0

        if len(argv) == 5 and argv[3] == 'cmd':     # poster master|slave|role cmd|fcmd|ufile|dfile command_args
            return self.put_command('cmd', argv[2], argv[4])

        if len(argv) == 4 and argv[1:] == ['env', 'create', 'user']:
            print("无法解析的参数：{}".format(argv))

        if len(argv) == 4 and argv[1:] == ['env', 'delete', 'user']:
            print("无法解析的参数：{}".format(argv))
        if len(argv) == 4 and argv[1] == 'ssh':   # ssh master|slave|role[1] \"command\" :远程执行命令
            print("无法解析的参数：{}".format(argv))
        if len(argv) == 4 and argv[1] == 'sshf':  # sshf master|slave|role[1] command_file :远程执行脚本
            print("无法解析的参数：{}".format(argv))

        if len(argv) == 5 and argv[1] == 'get':   # get role file_path des_dir: 拉取role上的文件到本地
            print("无法解析的参数：{}".format(argv))
        if len(argv) == 5 and argv[1] in ['scp', 'put']:
            print("无法解析的参数：{}".format(argv))

        print("无法解析的参数：{}".format(argv))
        show_cli_help()
        return -1


if __name__ == "__main__":
    poster = Poster()
    # res = poster.get_env()
    # print(res)
    res = poster.put_command('cmd', 'role1', "sleep 2")
    print(res)
    id = res["cmd_id"]
    res = poster.get_result(id)

    # res = poster.upload_file('role1','/Users/mawentao/PycharmProjects/data-test/dt4test/src/dt4test/webui/utils/temp_up/1.sh', '/Users/mawentao/PycharmProjects/data-test/dt4test/src/dt4test/webui/utils/temp_down/s.sh')
    # print(res)

    # res = poster.put_command('ufile_a', 'role1', "/Users/mawentao/PycharmProjects/data-test/dt4test/src/dt4test/webui/utils/temp_up/1.sh")
    # print(res)

    # res = poster.download_command_file("1115205907_811", "/Users/mawentao/PycharmProjects/data-test/dt4test/src/dt4test/webui/utils/temp_down/x.zip")
    # print(res)