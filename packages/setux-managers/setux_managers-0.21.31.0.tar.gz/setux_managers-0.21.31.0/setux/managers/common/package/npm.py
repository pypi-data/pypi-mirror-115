from setux.core.package import CommonPackager


# pylint: disable=no-member


class Distro(CommonPackager):
    manager = 'npm'

    def do_init(self):
        self.target.distro.Package.install('npm')

    def do_installed(self):
        ret, out, err = self.run('npm list -g --depth=0')
        for line in out[1:]:
            if len(line)<5: continue
            n, v = line[4:].split('@')
            yield n, v

    def do_installable(self, pattern):
        ret, out, err = self.run(f'npm search {pattern}')
        for line in out[1:]:
            fields = line.split('|')
            name, ver = fields[0], fields[4]
            yield name.strip(), ver.strip()

    def do_remove(self, pkg):
        self.run(f'npm uninstall {pkg}')

    def do_cleanup(self):
        raise NotImplemented

    def do_update(self):
        raise NotImplemented

    def do_install(self, pkg, ver=None):
        self.run(f'npm install -g {pkg}')
