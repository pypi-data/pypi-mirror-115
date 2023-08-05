import json


class TreeNode():
    def __init__(self,id,name="noname", len=0):
        self.id=id
        self.name=name
        self.len = len
        self.AllLen=0
        self.child=[]

    def setLen(self,name,length):
        if self.name==name:
            if len(self.child)>0:
                othernode = TreeNode(self.id,self.name+"'other",length)
                othercount=0
                for child in self.child:
                    if child.name== othernode.name:
                        othercount=othercount+1
                if othercount ==0:
                    self.child.append(othernode)
            else:
                self.len=length
        else:
            for child in self.child:
                child.setLen(name,length)

    def GetAllLen(self,name0,len):
        if self.name==name0:
            len= self.getAllLen()
        else:
            for child0 in self.child:
                if child0.name==name0:
                    len= child0.getAllLen()
                else:
                    len =child0.GetAllLen(name0,len)
        return len

    def getAllLen(self):
        if self.child :
            # print(self.child[0])
            self.AllLen =self.len   
            for child in self.child:
                self.AllLen =self.AllLen+child.getAllLen() 
        else:
            # print(self.len)
            self.AllLen =self.len
        # print(self.child)
        return self.AllLen

    def addChild(self,child):
        self.child.append(child)
    def print(self,depth=1,level=0):

        if depth>0:
            # print("--------------")
            for child in self.child:
                if child.getAllLen() :
                    for i in range(level):
                        print("\t",end="")
                
                    print(child.name+"  "+str(child.AllLen)  )

                child.print(depth-1,level+1)

    def __str__(self):
        # for child in self.child:
        #         print(child)
        return self.name +":"+ str(self.getAllLen())


class Anatation:
	def __init__(self,jsonfile='1.json'):
		with open(jsonfile) as regionsjson:
			regions = json.load(regionsjson)
			rootjson = regions['msg'][0]


	def readnode(self,nodejson):
		node = TreeNode(nodejson['id'],nodejson['acronym'])
		# print(node)
		if 'children' in nodejson:
			if nodejson['children']:
				for childjson in nodejson['children']:
					childnode = self.readnode(childjson)
					node.addChild(childnode)
		return node