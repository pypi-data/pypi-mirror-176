from ulises.subcli import SubCli
from pprint import pprint as pp

class ImagesCli(SubCli):
    def __init__(self, docker):
        super().__init__("images")
        self.docker=docker

    def CMD_code(self):
        import code
        code.interact(local=locals())

    def COMPLETER_ls(self):
       for i in self.docker.images.list():
           if i.tags:
               yield i.tags[0]
           else:
               yield "None"
           yield i.short_id.split(":")[1]
    COMPLETER_rm=COMPLETER_ls

    def get_used_images(self):
        return {i["Id"] for i in self.docker.df()["Images"] if i["Containers"]!=0}


    def CMD_ls(self,*args):
        '''list images (autocompletes image name or id).  If arguments are passed it will list image details.  Otherwise it will list all images'''
        if not args:
            used = self.get_used_images()
            self.print_table(sorted(self.docker.images.list(), key=lambda x: (not x.attrs["Id"] in used, x.attrs["Size"])),[
            ("short_id", lambda x,y: x.short_id.split(":")[1]), 
            ("size", lambda x,y: self.format_bytes(x.attrs["Size"])), 
            ("name (green == running)", lambda x,y: (self.color(x.tags[0],"bold green") if x.attrs["Id"] in used else x.tags[0]) if x.tags else "<None>")
            ])
        else:
            r = self.select_resources(*args)
            for i in r:
                self.key_val_table([
                ["os",i.attrs["Os"]],
                ["size", self.format_bytes(i.attrs["Size"])],
                ["env", i.attrs["Config"]["Env"]],
                ["cmd", i.attrs["Config"]["Cmd"]],
                ["entrypoint", i.attrs["Config"]["Entrypoint"]],
                ],
                [i.tags, i.short_id])

    def CMD_rm(self,*args):
        '''remove images (autocompletes image name or id)'''
        if not args:
            print ("You must specify at least one image")
        else:
            r = [i for i in self.select_resources(*args)]
            self.print_table(r,[
                ("short_id", lambda x,y: x.short_id.split(":")[1]),
                ("name", lambda x,y: x.tags[0] if x.tags else "<None>")
            ])
            if input("Press Y to delete: ").upper()=='Y':
                for i in r:
                    print (f"Deleting {i.short_id}")
                    self.docker.images.remove(i.id)
                print ("Done!")

