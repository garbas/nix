import click
import os
import shutil
import tarfile
import tempfile
import zipfile


MODES = ['single-user', 'multi-user']


def multi_user_mode():

    # linux
    # TODO: darwin -> http://nixos.org/nix/manual/#ssec-multi-user
    os.system('groupadd -r nixbld')
    for number in range(10):
        os.system('useradd -c "Nix build user {number}" -d /var/empty '
                  '-g nixbld -G nixbld -M -N -r -s "$(which nologin)" '
                  'nixbld{number}'.format(number=number))


options = dict(
    mode=dict(
        type=click.Choice(MODES),
        default="single-user",
        help='''
            Nix has two basic security models. First, it can be used in
            “single-user mode”, which is similar to what most other package
            management tools do: there is a single user (typically root) who
            performs all package management operations. All other users can
            then use the installed packages, but they cannot perform package
            management operations themselves.

            Alternatively, you can configure Nix in “multi-user mode”. In this
            model, all users can perform package management operations — for
            instance, every user can install software without requiring root
            privileges. Nix ensures that this is secure. For instance, it’s not
            possible for one user to overwrite a package used by another user
            with a Trojan horse.)
        '''
    )
)


def prompt(options, value):
    while True:
        break


@click.command()
def main():
    """ Nix installer.
    """
    click.echo('This is new nix installer')


# @click.option('--no-prompt', default=False, is_flag=True)
# @click.option('--mode', **options['mode'])
def main_(no_prompt, mode):
    def prompt_for(name):
        value = locals()[name]
        if not no_prompt:
            value = prompt(options[name], value)
        return value

    prompt_for('mode')

    click.echo('Installing Nix to `/nix/store`')

    try:
        tmp_dir = tempfile.mkdtemp(prefix='nix-installer-')

        unpack_dir = os.path.join(tmp_dir, 'unpack')
        archive_file = os.path.join(tmp_dir, 'archive.tar.bz2')

        os.mkdir(unpack_dir)

        ZIP = zipfile.ZipFile(os.path.dirname(__file__))
        ZIP.extractall(tmp_dir)

        TAR = tarfile.open(archive_file, mode='r:bz2')
        TAR.extractall(path=unpack_dir)

        if mode == "single-user":
            os.system(unpack_dir + "/*/install")

        elif mode == "multi-user":
            multi_user_mode()

        else:
            raise click.exceptions.ClickException(
                click.style('Wrong mode selected.', color='red'))

        click.secho("Nix installed. Sorry for the convenience.", fg="green")

    finally:
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
