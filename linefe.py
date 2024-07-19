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
        self.FuncXmlScripts = {}
        self.root_base = ["root","data"]
        self.ReadXml()


    def ReadXml(self):
        """ReadXml
                this function read XML choosed.
            _type_: Xml
        """
        self.LoadScriptXml(self.Doc)


    def LoadScriptXml(self,XmlFile,type="script"):
        file = self.__LoadPackages(XmlFile)
        if(type=="script"):
            self.Script["main"] = file
        else:
            self.FuncXmlScripts["cod"] = file

    def ScriptXml(self,XmlScript):
        self.LoadScriptXml(XmlScript,"noscript")

    def __LoadPackages(self,XmlFile):
        tree_xml = xml.parse(XmlFile)
        root = tree_xml.getroot()

        def read_node(elements, list_node):
            for child in elements:
                transform = xml.tostring(child,encoding="unicode")
                list_node.append(transform)

        all_nodes = []

        read_node(root, all_nodes)

        return all_nodes



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

    def RunProject(self):
        """_summary_
        Returns:
        _type_: _description_
        """
        #Rodar o projeto do cliente todo por aqui
        class TranspilerXML(Linefe):
            def __init__(self, docBase) -> None:
                super().__init__(docBase)
                self.BaseScript = docBase
                self.CallBacksEvents = None
                self.functions = []
                self.xmlFiles_databases = []
                self.xmlFiles_packs = []
                self.GetValues = []
                self.varsXml = {}

            def ReturnInputs(self,list_target,TypeVal):
                for i in list_target:
                    if('type="'+TypeVal+'"'in i):
                        value = i.strip().split("file=")
                        for i_v in value:
                            if(".xml" in i_v):
                                i_v =i_v.replace('"',"")
                                i_v = i_v[:-2]
                                if(TypeVal == "xml"):
                                    self.xmlFiles_databases.append(i_v)
                                else:
                                    self.xmlFiles_packs.append(i_v)

            def CopilerXmlValues(self):
                #Get all XMl files
                AllReadFiles = self.SelectNode("read").replace("<","").split(">")
                self.ReturnInputs(AllReadFiles,"xml")
                self.ReturnInputs(AllReadFiles,"pack")
                return self.Doc

            def GetValuesXml(self):
                element = xml.fromstring(self.SelectNode("get")).get("node")
                for nodes_xml in self.xmlFiles_databases:
                    self.Doc = nodes_xml
                    self.ReadXml()
                    self.GetValues.append(self.SelectNode(element))

            def NewNodeXml(self):
                self.Doc = self.BaseScript
                self.ReadXml()
                element = xml.fromstring(self.SelectNode("new"))
                value = element.get("text")
                attr_val = element.get("attr")
                node_name = element.get("name")

                if("$![" in value):
                    value = self.varsXml[value.replace("$![","").replace("]","")][0]

                if(attr_val != None):
                    attr_val = attr_val.split(",")
                    result_node = "<"+node_name
                    for i in attr_val:
                        i = i.split(":")
                        result_node += ' '+i[0].replace("@","")+'="'+i[1]+'"'
                    result_node+=">"+value+"</"+node_name+">"
                    self.GetValues.append(result_node)
                else:
                    self.GetValues.append("<"+node_name+">"+value+"</"+node_name+">")

            def NewVarXml(self):
                self.Doc = self.BaseScript
                self.ReadXml()
                varValue_ = xml.fromstring(self.SelectNode("var"))
                value_var = varValue_.get("value")
                type_var = varValue_.get("type")
                name_var = varValue_.get("name")

                self.varsXml[name_var] = [value_var,type_var]

            def OutValues(self,rootKeys):
                self.Doc = self.BaseScript
                self.ReadXml()
                OutValue_ = xml.fromstring(self.SelectNode("out")).get("type")
                if(OutValue_ == "console"):
                    for i in self.GetValues:
                        print(i)
                    return self.GetValues
                else:
                    root = xml.Element(rootKeys[0])

                    for xml_s in self.GetValues:
                        try:
                            xml_s = xml_s.strip()
                            element_root = xml.fromstring("<"+rootKeys[1]+">"+xml_s+"</"+rootKeys[1]+">\n")
                            root.append(element_root)
                        except xml.ParseError as e:
                            print(f"Erro ao analisar o XML: {e}")
                            continue

                    tr_fy = xml.ElementTree(root)
                    
                    with open(OutValue_, "wb") as file:
                        tr_fy.write(file, encoding="utf-8", xml_declaration=True)



        obj = TranspilerXML(self.Doc)
        obj.CopilerXmlValues()
        obj.NewVarXml()
        obj.GetValuesXml()
        obj.NewNodeXml()
        obj.OutValues(self.root_base)

    def SelectNode(self,nodepath,attr=None,value=None,text=False):
        x_tree = xml.parse(self.Doc)
        x_root = x_tree.getroot()
        Results_list = ""

        if attr is not None and value is not None:
            result = x_root.findall(f".//{nodepath}[@{attr}='{value}']")
        else:
            result = x_root.findall(f".//{nodepath}")

        for elem in result:
            Results_list += xml.tostring(elem, encoding='unicode')
        return Results_list

    def SelectResultNode(self,xmlObject,node):

        value_return = xmlObject.findall(f".//{node}")
        value_doc = ""
        for i in value_return:
            value_doc+= xml.tostring(i,encoding="unicode")
        return value_doc

    def TransformStringToXml(self,XmlValue):

        value = xml.ElementTree(xml.fromstring(XmlValue))
        return value.getroot()
