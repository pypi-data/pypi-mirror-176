import json
import os.path

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
        self.addr = "http://" + host + ":" + port

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
