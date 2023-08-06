# -*- coding: utf-8 -*-
__auther__ = "mawentao119@gmail.com"

import random

"""
Recieve commands and dispatch commands to roles
"""

from flask import current_app, session
from flask_restful import Resource, reqparse
import os
import time
from utils.mylogger import getlogger
import multiprocessing

from utils.file import remove_dir, get_splitext
from utils.run import robot_run, is_run, is_full, stop_robot, robot_debugrun, py_debugrun,bzt_debugrun, api_rf
from utils.pytester import debug_pytest_run, pytest_run, api_pytest

class Cia(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('method', type=str)
        self.parser.add_argument('group_roles', type=str)
        self.parser.add_argument('ip', type=str)
        self.parser.add_argument('role_ids', type=str)
        self.parser.add_argument('info', type=str)
        self.parser.add_argument('cmd_type', type=str)
        self.parser.add_argument('target', type=str)
        self.parser.add_argument('cmd_arg', type=str)
        self.parser.add_argument('sub_id', type=str)
        self.parser.add_argument('role_id', type=str)
        self.parser.add_argument('cmd_id', type=str)
        self.parser.add_argument('ret_code', type=str)
        self.parser.add_argument('out', type=str)
        self.parser.add_argument('err', type=str)

        self.log = getlogger(__name__)
        self.app = current_app._get_current_object()
        
        self.topology = self.app.config["TOPOLOGY"]
        self.commands = self.app.config["COMMANDS"]
        self.subcommands = self.app.config["SUBCOMMANDS"]
        self.command_types = self.app.config["COMMAND_TYPES"]
        self.interval = self.app.config["AGENT_INTERVAL"]

    def post(self):
        args = self.parser.parse_args()
        self.log.debug("Request args:{}".format(args))

        if args["method"] == "register":
            return self.register(args)
        elif args["method"] == "get_env":
            return self.get_env(args)
        elif args["method"] == "get_target" or args["method"] == "get_role":
            return self.get_targets(args)
        elif args["method"] == "get_command":
            return self.get_command(args)
        elif args["method"] == "put_command":
            return self.put_command(args)
        elif args["method"] == "get_result":
            return self.get_result(args)
        elif args["method"] == "put_result":
            return self.put_result(args)
        elif args["method"] == "drop_command" or args["method"] == "delete_command" or args["method"] == "rm_command":
            return self.drop_command(args)
        elif args["method"] == "clear_command":
            return self.clear_command(args)
        elif args["method"] == "get_command_list":
            return self.get_command_list(args)
        else:
            self.log.error("不支持的操作 'method' :{}".format(args['method']))
            return {"status": "fail", "msg": "不支持的操作 'method' :{}".format(args['method'])}

    def register(self, args):
        roles = args["group_roles"].split(',')
        ip = args["ip"]
        role_ids = []
        for item in roles:
            tmp = item.split(':')
            role = tmp[0]
            if len(tmp) > 1 :
                group = tmp[1]
            else:
                group = "unknown"
            role_id = self._add_to_topology(role, group, ip)
            role_ids.append(role_id)
        ids = ",".join(role_ids)
        self.log.info("注册成功 {}:{}".format(ip,ids))
        return {"status": "success", "msg": "OK", "role_ids": role_ids}

    def _add_to_topology(self, role, group, ip):
        """
        增加角色，topology 当前考虑一台机器上可以起多个role（docker情况），一个client可以归属多个role（1机多组件情况）
        :param role:
        :param group:
        :param ip:
        :return:
        """
        rnd = random.randint(100, 999)
        role_id = role + "_" + ip + "_" + str(1000 + rnd)
        new_role = {"role_id": role_id, "ip": ip, "role": role, "group": group, "report": 0.0, "is_alive": True}

        roles = self.topology.get(role, None)
        if roles:
            # for item in roles:
            #     count += 1
            #     if item["ip"] == ip:
            #         role_id = item["role_id"]
            #         item["is_alive"] = True
            #         self.log.info("角色ip存在:{}".format(ip))
            #         return role_id

            roles.append(new_role)
            self.log.info("追加新角色: {}:{}".format(role_id, ip))
            return role_id

        self.topology[role] = [new_role]
        self.log.info("创建新角色: {}:{}".format(role_id, ip))
        return role_id

    def _get_targets(self, target):
        """
        取得 target 所指代的 role ids
        :param target:
        :return:
        """
        role = target
        index = -1
        if target.find('[') != -1:
            role, left = target.split('[')
            index = int(left.split(']')[0])

        role_ids = []
        dead_roles = []
        roles = self.topology.get(role, [])
        if len(roles) > 0:
            now = time.time()
            timeout = 2 * self.interval
            for item in roles:
                if now - item["report"] < timeout:
                    role_ids.append(item["role_id"])
                else:
                    self.log.warn("超时的角色:{}".format(item["role_id"]))
                    item["is_alive"] = False
                    dead_roles.append(item)

            # 删除超时的角色
            for i in dead_roles:
                self.log.info("删除超时角色: {}".format(i))
                roles.remove(i)

        if index >= 0:
            if len(role_ids) > index:
                return [role_ids[index]]
            else:
                return []
        else:
            return role_ids

    def _gen_command_id(self):
        pre_fix = time.strftime("%m%d%H%M%S_", time.localtime(time.time()))
        cmd_id = random.randint(101, 999)
        return pre_fix + str(cmd_id)

    def _add_command(self, target, num_jobs, cmd_type, cmd_arg):
        """
        需要带 拆分的任务数 避免删除的维护
        :param target:
        :param num_jobs:
        :param cmd_type:
        :param cmd_arg:
        :return:
        """
        cmd_id = self._gen_command_id()
        cmd = {"target": target,
               "cmd_type":cmd_type,
               "cmd_arg": cmd_arg,
               "num_jobs": num_jobs,
               "time": time.time(),
               "last_report": 0.0,
               "result": []}
        self.commands[cmd_id] = cmd
        self.log.info("Add Cmd: {}:{}".format(cmd_id, cmd))
        return cmd_id

    def _drop_command(self, cmd_id):
        cmd = self.commands.get(cmd_id)
        if cmd:
            self.commands.pop(cmd)

        return True

    def _add_subcommand(self, role_id, cmd):
        role_cmds = self.subcommands.get(role_id, None)
        if role_cmds:
            role_cmds.append(cmd)
            self.log.info("ADD Subcmd: {}:{}".format(cmd["sub_id"], role_id))
        else:
            self.subcommands[role_id] = [cmd]

        return role_id

    def _drop_subcommand(self, cmd_id):
        """
        删除某个任务的运行，对于没有下发的子任务
        :param cmd_id:
        :return:
        """
        for role_id in self.subcommands:
            cmds = self.commands.get(role_id)
            deletes = []
            for c in cmds:
                if c["cmd_id"] == cmd_id:
                    deletes.append(c)
            for d in deletes:
                self.log.info("Delete subcommand: {}".format(d["sub_id"]))
                cmds.remove(d)

        return True

    def _get_subcommand(self, role_ids):
        cmds = []
        for rid in role_ids:
            if self.subcommands.get(rid, None):
                role_jobs = self.subcommands.pop(rid)
                for job in role_jobs:
                    cmds.append(job)

        return cmds

    def get_targets(self, args):
        """
        返回操作目标的id列表
        return: [id1,id2]
        """
        role_ids = self._get_targets(args["target"])
        if len(role_ids) > 0:
            ids = ','.join(role_ids)
            return {"status": "success", "msg": "OK", "node_ids": ids}
        else:
            return {"status": "fail", "msg": "Cannot find role", "node_ids": ""}

    def drop_command(self, args):
        cmd_id = args["cmd_id"]
        result1 = self._delete_command(cmd_id)
        result2 = self._delete_subcommand(cmd_id)
        if result1 and result2:
            return {"status": "success", "msg": "drop command {} OK".format(cmd_id)}
        else:
            return {"status": "fail", "msg": "drop command {} fail, Please see log".format(cmd_id)}

    def clear_command(self, args):
        self.log.info("清除Commands")
        self.commands.clear()
        return {"status": "success", "msg": "Clear commands ok", "data": self.commands}

    def get_command_list(self, args):
        cmds = []
        for cmd in self.commands:
            item = {"cmd_id": cmd["cmd_id"], "target": cmd["target"], "cmd_arg": cmd["cmd_arg"]}
            cmds.append(item)

        return {"status": "success", "msg": "get commands ok", "data": cmds}

    def put_command(self, args):
        """
        Client 提交的任务请求
        :param args:
        :return:
        """
        target = args["target"]
        cmd_type = args["cmd_type"]
        cmd_arg = args["cmd_arg"]

        role_ids = self._get_targets(target)
        if len(role_ids) == 0:
            return {"status": "fail", "msg": "Cannot find role", "cmd_id": ""}

        if not cmd_type in self.command_types:
            return {"status": "fail", "msg": "cmd_type no in:{}".format(self.command_types), "cmd_id": ""}

        num_jobs = len(role_ids)

        cmd_id = self._add_command(target, num_jobs, cmd_type, cmd_arg)

        for idx, rd in enumerate(role_ids):
            sub_id = cmd_id + "_" + str(idx)
            sub_cmd = {"sub_id": sub_id, "cmd_type": cmd_type, "cmd_arg": cmd_arg, "cmd_id": cmd_id, "role_id": rd}
            self._add_subcommand(rd, sub_cmd)

        return {"status": "success", "msg": "Put command success", "cmd_id": cmd_id}

    def get_command(self, args):
        """
        Agent 的心跳，通过心跳返回带回需要执行的命令，可以携带 info 参数，后续扩展
        :param args:
        :return:
        """
        ids = args["role_ids"].split(',')

        for rd in ids:
            self.update_role_status(rd)

        cmds = self._get_subcommand(ids)

        return {"status": "success", "msg": "Get command success", "cmds": cmds}

    def update_role_status(self, role_id):
        """
        更新role的status
        :param role_id: role_xx.xx.xx.xx_index
        :return:
        """
        role = role_id.split('_')[0]
        roles = self.topology.get(role)
        if roles:
            for r in roles:
                if r["role_id"] == role_id:
                    r["report"] = time.time()
                    r["is_alive"] = True
                    self.log.debug("Agent更新状态 {}".format(role_id))
                    break
        else:
            self.log.error("Agent更新状态，找不到角色: {}".format(role_id))

    def put_result(self, args):
        """
        Agent 上报任务运行结果
        :param args:
        :return:
        """
        sub_id = args["sub_id"]
        cmd_id = args["cmd_id"]
        role_id = args["role_id"]
        ret_code = args["ret_code"]
        out = args["out"]
        err = args["err"]

        result = { "sub_id": sub_id,
                   "role_id": role_id,
                   "ret_code": ret_code,
                   "out": out,
                   "err": err,
                   "time": time.time()}

        if self._put_result(cmd_id, result):
            return {"status": "success", "msg": "Put result success"}
        else:
            return {"status": "fail", "msg": "Put result failed"}

    def _put_result(self, cmd_id, result):
        cmd = self.commands.get(cmd_id, None)
        if cmd:
            cmd["result"].append(result)
            cmd["last_report"] = result["time"]
            self.log.info("Get Result: {}:{}".format(result["sub_id"], result["role_id"]))
            return True
        else:
            self.log.error("找不到任务: {}".format(cmd_id))
            return False

    def get_result(self, args):
        """
        返回任务结果，暂时实现实时返回，后续支持 timeout 的服务端重试
        :param args:
        :return:
        """
        if args.get("timeout", None):
            return {"status": "fail", "msg": "Not support timeout now."}

        cmd_id = args["cmd_id"]
        if self.commands.get(cmd_id):
            cmd = self.commands.pop(cmd_id)
            return {"status": "success", "msg": "get result success", "result": cmd["result"]}
        else:
            return {"status": "fail", "msg": "cmd_id: {} is not found".format(cmd_id)}

    def _get_result(self, cmd_id):

        cmd = self.commands.pop(cmd_id)
        return cmd["result"]

    def get_env(self, args):
        return {"status": "success", "msg": "get env success", "data": self.topology}

    def write_conf(self, args):
        """
        TODO: write config file .ini
        :param args:
        :return:
        """
        return {"status": "success", "msg": "get env success","data":self.topology}