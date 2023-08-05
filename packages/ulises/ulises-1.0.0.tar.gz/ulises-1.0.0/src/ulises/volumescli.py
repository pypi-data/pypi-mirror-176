from ulises.subcli import SubCli
from pprint import pprint as pp

class VolumesCli(SubCli):
    def __init__(self, docker):
        super().__init__("volumes")
        self.docker=docker

    def CMD_code(self):
        import code
        code.interact(local=locals())

    def COMPLETER_ls(self):
        pass
    def COMPLETER_rm(self):
       for i in self.docker.volumes.list():
           yield i.name

    def enrich_containers_in_vols(self,df_data):
        vmap = {}

        for i in df_data['Containers']:
            for m in i['Mounts']:
                if m['Type']=='volume':
                    vmap.setdefault(m['Name'], []).append(self.color(i['Names'][0][1:],self.FIELD_STYLE["status"].get(i['State'],"")))

        for i in df_data['Volumes']:
            i['UsageData']['Containers']=vmap.setdefault(i['Name'],[])


    def CMD_ls(self,*args):
        '''list volumes'''

        df = self.docker.df()

        self.enrich_containers_in_vols(df)

        self.print_table(sorted(df['Volumes'], key=lambda x: x['UsageData']['Size']),[
        ("name", lambda x,y: x['Name']), 
        ("size", lambda x,y: self.format_bytes(x['UsageData']['Size'])), 
        ("references", lambda x,y: x['UsageData']['Containers'])
        ])

    def CMD_rm(self,*args):
        '''remove volumes (autocompletes volume name)'''
        if not args:
            print ("You must specify at least one volume")
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

