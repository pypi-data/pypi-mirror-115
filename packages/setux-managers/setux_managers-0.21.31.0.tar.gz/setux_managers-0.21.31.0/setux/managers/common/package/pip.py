from re import compile

from setux.logger import error, info
from setux.core.package import CommonPackager
from setux.targets import Local


# pylint: disable=no-member


class Distro(CommonPackager):
    manager = 'pip'

    def do_init(self):
        self.target.distro.Package.install('setuptools')
        self.run(f'python3 -m pip install -qU pip')

    def do_install(self, pkg, ver=None):
        ret, out, err = self.run(f'python3 -m pip install -qU {pkg}')
        for o in out:
            if 'already satisfied' in o:
                break
            if 'Successfully installed' in o:
                info('\t--> %s %s', pkg, ver or '')
                break
        else:
            if any(line.strip() for line in out):
                error('\n'.join(out))

    def do_installed(self):
        ret, out, err = self.run('python3 -m pip list')
        for line in out[2:]:
            try:
                n, v = line.split()
                v = v.replace('(', '')
                v = v.replace(')', '')
                yield n, v
            except:
                error(line)

    def get_pkg_list(self):
        local = Local(outdir='/tmp')
        dst = '/tmp/setux/pypi.packages'
        try:
            fil = local.file(dst)
            if fil.age < 10: return
        except FileNotFoundError: pass

        url = 'https://pypi.org/simple'
        org = '/tmp/setux/pypi.simple'
        local.dir('/tmp/setux').deploy()
        local.download(url=url, dst=org)
        pat = compile(r'^.*?<a href="/simple/.*?/">(?P<name>.*?)</a>')
        with open(dst, 'w') as out:
            for line in open(org):
                try:
                    name = pat.search(line).groupdict()['name']
                    out.write(f'{name}\n')
                except AttributeError: pass
        local.file(org).rm()

    def do_installable(self, pattern):
        dst = '/tmp/setux/pypi.packages'
        self.get_pkg_list()
        for name in open(dst):
            yield name.strip(), '-'

    def do_remove(self, pkg):
        self.run(f'python3 -m pip uninstall -y {pkg}')

    def do_cleanup(self):
        raise NotImplemented

    def do_update(self):
        raise NotImplemented

