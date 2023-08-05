from rich.console import Console
from rich.table import Table
import readline
import re
import sys
from pprint import pformat

def pf(v):
    if type(v) in (list,dict,tuple):
        return pformat(v)
    return v

class SubCli():

    FIELD_STYLE = {
        "status": {
          "created":"bold blue on black",
          "restarting":"bold pink on black",
          "running":"bold green on black",
          "removing":"bold orange on black",
          "paused":"bold yellow on black",
          "exited":"bold red on black",
          "dead":"bold brown on black"
        }
    }

    def __init__(self, mode=""):
        self.mode = "ulises" + (f":{mode}" if mode else mode)

        self.matches=[None]
        self.exit=False

        self.next_command=None

        self.CMDS = {i[4:]:getattr(self,i) for i in dir(self) if i.startswith('CMD_')}
        self.COMPLETERS = {i[10:]:getattr(self,i) for i in dir(self) if i.startswith('COMPLETER_')}
        self.console = Console()

    def cmdloop(self):
        while True and not self.exit:
            readline.set_completer(self.main_completer)
            try:
                if self.next_command:
                    last_command = self.next_command
                    self.next_command = None
                else:
                    last_command = input(f"{self.mode}> ")
                self.process_command(last_command)
            except EOFError as e:
                last_command = "exit"
                break
        return last_command

    def key_val_table(self,tuples,title=None):
        table=Table(title=pf(title))
        table.add_column("key")
        table.add_column("value")

        for i,j in tuples:
            table.add_row(i,pf(j))

        self.console.print(table)

    def format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : '', 1: 'k', 2: 'm', 3: 'g', 4: 't'}
        while size > power:
            size /= power
            n += 1
        return f'{size:.2f} {power_labels[n]}b'

    def main_completer(self,text,state):
        if state==0:
            if re.match("^\S*$",readline.get_line_buffer()):
                self.matches=[i+" " for i in self.CMDS if i.startswith(text)] + [None]
            elif re.match("^\S+\s+\S*",readline.get_line_buffer()):
                cmd=re.findall("^(\S+)\s",readline.get_line_buffer())
                if not cmd: self.matches=[None]
                elif cmd[0] in self.COMPLETERS:
                    self.matches=[(i,i) for i in self.COMPLETERS[cmd[0]]() if re.search(text, i)]
                    if len(self.matches)>1:
                        self.matches = [i[1][i[1].find(text):] for i in self.matches]+[None]
                    elif len(self.matches)==1:
                        self.matches=[self.matches[0][0]+" ",None]
                    else:
                        self.matches=[None]

            elif re.match("^\S+\s+\S+\s+",readline.get_line_buffer()):
                self.matches=[None]

        return self.matches[state]

    def process_command(self,cmd):
        parsed = re.findall('^(?:\s*(\S+))?(?:\s+(\S+.*))?$',cmd.strip())
        if not parsed or not parsed[0][0]:
            return

        cmd,arg = parsed[0]

        if cmd not in self.CMDS:
            sys.stderr.write(f'Command "{cmd}" does not exist\n')
        else:
            try:
                self.CMDS[cmd](*re.findall('\S+',arg))
            except Exception as ex:
                self.error=1
                sys.stderr.write (f'Error: {ex}\n')


    def print_table(self, data,fields):
        table = Table()
        for i in fields:
            if type(i) == str:
              table.add_column(i)
            elif type(i) == tuple and len(i)==2 and type(i[0])==str:
              table.add_column(i[0])
        
        for i in data:
            row = []
            for fi in fields:
                if type(fi) == str:
                    fname = fi
                    l = lambda x,y: getattr(x,y)
                elif type(fi) == tuple and len(fi)==2 and type(fi[0])==str:
                    fname, l = fi
                else:
                    continue

                val = l(i,fname)
                if fname in self.FIELD_STYLE:
                    st = self.FIELD_STYLE[fname][val]
                    row.append(f"[{st}]{pf(val)}[/{st}]")
                else:
                    row.append(pf(val))

            table.add_row(*row)
        
        self.console.print(table)

    def select_resources(self,*args):
        if self.mode == "ulises:containers":
            r = self.docker.containers.list(all=True)
            r = [(i,[i.short_id, i.name]) for i in r]
        if self.mode == "ulises:images":
            r = self.docker.images.list()
            r = [(i,[i.short_id, i.tags[0] if i.tags else "<None>"]) for i in r]

        return {i[0] for i in r if any(any(re.search(j,k) for k in i[1]) for j in args)}

    def color(self,txt,fmt=None):
        if not fmt:
            return txt
        else:
            return "[{0}]{1}[/{0}]".format(fmt,txt)

    def CMD_images(self, *args):
        '''switches to docker images CLI'''
        self.exit=True
    def CMD_containers(self, *args):
        '''switches to docker containers CLI'''
        self.exit=True
    def CMD_networks(self, *args):
        '''switches to docker networks CLI'''
        self.exit=True
    def CMD_volumes(self, *args):
        '''switches to docker volumes CLI'''
        self.exit=True
    def CMD_exit(self, *args):
        '''exits ulises (CTRL+D also works)'''
        self.exit=True
    def CMD_help(self, *args):
        '''shows this help message (you can use 'h' as well)'''
        print ("=== List of commands ===")

        defaults = ["help","images","containers","volumes","networks","exit"]

        data = []

        for i in defaults:
            data.append([i,self.CMDS[i].__doc__])
        data.append(["",""])

        for i,j in self.CMDS.items():
            if i not in defaults+["h"]:
                data.append([i,j.__doc__])

        self.print_table(data,[("Command", lambda x,y: x[0]),("Description", lambda x,y: x[1])])
    CMD_h = CMD_help

    def COMPLETER_images(self): 
        pass
    COMPLETER_containers=COMPLETER_networks=COMPLETER_volumes=COMPLETER_exit=COMPLETER_help=COMPLETER_images
