import time, socket, hashlib, zipfile, os, sys, shutil, glob, platform, base64, subprocess, tempfile
from uuid import getnode

from rest import Rest

class Helper(object):
    def __init__(self):
        self.host = None
        self.states = None


    def get_mac(self):
        mac = getnode()
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (
            mac >> 40,
            mac >> 32 & 0xff,
            mac >> 24 & 0xff,
            mac >> 16 & 0xff,
            mac >> 8 & 0xff,
            mac & 0xff,
        )


    def get_default_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('moflow.org', 9))
            client = s.getsockname()[0]
        except socket.error:
            client = "0.0.0.0"
        finally:
            del s
        return client

    def get_platform_id(self):
        plat_name = platform.system() + ' ' + platform.release()

        plats = Rest.list_platform()
        if plats is not None and len(plats) > 0:
            for p in plats:
                if p['name'] == plat_name:
                    return p['id']

        new_platform = Rest.create_platform(plat_name)
        return new_platform['id']



    def get_arch_id(self):
        arch_name = platform.machine()

        arches = Rest.list_arch()
        if arches is not None and len(arches) > 0:
            for a in arches:
                if a['name'] == arch_name:
                    return a['id']

        new_arch = Rest.create_arch(arch_name)
        return new_arch['id']

    def register_host(self):
        print "[*] Trying to register the host..."
        platform_id = self.get_platform_id()
        arch_id = self.get_arch_id()
        mac = self.get_mac()
        hostname, alias_list, addr_list = socket.gethostbyaddr(self.get_default_ip())
        ip = addr_list[0]
        host_payload = {
            'name' : hostname,
            'mac' : mac,
            'ip' : ip,
            'platform_id': platform_id,
            'arch_id': arch_id
        }

        self.host = Rest.get_host_by_mac(mac)
        if self.host is not None:
            print "[!] Host with mac address %s has already been registered." % mac
            Rest.update_host(self.host['id'], host_payload)
        else:
            self.host = Rest.create_host(host_payload)

        return self.host


    def update(self):
        print "[*] Trying to update the client..."
        try:
            with open("client.zip", "rb") as f:
                cli = f.read()
                hsh = hashlib.md5(cli).hexdigest()
        except IOError:
            hsh = "INVALID"

        path = Rest.get_update(hsh)
        if path is not None:
            shutil.rmtree('engine')
            shutil.rmtree('client')
            os.remove('client.py')
            os.remove('requirements.txt')

            f = zipfile.ZipFile(path, "r")
            f.extractall('tmp')
            f.close()

            root = 'tmp' + os.sep + 'client' + os.sep
            shutil.move(root + 'client', '.')
            shutil.move(root + 'engine', '.')
            shutil.move(root + 'client.py', '.')
            shutil.move(root + 'requirements.txt', '.')
            shutil.rmtree('tmp')

            args = sys.argv[:]
            print "[*] Update installed successfully, restarting...\n"

            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]

            os.execv(sys.executable, args)
            sys.exit(1)

        else:
            print "[!] Client is already the latest version."


    def log_error(self, message):
        log_file = "log-" + time.strftime("%Y-%m-%d-%H.%M.%S") + ".log"
        with open(log_file, "a") as f:
            f.write(message)

        Rest.create_log(message)

    def extract_job(self, job):
        engine = Rest.get_engine(job['engine_id'])
        target = Rest.get_target(job['target_id'])
        options = {}
        for opt in engine['options']:
            for opt_val in job['options']:
                if opt['id'] == opt_val['option_id']:
                    options[opt['name']] = opt_val['value']

        return engine, target, options

    def get_state_id_by_name(self, name):
        if self.states is None:
            self.states = Rest.list_job_state()
        for state in self.states:
            if state['name'] == name:
                return state['id']

    def get_state_name_by_id(self, id):
        if self.states is None:
            self.states = Rest.list_job_state()
        for state in self.states:
            if state['id'] == id:
                return state['name']

    def update_job_state(self, job_id, state_id):
        return Rest.update_job(job_id, {
            'state_id': state_id
        })

    def move_job_state(self, job, current, next):
        if current == "*":
            new_state_id = self.get_state_id_by_name(next)
            return self.update_job_state(job['id'], new_state_id)

        state_name = self.get_state_name_by_id(job['state_id'])
        if state_name == current:
            new_state_id = self.get_state_id_by_name(next)
            return self.update_job_state(job['id'], new_state_id)
        return job

    def update_job_output(self, job_id, content):
        output = base64.encodestring(content)
        return Rest.update_job(job_id, {
            'output': output
        })

    def report_crash_sample(self, job, target, sample):
        if platform.system() == 'Linux':
            tmp = tempfile.NamedTemporaryFile()
            dump_file_name = tmp.name

            dbg_cmd = [
                'gdb',
                '-batch',
                '-ex', 'run',
                '-ex', 'set disassembly-flavor intel',
                '-ex', 'info registers',
                '-ex', 'bt full',
                '-ex', 'disass',
                '-ex', 'generate-core-file %s' % dump_file_name,
                '--args',
                target['path'],
                sample
            ]

            print dbg_cmd

            dbg_file = dump_file = None
            proc = subprocess.Popen(dbg_cmd, stdout=subprocess.PIPE)
            if proc.wait() == 0:
                try:
                    dbg_file = Rest.upload_file(proc.stdout)
                    dump_file = Rest.upload_file(open(dump_file_name, 'rb'))
                except:
                    None



            crash_payload = {}
            crash_payload['job_id'] = job['id']

            repro_file = Rest.upload_file(open(sample, 'rb'))
            if repro_file is not None:
                crash_payload['repro_file'] = repro_file['upload_path']
            if dump_file is not None:
                crash_payload['dump_file'] = dump_file['upload_path']
            if dbg_file is not None:
                crash_payload['dbg_file'] = dbg_file['upload_path']

            print Rest.create_crash(crash_payload)


        else:
            print "No Implemented!!!"
