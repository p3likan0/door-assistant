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
RPC_INV_CRED = 'mos --rpc-creds "no:existe"'
RPC_NO_CRED = "mos"
GET_CONF = "call Config.Get"
SET_CONF = "config-set"
ENABLE_DOOR = "door.enable=true"
DISABLE_DOOR = "door.enable=false"
OPEN_DOOR = "call Door.Open"


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
        sleep(3)

    def test_should_generate_rpc_user_and_password(self):
        args = shlex.split(GEN_PASS_RPC.format(USER, PASSWORD))
        p = subprocess.Popen(args)
        p.wait()  # mongoose bug, output its error when load credentials.

    def test_should_get_config_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(GET_CONF)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)

    def test_should_not_get_config_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(GET_CONF)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_disable_door_when_credentials_are_valid(self):
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

    def test_should_not_disable_door_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(SET_CONF)
        args += shlex.split(DISABLE_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()
        sleep(3)

        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_enable_door_when_credentials_are_valid(self):
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

    def test_should_open_door_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER, PASSWORD))
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), '{\n  "Door": "Open"\n}')
        p.stdout.close()

    def test_should_not_open_door_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_not_open_door_when_dont_have_credentials(self):
        args = shlex.split(RPC_NO_CRED)
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("wrong RPC creds spec", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()


if __name__ == '__main__':
    unittest.main()
