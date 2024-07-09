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
        """ReadXml
                this function read XML choosed.
            _type_: Xml
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
        """ReturnScrip
                    this function returns script where only keyvalue = true
                _type_: "Return"
            """
        if(index == None):
            return self.Script[Keyvalue][Keyvalue]
        else:
            if(att!= None):
                return self.Script[Keyvalue][Keyvalue][index][att]    
            return self.Script[Keyvalue][Keyvalue][index]

    def ExecuteScript(self,KeyValue,input=None):
        """ExecuteScript
        Execute: this function execute keyvalue 
        _type_: execute

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
        """CreateEvent
        Create: create tags, parameters, events and Baseclass
        _type_: Create
        """
        self.Events[tag] = [parans,event,classBase]

    def RegisterTag(self,tag,attrs=None):
        # Criação de registro de TAG ( se estiver fora do Esquema retornar uma mensagem de erro)  E campos obrigatorios na TAG do esquema
        # RegisterTag(TagName,attrs=[])
        #AINDA VOU IMPLEMENTAR ISSO.
        ...


    def NewNode(self,tagTarget,tag,content,attr=None):
        """_summary_
        Returns:
        _type_: _description_
        """
        xm_doc = xml.parse(self.Doc)
        xm_root = xm_doc.getroot()

        node_ = xm_root.find(tagTarget)
        if node_ is None:
            raise ValueError("Node dont find in XML.")
        
        node_new = xml.Element(tag)
        node_new.text = content

        if attr:
            for key,value in attr.items():
                node_new.set(key,value)

        node_.append(node_new)
        xm_doc.write(self.Doc,encoding="utf-8",xml_declaration=True)

    def UpdateNode(self,TagTarget,value,attr=None):
        """_summary_
        Returns:
        _type_: _description_
        """
        xm_doc = xml.parse(self.Doc)
        xm_root = xm_doc.getroot()

        node_s = xm_root.find(TagTarget)
        if node_s is None:
            raise ValueError("Node dont find in XML.")
        
        node_s.text = value

        if(attr!=None):
            for key,valor in attr.items():
                node_s.set(key,valor)

        xm_doc.write(self.Doc,encoding="utf-8",xml_declaration=True)

    def DeleteNode(self,TagTarget):
        """_summary_
        Returns:
        _type_: _description_
        """
        xm_doc = xml.parse(self.Doc)
        xm_root = xm_doc.getroot()

        no_find = xm_root.find('.//' + TagTarget)
        if no_find is None:
            raise ValueError("Node not found in XML.")

        no_pai = xm_root.find('.//' + TagTarget + '/..')
        if no_pai is None:
            raise ValueError("Parent node not found in XML.")
        
        no_pai.remove(no_find)
        xm_doc.write(self.Doc,encoding="utf-8",xml_declaration=True)

    def NewXml(self,ParentName,nodes,xmlOutputName):
        """_summary_
        Returns:
        _type_: _description_
        """
        xm_elem  = xml.Element(ParentName)
        
        for key,value in nodes.items():
            sub_xm = xml.SubElement(xm_elem,key)
            sub_xm.text = str(value)
        
        xm_tree = xml.ElementTree(xm_elem)

        xm_tree.write(xmlOutputName,encoding="utf-8",xml_declaration=True)
        return xmlOutputName


