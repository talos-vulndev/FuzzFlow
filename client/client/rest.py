import requests

from config import SERVER_ENDPOINT


class Rest(object):
    @staticmethod
    def url(sections):
        return SERVER_ENDPOINT + '/'.join(sections)

    @staticmethod
    def post(sections, payload):
        r = requests.post(Rest.url(sections), json=payload)
        return r

    @staticmethod
    def get(sections, params=None):
        r = requests.get(Rest.url(sections), params=params)
        return r

    @staticmethod
    def download_file(url):
        filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.__iter__():
                if chunk:
                    fd.write(chunk)
                    fd.flush()
        return filename

    @staticmethod
    def upload_file(f):
        files = {'file': f}
        r = requests.post(Rest.url(['api', 'upload']), files=files)
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def create_log(message):
        payload = {"message": message}
        r = Rest.post(['api', 'log'], payload)
        print r.json()

    @staticmethod
    def list_platform():
        r = Rest.get(['api', 'platform'])
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def create_platform(name):
        r = Rest.post(['api', 'platform'], {
            "name" : name
        })
        if r.status_code == 201:
            return r.json()
        else:
            return None

    @staticmethod
    def list_arch():
        r = Rest.get(['api', 'arch'])
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def create_arch(name):
        r = Rest.post(['api', 'arch'], {
            "name": name
        })
        if r.status_code == 201:
            return r.json()
        else:
            return None

    @staticmethod
    def get_host_by_mac(mac):
        r = Rest.get(['api', 'host', mac], {'mac': 1})
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def create_host(host):
        r = Rest.post(['api', 'host'], host)
        if r.status_code == 201:
            return r.json()
        else:
            return None

    @staticmethod
    def update_host(host_id, host):
        r = Rest.post(['api', 'host', host_id], host)
        if r.status_code == 201:
            return r.json()
        else:
            return None

    @staticmethod
    def get_update(hash):
        r = Rest.get(['api', 'update', hash])
        if r.status_code == 200:
            payload = r.json()
            return Rest.download_file(payload['url'])
        else:
            return None

    @staticmethod
    def get_job_by_host(host_id):
        r = Rest.get(['api', 'job', host_id], {'host': 1})
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def update_job(job_id, payload):
        r = Rest.post(['api', 'job', job_id], payload)
        if r.status_code == 201:
            return r.json()
        else:
            return None

    @staticmethod
    def list_job_state():
        r = Rest.get(['api', 'job'], {'state': 1})
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def get_engine(engine_id):
        r = Rest.get(['api', 'engine', engine_id])
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def get_target(target_id):
        r = Rest.get(['api', 'target', target_id])
        if r.status_code == 200:
            return r.json()
        else:
            return None

    @staticmethod
    def create_crash(crash):
        r = Rest.post(['api', 'crash'], crash)
        if r.status_code == 201:
            return r.json()
        else:
            return None

