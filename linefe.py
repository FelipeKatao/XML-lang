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
        _type_: Execute

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
        """NewNode
        Create: Create new element > tag, tagTarget and content 
        _type_: Create
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
        """UpdateNode
        Update: this function updated on tagtarget and values .
        _type_:Update
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
        """DeleteNode
        Delete: this function delete tagtargets
        _type_: Delete
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
        """NewXml
        CreateNewXml: this function created new XmlArchive
        _type_: Xml
        """
        xm_elem  = xml.Element(ParentName)
        
        for key,value in nodes.items():
            sub_xm = xml.SubElement(xm_elem,key)
            sub_xm.text = str(value)
        
        xm_tree = xml.ElementTree(xm_elem)

        xm_tree.write(xmlOutputName,encoding="utf-8",xml_declaration=True)
        return xmlOutputName
    
    def ImportsXml(self,NewXmlName,ParentNodeName,base_path="."):
        """_summary_
        Returns:
        _type_: _description_
        """
        return self.__include__xml(NewXmlName,ParentNodeName,base_path)    

    def __include__xml(self,NewXmlName,ParentNodeName,base_path="."):
        element_t = xml.parse(self.Doc)
        element = element_t.getroot()
        xi_include_tag = '{http://www.w3.org/2001/XInclude}include'
        for elem in element.findall('.//' + xi_include_tag):
            href = elem.attrib.get('href')
            if href:
                included_tree = xml.parse(f"{base_path}/{href}")
                included_root = included_tree.getroot()
                
                # Find parent element
                parent_map = {c: p for p in element.iter() for c in p}
                parent = parent_map.get(elem)
                
                if parent is not None:
                    index = list(parent).index(elem)
                    parent.remove(elem)
                    for child in included_root:
                        parent.insert(index, child)
                        index += 1
        element_t.write(NewXmlName,encoding='utf-8', xml_declaration=True)
        self.__modifyRootName(ParentNodeName)
        return xml.dump(element)
    
    def __modifyRootName(self,newRootName):
        t_xml = xml.parse(self.Doc)
        old_xml = t_xml.getroot()

        new_xml =  xml.Element(newRootName)

        for child in old_xml:
            new_xml.append(child)

        new_xml.attrib = old_xml.attrib
        new_t = xml.ElementTree(new_xml)

        new_t.write(self.Doc, encoding="utf-8", xml_declaration=True)

    def IncludeXml(self,pathXml,fileImport):
        """_summary_
        Returns:
        _type_: _description_
        """
        xm_tre =xml.parse(self.Doc)
        xm_root = xm_tre.getroot()

        xml.register_namespace("xi","http://www.w3.org/2001/XInclude")
        xi_include = xml.Element("{http://www.w3.org/2001/XInclude}include",href=fileImport)

        target_node = xm_root.find(pathXml)
        if target_node is not None:
            target_node.append(xi_include)
        else:
            raise IndexError("Node don't find")
        
        xm_tre.write(self.Doc,xml_declaration=True, encoding="UTF-8")
