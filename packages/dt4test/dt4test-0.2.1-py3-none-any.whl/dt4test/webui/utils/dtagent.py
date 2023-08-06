# -*- utf-8 -*-
import os
import sys
import time
import json
import threading

from dt4test import network as nt
from dt4test import proc


class DtAgent():
    def __init__(self, cia_ip, cia_port, role_info):
        """

        :param cia_ip:
        :param cia_port:
        :param role_info:   role1:group1,role2:group2
        """
        self.server_host = "http://" + cia_ip + ":" + cia_port
        self.api_path = "/api/v1/cia/"

        self.log_size = 100
        self.log = []
        self.cur_idx = -1
        self.init_log()

        self.hb_interval = 3     # heart beat interval default is 3

        self.roles_info = role_info

        self.roles = []
        self.role_ids = []
        self.group_roles = []
        self.roles_str = ""
        self.get_roles()

    def init_log(self):
        for i in range(0, self.log_size):
            self.log.append('x')

    def get_roles(self):
        self.group_roles = self.roles_info.split(",")
        for s in self.group_roles:
            self.roles.append(s.split(':')[0])
        self.roles_str = ','.join(self.roles)

    def get_ids_str(self):
        return ','.join(self.role_ids)

    def put_command(self, target, cmd_type, cmd_arg):
        payload = {"method":"put_command", "cmd_type": cmd_type, "target":target, "cmd_arg":cmd_arg}
        res = nt.send_post_request(self.server_host, self.api_path, payload)
        if not res.status_code == 200:
            return {"status":"fail", "msg":"return code:{}".format(res.status_code),"cmd_id": "0"}
        body = json.loads(res.text)
        return body

    def get_command(self):
        info = self.get_info()
        role_ids = self.get_ids_str()
        payload = {"method":"get_command", "role_ids": role_ids, "info": info}
        res = nt.send_post_request(self.server_host, self.api_path, json=payload)
        if not res.status_code == 200:
            return {"status":"fail", "msg":"return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def get_info(self):
        return "TODO"

    def set_interval(self, sec):
        self.hb_interval = sec

    def get_interval(self):
        return self.hb_interval

    def put_result(self, payload):
        res = nt.send_post_request(self.server_host, self.api_path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def get_result(self, cmd_id):
        payload = {"method": "get_result", "cmd_id": cmd_id}
        res = nt.send_post_request(self.server_host, self.api_path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        return body

    def register(self, local_ip='unknown'):
        payload = {"method": "register", "group_roles": ','.join(self.group_roles), "ip": local_ip}
        res = nt.send_post_request(self.server_host, self.api_path, json=payload)
        if not res.status_code == 200:
            return {"status": "fail", "msg": "return code:{}".format(res.status_code)}
        body = json.loads(res.text)
        role_ids = body["role_ids"]
        self.role_ids = role_ids
        print("RegisterOK, role_ids: {}".format(self.role_ids))
        return body

    def is_registered(self):
        return True if len(self.role_ids) > 0 else False

    def add_log(self, info):
        self.cur_idx += 1
        if self.cur_idx < self.log_size:
            self.log[self.cur_idx] = str(self.cur_idx) + ": " + info
        else:
            self.cur_idx = -1
            self.add(info)

    def get_log(self, format='str'):
        if format == "str":
            info = ""
            head = self.cur_idx + 1
            while head < self.log_size:
                info += self.log[head] + "\n"
                head += 1

            head = 0
            while head <= self.cur_idx:
                info += self.log[head] + "\n"
                head += 1

            return info
        else:
            return self.log


class RunCommand(threading.Thread):
    def __init__(self, cmd):
        super(RunCommand,self).__init__()   #重构run函数必须写
        self.cmd = cmd

    def run(self):
        print('task',self.n)
        time.sleep(1)
        print("{} print".format(self.n))
        time.sleep(1)
        print("{} print".format(self.n))


class CommandRunner(threading.Thread):
    def __init__(self, agent):
        self.runner = proc
        self.agent = agent

    def run(self, cmd):
        print("Run CMD: {}".format(cmd))
        cmd_arg = cmd["cmd_arg"]
        result = self.runner.run_process(cmd_arg, shell=True)
        payload = {"method": "put_result",
                   "sub_id": cmd["sub_id"],
                   "role_id": cmd["role_id"],
                   "cmd_id": cmd["cmd_id"],
                   "ret_code": "{}".format(result.rc),
                   "out": "{}".format(result.stdout),
                   "err": "{}".format(result.stderr)}
        print("Put Result:{}".format(payload))
        self.agent.put_result(payload)



def show_usage():
    print(">>python dtagent.py cia_ip, cia_port, role_info")
    print(">>role_info format: role1:group1,role2:group2")


def get_local_ip():
    ip = os.environ.get("POD_IP", None)
    if not ip:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

    return ip


if __name__ == '__main__':
    if len(sys.argv) < 4:
        show_usage()
        exit(1)
    cia_ip = sys.argv[1]
    cia_port = sys.argv[2]
    role_info = sys.argv[3]
    agent = DtAgent(cia_ip, cia_port, role_info)
    interval = agent.get_interval()

    my_pid = os.getpid()
    print("Write pid file: /tmp/dtagant.pid ...")
    with open('/tmp/dtagent.pid', 'w') as pf:
        pf.write("{}".format(my_pid))

    while True:
        try:
            result = agent.register(get_local_ip())
            if agent.is_registered():
                print("Agent register Success:{}".format(result))
                break
            else:
                print("Agent register failed , try again later ...")
                agent.add_log("Register failed")
                time.sleep(interval)
        except Exception:
            print("Connection Error , try again later ...")
            time.sleep(interval)

    runner = CommandRunner(agent)

    while True:
        time.sleep(interval)
        print("{} : Get Cmd".format(time.time()))
        res = agent.get_command()
        cmds = res["cmds"]
        print("CMDS:{}".format(cmds))
        for cmd in cmds:
            agent.add_log("sent cmd :{}".format(cmd))
            runner.run(cmd)



