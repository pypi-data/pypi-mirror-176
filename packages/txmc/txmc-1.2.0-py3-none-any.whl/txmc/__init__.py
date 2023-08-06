#encoding='utf-8' 
import socket
import select,base64,collections,math
class Minecraft:
    def __init__(self,server,guid):
        self.nickname='player'
        self.message=''
        self.status=False
        self.__socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect(('tk.makeblock.net.cn',4710))
        if self.__sendReceive('?????')=='?????':
            args=self.__sendReceive('python|%s|%s'%(guid,server)).split('`')
            if len(args)==2 and args[1]=='ok':
                self.nickname=args[0]
                self.status=True
            else:
                self.message=args[0]
        else:
            self.Close()
    def __drain(self):
        while True:
            readable, _, _ = select.select([self.__socket], [], [], 0.0)
            if not readable:
                break
            try:
                data = self.__socket.recv(1500)
                e =  "Drained Data: <%s>"%data.strip()
                print(e)
                break
                self.__socket.close()
            except Exception as e:
                print('error!',e)
    def __flatten(self,l):
        for e in l:
            if isinstance(e, collections.Iterable) and not isinstance(e, str):
                for ee in self.__flatten(e): yield ee
            else: yield e
    def __flatten_parameters_to_bytestring(self,l):
        return b",".join(map(_misc_to_bytes, self.__flatten(l)))
    def _misc_to_bytes(self,m):
        return str(m).encode(encoding='UTF-8')
    def __intFloor(self,*args):
        return [int(math.floor(x)) for x in self.__flatten(args)]
    def __send(self,s):
        if self.__socket==None:
            return None
        self.__drain()
        self.lastSent = s
        if self.status:
            self.__socket.sendall(base64.b64encode(base64.b64encode(bytes(s,'utf-8'))[::-1])+b'\n')
        else:
            self.__socket.sendall(bytes(s,'utf-8')+b'\n')
    def __receive(self):
        if self.__socket==None:
            return None
        if self.status:
            return base64.b64decode(base64.b64decode(bytes(self.__socket.makefile("r").readline().rstrip("\n"),encoding='utf-8'))[::-1]).decode('utf-8')
        else:    
            return self.__socket.makefile("r",encoding='utf-8').readline().rstrip("\n")
    def __sendReceive(self,*data):
        self.__send(*data)
        return self.__receive()
    def Close(self):
        self.__socket=None
        self.status=False
    @staticmethod
    def Connect(server,guid):
        return Minecraft(server,guid)
    def toChat(self,msg):
        self.__send('''tochat:%s说:%s''' % (self.nickname,msg))
    def getBlock(self,*args):
        return self.__sendReceive('''getblock:%s|%s|%s''' % tuple(self.__intFloor(args)))
    def setBlock(self,*args):
        self.__send('''setblock:%d|%d|%d|%d|%d''' % tuple(self.__intFloor(args)))
    def setBlockByName(self,x,y,z,blockname,data,type='replace'):
        return self.__sendReceive('''setblocknew:{_x}|{_y}|{_z}|{_block}|{_data}|{_type}'''
        .format(_x=x,_y=y,_z=z,_block=blockname,_data=data,_type='keep' if type=='keep' else 'replace'))
    def drawLine(self,*args):
        return self.__send('''drawLine:%s|%s|%s|%s|%s|%s|%s|%s''' % tuple(self.__intFloor(args)))
    def setBlocks(self,*args):
        return self.__send('''setblocks:%s|%s|%s|%s|%s|%s|%s|%s''' % tuple(self.__intFloor(args)))
    def setBlocksByName(self,x,y,z,x1,y1,z1,blockname,data=0,type='replace'):
        return self.__sendReceive('''setblocksnew:{_x}|{_y}|{_z}|{_x1}|{_y1}|{_z1}|{_block}|{_data}|{_type}'''
        .format(_x=x,_y=y,_z=z,_x1=x1,_y1=y1,_z1=z1,_block=blockname,_data=data,_type=type))
    def getMyPos(self):
        return self.__sendReceive('''getplaypos:%s'''%(self.nickname))
    def setMyFly(self):
        self.__send('''playfly:%s|1'''%(self.nickname))
    def openInventory(self,index=1):
        return self.__sendReceive('''openmyinventory:%s''' % (index))
    def setMyPos(self,x,y,z):
        return self.__sendReceive('''setplayerpos:%s|%d|%d|%d'''%(self.nickname,x,y,z))
    def setLight(self,*args):
        return self.__sendReceive('''light:%d|%d|%d'''% tuple(self.__intFloor(args)))
    def drawCircle(self,x,y,z,radius,id,data,type='x'):
        self.__send('''drawCircle:%d|%d|%d|%d|%d|%d|%d'''% (1 if type=='x' else 0 ,x,y,z,radius,id,data))
    def drawSphere(self,x,y,z,radius,id,data,type=0):
        self.__send('''drawSphere:%d|%d|%d|%d|%d|%d|%d'''% (type,x,y,z,radius,id,data))