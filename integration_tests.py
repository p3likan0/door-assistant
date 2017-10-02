#!/usr/bin/env python3
import unittest
import json
import shlex
import subprocess
from time import sleep

BUILD = "mos build --arch esp8266"
FLASH = "mos flash"
USER = "prueba"
PASSWORD = "pobaxx"
GEN_PASS_RPC = "/bin/bash generate_user_and_password_for_rpc.sh {} {}"
RPC_CRED = 'mos --rpc-creds "{}:{}"'
GET_CONF = "call Config.Get"
SET_CONF = "config-set"
ENABLE_DOOR = "door.enable=true"
DISABLE_DOOR = "door.enable=false"


class TestStringMethods(unittest.TestCase):
    def test_build(self):
        args = shlex.split(BUILD)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)

    def test_flash(self):
        args = shlex.split(FLASH)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(10)

    def test_generate_rpc_user_and_password(self):
        args = shlex.split(GEN_PASS_RPC.format(USER, PASSWORD))
        print(args)
        p = subprocess.Popen(args)
        exit_code = p.wait()

        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(GET_CONF)
        print(args)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)

    def test_disable_door(self):
        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(SET_CONF)
        args += shlex.split(DISABLE_DOOR)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(3)

        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), "false")
        p.stdout.close()

    def test_enable_door(self):
        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(SET_CONF)
        args += shlex.split(ENABLE_DOOR)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(3)

        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), "true")
        p.stdout.close()


if __name__ == '__main__':
    unittest.main()
