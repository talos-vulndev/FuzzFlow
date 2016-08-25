import threading, os, subprocess, hashlib
from client.helper import Helper


class Fuzzer():
    prev_hsh = ''
    helper = None
    timer = None
    def __init__(self, job, engine, target, options):
        self.job = job
        self.engine = engine
        self.target = target
        self.options = options
        self.helper = Helper()
        self.crashes = []

    def fail(self, err=None):
        self.job = self.helper.move_job_state(self.job, '*', 'Failed')
        if err is not None:
            self.helper.update_job_output(self.job['id'], err)
        call_args = [
            'pkill',
            'afl-fuzz'
        ]
        subprocess.call(call_args)
        if self.timer is not None:
            self.timer.cancel()

    def watch_for_crash(self, dir):
        for root, dirs, samples in os.walk(dir):
            for sample in samples:
                try:
                    found = self.crashes.index(sample)
                except:
                    self.crashes.append(sample)
                    self.helper.report_crash_sample(self.job, self.target, dir + os.sep + sample)


    def start(self):
        def probe_afl():
            out_dir = self.options['afl_out_dir']
            self.watch_for_crash(out_dir + os.sep + 'crashes')
            try:
                raw_stats = open(out_dir + os.sep + 'fuzzer_stats').read()
            except Exception as e:
                self.fail(e.message)

            hsh = hashlib.md5(raw_stats)
            if hsh != self.prev_hsh:
                self.job = self.helper.move_job_state(self.job, 'Allocated', 'Active')
                self.helper.update_job_output(self.job['id'], raw_stats)
                self.prev_hsh = hsh

        def wrapper1():
            probe_afl()
            e = threading.Event()
            while not e.wait(10): #We update the status of afl with server every 20 seconds
                probe_afl()

        self.timer = threading.Timer(5, wrapper1)
        self.timer.start()

        in_dir = self.options['afl_in_dir']
        out_dir = self.options['afl_out_dir']
        tout = self.options['afl_timeout']
        call_args = [
            self.engine['path'],
            '-i',
            in_dir,
            '-o',
            out_dir
        ]

        if tout is not None and len(tout) > 0:
            call_args.append('-t')
            call_args.append(tout)

        call_args.append('--')
        call_args.append(self.target['path'])
        call_args.append('@@')

        proc = subprocess.Popen(call_args, stdout=subprocess.PIPE)
        if proc.wait() != 0:
            output = proc.stdout.read()
            self.fail(output)

