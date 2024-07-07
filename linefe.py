import xml.etree.ElementTree as xml


class Linefe():
    """_summary_

            _type_: _description_
        """
    def __init__(self,docBase) -> None:
        
        self.Doc = docBase
        self.ScriptName = []
        self.Script = {}
        self.SubScripts = []
        self.Events = {}
        self.ReadXml()


    def ReadXml(self):
        """_summary_

            _type_: _description_
        """
        tree_xml = xml.parse(self.Doc)
        root = tree_xml.getroot()
        ScName = {}
        ScName["App"] = root.text
        ScName["Parans"] = root.attrib
        self.ScriptName.append(ScName)
        self.__readnodes(root)


    def __readnodes(self,child):
        valueTag ={}
        for i in child:
          valueTag[i.tag] = [i.text,i.attrib]
          for a in i:
              valueTag[i.tag].append({a.tag:[a.text,a.attrib]})
              if(len(list(a)) >=1):
                  self.__AddSubNodes(a,valueTag[i.tag])

          self.Script[i.tag] = valueTag
          valueTag = {}


    def __AddSubNodes(self,Element,ListElem):
        for E in Element:
            ListElem.append({E.tag:[E.text,E.attrib]})
            if(len(list(E)) >=1):
                self.__AddSubNodes(E,ListElem)

    def ReturnScript(self,Keyvalue,index=None,att=None):
        """_summary_
            Returns:
                _type_: _description_
            """
        if(index == None):
            return self.Script[Keyvalue][Keyvalue]
        else:
            if(att!= None):
                return self.Script[Keyvalue][Keyvalue][index][att]    
            return self.Script[Keyvalue][Keyvalue][index]

    def ExecuteScript(self,KeyValue,input=None):
        """_summary_
        Returns:
        _type_: _description_
        Input = [ValueSubstitute,Value]
        """
        for i in self.Script[KeyValue][KeyValue]:
            if(str(type(i)) == "<class 'dict'>"):
                for x in i:
                    key_val = list(i.keys())
                    try:
                        self.Events[key_val[0]]
                        for y in i[x]:
                            
                            if(str(type(y)) == "<class 'dict'>"):
                                if(input!=None):
                                    for in_i in input:
                                        val = i[x][1].get(in_i[0])
                                        if val is not None:
                                            i[x][1][in_i[0]] = in_i[1]
                                func= getattr(self.Events[key_val[0]][2],self.Events[key_val[0]][1])
                                func(i[x])
                    except Exception as e:
                        ...
                    
    def CreateEvent(self,tag,parans,event,classBase):
        """_summary_
        Returns:
        _type_: _description_
        """
        self.Events[tag] = [parans,event,classBase]


