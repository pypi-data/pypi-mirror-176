from ulises.subcli import SubCli

class ContainersCli(SubCli):
    def __init__(self, docker):
        super().__init__("containers")
        self.docker=docker

    def describe_mounts(self, container):
        res = []
        for i in container.attrs["Mounts"]:
            if i["Type"]=="volume":
                res.append(f"volume(path:{i['Destination']} - id:{i['Name'][:10]})")
            elif i["Type"]=="bind":
                res.append(f"bind(src:{i['Source']} - dst:{i['Destination']} - {i['Mode']})")
        return res

    def CMD_code(self):
        import code
        code.interact(local=locals())

    def COMPLETER_ls(self):
        for i in self.docker.containers.list(all=True):
            yield i.name
            yield i.short_id
    COMPLETER_rm=COMPLETER_ls
    
    def COMPLETER_start(self):
        for i in self.docker.containers.list(all=True):
            if i.status!="exited": continue
            yield i.name
            yield i.short_id

    def COMPLETER_stop(self):
        for i in self.docker.containers.list(all=True):
            if i.status!="running": continue
            yield i.name
            yield i.short_id

    COMPLETER_pause=COMPLETER_stop

    def COMPLETER_unpause(self):
        for i in self.docker.containers.list(all=True):
            if i.status!="paused": continue
            yield i.name
            yield i.short_id


    def CMD_ls(self,*args):
        '''list containers (autocompletes names or ids)'''
        if not args:
            self.print_table(sorted(self.docker.containers.list(all=True), key=lambda x: x.status!="running"),["status","short_id","name"])
        else:
            r = self.select_resources(*args)
            for i in r:
                self.key_val_table ([
                    ["created", i.attrs["Created"]],
                    ["image", [i.attrs["Config"]["Image"],i.attrs["Image"].split(":")[1][:10]]],
                    ["env", i.attrs["Config"]["Env"]],
                    ["cmd", " ".join(i.attrs["Config"]["Cmd"])],
                    ["entrypoint", i.attrs["Config"]["Entrypoint"]],
                    ["ports", i.attrs["NetworkSettings"]["Ports"]],
                    ["networks", list(i.attrs["NetworkSettings"]["Networks"].keys())],
                    ["mounts", self.describe_mounts(i)],
                    ["state",i.attrs["State"]["Status"]],
                    ],
                    [i.name,i.attrs["Config"]["Hostname"]]) 

    def CMD_rm(self,*args):
        '''removes containers (autocompletes names or ids)'''
        if not args:
            print ("You must specify at least one container")
        else:
            r = [i for i in self.select_resources(*args)]
            self.print_table(r,["status","name"])
            if input("Press Y to delete: ").upper()=='Y':
                for i in r:
                    print (f"Deleting {i.name}")
                    i.remove(force=True)
                print ("Done!")

    def CMD_start(self,*args):
        '''starts containers (autocompletes names or ids)'''
        r = [i for i in self.select_resources(*args) if i.status=="exited"]
        if not r:
            print ("You must specify at least one container with exited status")
        else:
            if len(r)>1:
                self.print_table(r,["status","name"])
                if input("Press Y to start containers: ").upper()!='Y':
                    return
            for i in r:
                print (f"Starting {i.name}")
                i.start()
            print ("Done!")
           
    def CMD_stop(self,*args):
        '''stops containers (autocompletes names or ids)'''
        r = [i for i in self.select_resources(*args) if i.status=="running"]
        if not r:
            print ("You must specify at least one container with running status")
        else:
            if len(r)>1: 
                self.print_table(r,["status","name"])
                if input("Press Y to stop containers: ").upper()!='Y':
                    return
            for i in r:
                print (f"Stopping {i.name}")
                i.stop()
            print ("Done!")
           
    def CMD_pause(self,*args):
        '''pauses containers (autocompletes names or ids)'''
        r = [i for i in self.select_resources(*args) if i.status=="running"]
        if not r:
            print ("You must specify at least one container with running status")
        else:
            if len(r)>1: 
                self.print_table(r,["status","name"])
                if input("Press Y to pause containers: ").upper()!='Y':
                    return
            for i in r:
                print (f"Pausing {i.name}")
                i.pause()
            print ("Done!")
           
    def CMD_unpause(self,*args):
        '''unpauses containers (autocompletes names or ids)'''
        r = [i for i in self.select_resources(*args) if i.status=="paused"]
        if not r:
            print ("You must specify at least one container with paused status")
        else:
            if len(r)>1: 
                self.print_table(r,["status","name"])
                if input("Press Y to unpause containers: ").upper()!='Y':
                    return
            for i in r:
                print (f"unpausing {i.name}")
                i.unpause()
            print ("Done!")

