import os
import random
from amiibo import AmiiboDump, AmiiboMasterKey
from time import sleep
from pexpect.popen_spawn import PopenSpawn

eml_starting_line = 19
proxmark_path = "/usr/src/proxmark3/"
port = "bt:20:19:05:06:22:69"
#port = "/dev/ttyACM0"
amiibo_path = ""
key_path = ""

class Proxmark3:
    def __init__(self) -> None:
        self.proxmark_path = proxmark_path

        # Start the PM3 shell
        shell_command = os.path.join(proxmark_path, "client", "") + "proxmark3 " + port
        self.proxmark3 = PopenSpawn(shell_command)


    def eml_to_bin(self, eml_path: str, bin_path: str):
        eml_file = open(eml_path, 'r')
        lines = eml_file.readlines()
        lines = lines[eml_starting_line:]

        data = []

        for line in lines:
            data.append(int(line[0:1], 16))
            data.append(int(line[2:3], 16))
            data.append(int(line[4:5], 16))
            data.append(int(line[6:7], 16))

        bin_file = open(bin_path, "wb")
        bin_file.write(bytearray(data))


    def pm3_load(self, dump_name: str):
        command = "hf mfu eload -f " + os.path.join(amiibo_path, dump_name)
        self.proxmark3.sendline(command)

        self.proxmark3.expect("Done!")

        command = "hf mfu sim -t 7"
        self.proxmark3.sendline(command)


    def randomize_uid(self, input_name: str):
        uid = "04"

        input_path = os.path.join(amiibo_path, input_name)
        output_path = os.path.join(amiibo_path, "temp.bin")

        for i in range(0, 6):
            uid += hex(random.randint(0, 255))[2:]

        with open(key_path, 'rb') as keybin:
            master_key = AmiiboMasterKey.from_combined_bin(keybin.read())

        with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
            dump = AmiiboDump(master_key, fin.read(), is_locked=True)
            dump.unlock()
            dump.uid_hex = uid
            dump.lock()
            fout.write(dump.data)
    
        self.pm3_load("temp.bin")

        os.remove(output_path)


    def write_back(self, dump_name: str):
        command = "hf mfu esave -f temp"
        self.proxmark3.sendline(command)
        self.proxmark3.expect("to binary")
        sleep(1)

        source_path = os.path.join(self.proxmark_path, "temp.bin")
        destination_path = os.path.join(amiibo_path, dump_name)
        os.replace(source_path, destination_path)

        os.remove(source_path)
