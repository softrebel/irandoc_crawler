from src.cmds import *

lang=LANG


def main():
    while True:
        value = click.prompt(LANG['main'], type=click.Choice(list(cli.commands.keys()) + ['exit']))
        if value != 'exit':
            cli.commands[value]()


if __name__ == '__main__':
    main()




