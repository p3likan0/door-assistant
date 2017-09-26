#!/usr/bin/env python3
import unittest
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


if __name__ == '__main__':
    unittest.main()
