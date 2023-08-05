from setux.core.package import CommonPackager


# pylint: disable=no-member


class Distro(CommonPackager):
    manager = 'gem'

    def do_init(self):
        self.target.distro.Package.install('ruby-dev')
        self.target.distro.Package.install('rubygems')

    def do_installed(self):
        ret, out, err = self.run('gem list')
        for line in out:
            line = line.replace('(', '')
            line = line.replace(')', '')
            n, *_, v = line.split()
            yield n, v

    def do_installable(self, pattern):
        ret, out, err = self.run(f'gem search {pattern}')
        for line in out:
            name, ver = line.split()
            yield name.strip(), ver.strip('( )')

    def do_remove(self, pkg):
        self.run(f'gem uninstall {pkg}')

    def do_cleanup(self):
        raise NotImplemented

    def do_update(self):
        raise NotImplemented

    def do_install(self, pkg, ver=None):
        self.run(f'gem install {pkg}')
