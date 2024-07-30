import subprocess
import os


def upgrage():
    print("Upgrading...")
    subprocess.run('alembic upgrade head', shell=True, check=True)


def downgrade():
    print('Downgrading')
    subprocess.run('alembic downgrade base', shell=True, check=True)


def smart_input(inf_text, inp_text, incorrect, can_be_text):
    print(inf_text)
    while True:
        inp = input(inp_text)
        if can_be_text(inp):
            return inp
        print(incorrect)


def updater_func():
    directory = os.path.dirname(os.getcwd())
    os.chdir(directory)

    while True:
        inp = smart_input('Choose what do you want to do with database: upgrade, downgrade, or exit from program',
                          'Options: upgrade, downgrade, exit: ',
                          'Maybe you have mistyped, try again.',
                          lambda x: x in ['upgrade', 'downgrade', 'exit'])
        os.chdir(directory)

        if inp == 'upgrade':
            upgrage()
        elif inp == 'downgrade':
            downgrade()
        elif inp == 'exit':
            return


if __name__ == '__main__':
    updater_func()
