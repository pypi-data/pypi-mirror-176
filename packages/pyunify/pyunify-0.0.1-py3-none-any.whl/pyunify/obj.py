class Obj:

  def __init__(self, json={ "meta":{}, "data":[], "concepts":{}, "compute":[], "custom":{}}):
    
    self.json = dict(json)

    self._init_blank_meta = {
        "contract":"https://github.com/JSON-UNIFY",
        "description": None,
        "source": None,
        "tags": None,
        "authors": None,
        "id": None,
        "contact": None        
    }

    if "meta" not in self.json:
      self.json["meta"] = self._init_blank_meta
    else:
      self.meta_setInitValues()
    
    if "compute" not in self.json or self.json['compute'] == []:      
      self.json["compute"] = [
          ['STATE', 'VALUE', 'LISTENER', 'EVENT', 'DESCRIPTION'],
          ['NUM_ROWS', None, None, None, 'The number of rows in the dataset'],
          ['NUM_COLUMNS', None, None, None, 'The number of columns in the dataset'],
          ['DATE_CREATED', None, None, None, 'The date this object was created'],
          ['DATE_MODIFIED', None, None, None, 'The date his object was last modified'],          
      ]    
      

    if "data" not in self.json:
      self.json["data"] = []
      self.data_initFromConcepts()

    if "concepts" not in self.json:
      self.json["concepts"] = {"columns":{}}
      self.concepts_initFromData()

    if 'concepts' in self.json == {} and self.json['data'] != []:      
      self.concepts_initFromData()
    
    if 'custom' not in self.json:
      self.json['custom'] = {}

    req_keys = list(self.json)
    for key in req_keys:      
      if key != "meta" and key != 'concepts' and key != 'data' and key != 'custom' and key != 'compute':
        print("Init object \033[91mDOES NOT\033[0m meet requirements. Only 'meta', 'concepts', 'data', 'custom', and 'compute allowed.\n")
        print('key:', key,'\nvalue: ',self.json[key], '\n')

    self._init_dependencies()
    #self.compute_setNumRows()
  
  #def compute_setNumRows(self):
    #num_rows = self.json['data'].len() - 1
    #print(num_rows)


  def format(self, style):
    if style == 'italic':
      return '\033[3m'
    elif style == 'default':
      return '\033[0m'
    elif style == 'bold':
      return'\033[1m'

  def _init_dependencies(self):
    import pandas as pd
    self.pd = pd
    self.pd.set_option('max_colwidth', 1024)    

  def meta_setInitValues(self):
    meta = self.json['meta']
    for key in self._init_blank_meta:
      if key not in meta:
        meta[key] = self._init_blank_meta[key]

  def data_initFromConcepts(self):
    row = []
    for concept in self.json['concepts']['columns']:
      row.append(concept)
    self.json['data'].append(row)

  def concepts_initFromData(self):
    #for each column in data, add a key, type, and description in concepts
    for column_name in self.json['data'][0]:
      self.json['concepts']['columns'][column_name] = {
          "type":{},
          "description":{}
      }

  def __str__(self):    
    return str(self.json)

  def __repr__(self):    
    return str(self.json)  

  def concepts(self, concepts=None):
    if concepts == None:
      return self.json['concepts']
    else:
      self.json['concepts'] = concepts

  def data_getColumnNumber_byColumnName(self, columnName):
    data = self.json['data']
    columns = data[0]
    
    col_num = columns.index(columnName)
    return col_num

  def data_getRows_byColumnNumber(self, col_num):
    data = self.json['data']
    column = []
    for row in data:
      cell = row[col_num]
      column.append(cell)
    column.pop(0)
    return column

  def meta(self, meta=None):    
    if meta != None:      
      self.json['meta'] = meta
    else:
      return self.json['meta']
  
  def compute(self, compute=None):    
    if compute != None:      
      self.json['compute'] = compute
    else:
      return self.json['compute']
  
  
  
  

  def pandas_format_cell_style_by_string_match(self, val, str_to_match, params):        
    retVal = ''
    if val == str_to_match:
      props = list(params.keys())
      for prop in props:
        retVal += "{0}:{1}; ".format(prop, params[prop])    
    return retVal
    

  
  def columnNames(self):
    if 'columns' in self.json['concepts']:
      col_names = list(self.json['concepts']['columns'].keys())
      return col_names
    else:
      #print('No columns defined in "concepts" key')
      return []

  def describeColumn(self, name):
    col_desc = None    
    col_desc = self.json['concepts']['columns'][name]['description']
    return col_desc

  def getColumnDesriptionRow(self, col):
    row = []
    col_name = col
    col_type = None
    col_desc = None
    columns = self.json['concepts']['columns']
    if col in columns:
      if 'type' in columns[col]:
        col_type = columns[col]['type']        
      if 'description' in columns[col]:
        col_desc = columns[col]['description']          
    row.append(col_name)
    row.append(col_type)
    row.append(col_desc)
    return row

  def getDataConcepts(self):                
    cols = self.columnNames()
    rows = []
    for col in cols:            
      row = self.getColumnDesriptionRow(col)          
      rows.append(row)          
    return rows

  def getMetadataData(self):
    keys = list(self.json['meta'].keys())
    rows = []
    for key in keys:            
      row = [key, self.json['meta'][key]]
      rows.append(row)          
    return rows

  
    
  
  def concept(self, column_name, params):        
    key = list(params.keys())[0]
    self.json['concepts']['columns'][column_name][key] = params[key]
  
  def concept_highlight(self, key):
    return self.concepts_toTable(key, {'color':'blue', 'font-weight':'bold'})
  
  def concepts_toTable(self, string_to_match=None, new_params=None):
    data = self.getDataConcepts()        
    df = pd.DataFrame(data, columns=['Column Name', 'Type', 'Description'])    
    if new_params != None:                  
      df = df.style.applymap(self.pandas_format_cell_style_by_string_match, str_to_match = string_to_match, params = new_params)    
    return df

  

  #will analyze concepts for 'description' and report missing keys
  def concepts_validate_descriptions(self):
    true_count = 0
    false_count = 0
    print("\n\033[0m\033[1mCHECKING 'Description' PROPERTY IN CONCEPTS...\n")
    cols = self.json['concepts']['columns']
    for concept_name in cols:
      concept = cols[concept_name]           
      if 'description' in concept:
        msg = "\033[0m{0}: \033[92m\033[1mTrue".format(concept_name)                
        print(msg)
        true_count = true_count+1
      else:
        msg = "\033[0m{0}: \033[91m\033[1mFalse".format(concept_name)        
        print(msg)
        false_count = false_count+1
    print("\n\033[0m\033[3m'Description' property DOES exist in {0} columns, 'Description' property DOES NOT exist in {1} columns\n".format(true_count, false_count))

  #will analyze concepts for 'types' and report missing keys
  def concepts_validate_types(self):
    true_count = 0
    false_count = 0
    print("\n\033[0m\033[1mCHECKING 'Type' PROPERTY IN CONCEPTS...\n")
    cols = self.json['concepts']['columns']
    for concept_name in cols:
      concept = cols[concept_name]           
      if 'type' in concept:
        msg = "\033[0m{0}: \033[92m\033[1mTrue".format(concept_name)                
        print(msg)
        true_count = true_count+1
      else:
        msg = "\033[0m{0}: \033[91m\033[1mFalse".format(concept_name)        
        print(msg)
        false_count = false_count+1
    print("\n\033[0m\033[3m'Type' property DOES exist in {0} columns, 'Type' property DOES NOT exist in {1} columns\n".format(true_count, false_count))

  #will analyze concepts for 'types' and 'description' and report missing keys
  def concepts_validate(self):
    self.concepts_validate_types()
    self.concepts_validate_descriptions()


  def help(self, type_of = None):
    if type_of == None:
      print("""        
        - \033[1mThe JSON-UNIFY Object Specification\033[0m
          - The JSON object MUST contain a 'meta', 'concepts', and 'data' key                        
        
          - \033[1mCONCEPTS\033[0m
            - \033[1mThe obj['concepts'] key MUST contain:\033[0m
              - 'columns': concept definitions for column headers
                - EACH column MUST have the following items:
                  - 'type': the type (int, string, etc.)
                  - 'description': a description of the concept
                              
            - \033[1mThe obj['concepts']['columns'] key is RECOMMENDED to contain:\033[0m
              - 'values': concept definitions for values inside a columns
              - 'uri': any knowledge base information, such as from wikidata
              - 'examples': a collection of examples
              - 'relations': a collection of relations such as
                - 'is a'
                - 'part of'
                - 'has kind'
                - 'has instance'
                - 'category domain'
                - 'has quality'
                - 'studied by'
            
            - \033[1mThe obj['concepts'] key CAN contain:\033[0m
              - 'groups': a dictionary of a group with the column names of the group
                - example: 'height', and 'width' columns can be in a group called 'physical dimensions'
                  - 'group': {
                    "dimensions": [
                      "height",
                      "width
                    ]                                          
                  }

              
          - \033[1mDATA\033[0m
            - \033[1mThe 'data' key MUST contain:\033[0m
              - data in the form of rows (an array of arrays, where the inner array represents one row)
                example - 'data': [['col1', 'col2'], [1, 3], [2, 4]] 

              - FUTURE FEATURE: data in the form of columns (an object where each key represents the column header, and each row is in an array)
                example - 'data': {'col1': [1, 2], 'col2': [3, 4]}            

          - \033[1mMETA\033[0m
            - \033[1mThe 'meta' key MUST contain:\033[0m
              - 'source': where the data came from
              - 'contract': which JSON-Unify contract is being used (see GitHub page or json-unify.org)
                - default:
                   - https://github.com/JSON-UNIFY                      
              - 'description': a description about the data set
          
            - \033[1mThe 'meta' key CAN contain:\033[0m              
              - 'authors': any author names / owner names
              - 'tags': any comma-separated tags for search
              - 'contact': any contact information (team name, person email address, etc.)
              - 'custom': anything custom 
              - 'id': a unique ID for the JSON-Unify objects 
              - 'license': any license information

          - \033[1mCOMPUTE\033[0m
            - \033[1mThe 'compute' key MUST contain:\033[0m
              - 'state': any associated state of the object's internal variables managed by the object
              - 'value': any associated value of a state of the object's internal variables managed by the object
              - 'listener': the function listening for an event
              - 'event': a boolean conditional for the event that triggers the listener's function to execute
              - 'description': what the function does
              
                

          
        - \033[1mAbout the JSON-Unify Specification\033[0m
          - GitHub: \033[94mhttps://github.com/JSON-UNIFY\033[0m
          - Website: 033[94mhttps://json-unify.org\033[0m
          - License: \033[94mhttps://www.gnu.org/licenses/gpl-3.0.en.html\033[0m
          - Contributors: Ron Itelman, Cameron Prybol, Stephanie Bankes
        
        - \033[1mAbout the JSON-Unify Implementation\033[0m
          - GitHub: \033[94mhttps://github.com/JSON-UNIFY\033[0m
          - Website: \033[94mhttps://json-unify.org\033[0m
          - License: \033[94mhttps://www.gnu.org/licenses/gpl-3.0.en.html\033[0m
          - Contributors: Ron Itelman, Cameron Prybol, Stephanie Bankes

        - \033[1mJSON-Unify Implementation API\033[0m
          - meta_validate() 
            - Description: Will analyze 'meta' top-level key and look for missing requirements
            - Parameters: None
            - Outputs: Prints text
            - Returns: None

          - concepts_validate()
            - Description: Will analyze 'concepts' top-level key and look for missing requirements
            - Parameters: None
            - Outputs: Prints text
            - Returns: None
        
        
      """)

  #will analyze 'meta' top-level key and look for missing requirements
  def meta_validate(self):
    total_req_props = 3
    has_req_props = 0
    total_rec_props = 4
    has_rec_props = 0
    has_contract = False
    has_source = False
    has_description = False
    has_authors = False
    has_license = False
    has_contact = False
    has_id = False
    print("\n\033[0m\033[1mCHECKING META...\n")
    if 'contract' in self.json['meta']:
      has_contract = True      
      has_req_props = has_req_props + 1
      msg = "\033[0mCONTRACT (required): \033[92m\033[1m{0}".format(has_contract)
    else:
      msg = "\033[0mCONTRACT (required): \033[93m\033[1m{0}".format(has_contract)
    print(msg)
    if 'source' in self.json['meta']:
      has_source = True
      has_req_props = has_req_props + 1
      msg = "\033[0mSOURCE (required): \033[92m\033[1m{0}".format(has_source)
    else:
      msg = "\033[0mSOURCE (required): \033[93m\033[1m{0}".format(has_source)
    print(msg)
    if 'description' in self.json['meta']:
      has_description = True
      has_req_props = has_req_props + 1
      msg = "\033[0mDESCRIPTION (required): \033[92m\033[1m{0}\n".format(has_description)
    else:
      msg = "\033[0mDESCRIPTION (required): \033[93m\033[1m{0}".format(has_description)
    print(msg)
    if 'authors' in self.json['meta']:
      has_authors = True 
      has_rec_props += 1     
      msg = "\033[0mAUTHOR (recommended): \033[92m\033[1m{0}".format(has_authors)
    else:
      msg = "\033[0mAUTHOR (recommended): \033[94m\033[1m{0}".format(has_authors)
    print(msg)
    if 'license' in self.json['meta']:
      has_license = True 
      has_rec_props += 1     
      msg = "\033[0mLICENSE (recommended): \033[92m\033[1m{0}".format(has_license)
    else:
      msg = "\033[0mLICENSE (recommended): \033[94m\033[1m{0}".format(has_license)
    print(msg)
    if 'id' in self.json['meta']:
      has_id = True 
      has_rec_props += 1     
      msg = "\033[0mID (recommended): \033[92m\033[1m{0}".format(has_id)
    else:
      msg = "\033[0mID (recommended): \033[94m\033[1m{0}".format(has_id)
    print(msg)
    if 'contact' in self.json['meta']:
      has_contact = True 
      has_rec_props += 1     
      msg = "\033[0mCONTACT (recommended): \033[92m\033[1m{0}".format(has_contact)
    else:
      msg = "\033[0mCONTACT (recommended): \033[94m\033[1m{0}".format(has_contact)
    print(msg)
    print("\n\033[0m\033[3m{0}/{0} required properties DO exist, {1} required properties ARE MISSING\n{2} recommended properties DO exist, {3} recommended properties ARE MISSING".format(has_req_props, total_req_props - has_req_props, has_rec_props, total_rec_props - has_rec_props))

  def pretty(self, key=None):
    import json
    if key == None:      
      j = json.dumps(self.json, indent=4)      
    else:
      j = json.dumps(self.json[key], indent=4)
    print(j)

  def table_render(self, header, df=None):    
    from IPython.display import display, HTML
    h3 = "<h3 style='margin-bottom:20px; padding-bottom:0px'>{0}</h3>".format(header)    
    empty = '<i style="margin-bottom:0px;">No {0} to display</i>'.format(header.lower())
    if not df.empty:      
      spacer = '<div style="margin-bottom:0px">&nbsp;</div>'
      display(HTML(h3), df, HTML(spacer))  
    else:      
      spacer = '<div style="margin-bottom:0px">&nbsp;</div>'
      display(HTML(h3), HTML(empty), HTML(spacer))


  def table_meta(self):    
    meta = self.getMetadataData()        
    if meta != []:                  
      df = self.pd.DataFrame(meta, columns=["Key", "Value"])         
    else:      
      df = self.pd.DataFrame()     
    self.table_render("META", df)   
      
  def table_data(self):    
    data = self.json['data']    
    if data != []:                
      df = self.pd.DataFrame(data)    
      df.columns = df.iloc[0] 
      df = df[1:] 
    else:
      df = self.pd.DataFrame()      
    self.table_render("DATA", df)                     

  def table_concepts(self):    
    data = self.getDataConcepts() 
    if data != []:                
      df = self.pd.DataFrame(data, columns=["COLUMN NAME", 'TYPE', 'DESCRIPTION'])          
    else:
      df = self.pd.DataFrame()      
    self.table_render("CONCEPTS", df)

  def table_compute(self):    
    data = self.json['compute']
    if data != []:                
      df = self.pd.DataFrame(data, columns=['STATE', 'VALUE', 'FUNCTION', 'EVENT', 'DESCRIPTION'])          
      df.columns = df.iloc[0] 
      df = df[1:] 
    else:
      df = self.pd.DataFrame()      
    self.table_render("COMPUTE", df)   

  def table_custom(self):    
    data = self.json['custom']
    if data != {}:
      df = self.pd.DataFrame(data)          
    else:
      df = self.pd.DataFrame()      
    self.table_render("CUSTOM", df)                     
             
  def table_all(self):       
    pd.set_option('max_colwidth', 1024)    
    self.table_compute() 
    self.table_concepts()    
    self.table_custom()
    self.table_data()    
    self.table_meta()
  
  def table_spec(self):       
    pd.set_option('max_colwidth', 1024)        
    self.table_concepts()        
    self.table_data()    
    self.table_meta()
    
    
  def table(self, key=None, describe=True):
    import pandas as pd
    
    if key == 'meta':
      self.table_meta()
    elif key == 'data':
      self.table_data()
    elif key == 'concepts':
      self.table_concepts()
    elif key == 'compute':
      self.table_compute()
    elif key == 'custom':
      self.table_custom()
    elif key == "all":
      self.table_all()
    elif key == None:
      self.table_spec()
      

  def test_cell(self, _type, cell, language):
    language = language.lower()

    boolean = None
    string = None

    if (language == 'python'):
      boolean = 'bool'
      string = 'str'

    if (language == 'javascript'):
      boolean = 'boolean'
      string = 'string'

    if _type == boolean:
      if type(cell) != type(True):
        print('\t\033[0m\033[91mFAIL\033[0m: {0}, expecting {1}, found {2}'.format(cell, _type, type(cell)))              
      else:
        print('\t\033[0m\033[92mPASSED\033[0m: {0}, expecting {1}, found {2}'.format(cell, _type, type(cell)))
    if _type == string:
      if type(cell) != type("string"):
        print('\t\033[0m\033[91mFAILED\033[0m: {0}, expecting {1}, found {2}'.format(cell, _type, type(cell)))
      else:
        print('\t\033[0m\033[92mPASSED\033[0m: {0}, expecting {1}, found {2}'.format(cell, _type, type(cell)))    
      

  # loops through each column, gets the type, and then loops through each value to validate the type
  def test(self, language="python"):
    concepts = self.json['concepts']['columns']
    print("\033[0mLANGUAGE\033[0m: \033[1m{0}\033[0m\n".format(language))
    for column_name in concepts:
      #get the column number of the column_name
      col_num = self.data_getColumnNumber_byColumnName(column_name)        
      #get all values in the column by column number
      column = self.data_getRows_byColumnNumber(col_num)                            
      if 'type' in concepts[column_name]:        
        _type = concepts[column_name]['type']  
        #check each value against _type
        print("\033[1m{0}".format(column_name))
        for cell in column:
          self.test_cell(_type, cell, language)
          
      else:
          print("\033[1m{0}: \t\033[0m\033[91mNo type defined for {0}\033[0m".format(column_name))                            
      print("\n")

  def validate(self):
    self.meta_validate()
    self.concepts_validate()
    