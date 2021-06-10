import psycopg2 as p
from matcha.config import Config
import logging
from matcha.orm.reflection import ListField, ModelDict, ModelObject


def appendif(first, value, member, firstprefix, otherprefix):
    """
    Append member to value whith prefix, returning value
        if first equal true append firstprefix otherwise otherprefix, then concatenate member
        return False (for first), concatenated strings   
    """
    if first:
        return False, ('' if value is None else value) + firstprefix + member
    else:
        return False, value + otherprefix + member


class Query():
    """
    Class Query for buildinq a sql command from parameter list
    """
    def __init__(self, model, conditions, leftjoins, whereaddon, orderby, limit):
        self.model = model
        self.conditions = conditions
        self.leftjoins = leftjoins
        self.whereaddon = whereaddon
        self.orderby = orderby
        self.limit = limit
    
    def get_condition(self, condition):
        """
        get formatted condition from raw condition
        """
        if not type(condition) is tuple:
            condition = ((condition,))
        size = len(condition)
        if 3 != size:
            if 2 == size:
                condition = (condition[0], '=', condition[1])
            elif 1 == size: 
                condition = (self.suffix + '.' + self.model.get_key_field().name, '=',) + condition
            else:
                raise ValueError("Invalid condition:" + condition)
        return condition
    
    def build_where(self, conditions):
        """
        Build where clause from conditions
        """
        if conditions is None:
            return None
        if not type(conditions) is list:
            conditions = [conditions]
        where = None
        first = True
        parameters = tuple()
        for condition in conditions:
            fcondition = self.get_condition(condition)
            member = fcondition[0] + fcondition[1] + '%s'
            parameters += (fcondition[2],)
            first, where = appendif(first, where, member, " where ", " and ")
        return where, parameters
    
    def build_query(self):
        """
        Build query
            - return query string and tuple of parameters
        """
        model_name  = self.model.name
        self.suffix = model_name[0]
        query = "select "
        from_clause = " from " + self.model.name + ' ' + self.suffix
        first = True
        model = ModelDict().get_model_class(model_name)
        for field in model.get_fields():
            if not isinstance(field, ListField):
                first, query = appendif(first, query, self.suffix + '.' + field.name, ' ', ', ')
        
        # leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        for leftjoin in self.leftjoins:
            field = leftjoin[3]          
            from_clause += " left outer join " + field.modelname + ' ' + leftjoin[1]
            for field in leftjoin[2].get_fields():
                if not isinstance(field, ListField):
                    query += ", " + leftjoin[1] + '.' + field.name
                    if field.iskey:
                        from_clause += " on " +self.suffix + '.' + leftjoin[0] + ' = ' + leftjoin[1] + '.' + field.name
        query += from_clause

        # Add conditions
        where_clause, parameters = self.build_where(self.conditions)

        # Add where addon
        if not self.whereaddon is None:
            if isinstance(self.whereaddon, str):
                self.whereaddon = (self.whereaddon, [])
            _, where_clause = appendif(where_clause is None, where_clause, self.whereaddon[0], " where ", " and ")
            if 0 < len(self.whereaddon[1]):
                if isinstance(self.whereaddon[1], list):
                    parameters += tuple(self.whereaddon[1])                
                else:
                    parameters += (self.whereaddon[1], )
 
        if not where_clause is None:
            query += where_clause
        '''
        Add order by clause
        '''
        if not self.orderby is None:
            query += ' order by ' + self.orderby
        '''
        Add limit clause
        '''
        if not self.limit is None:
            query += ' limit ' + str(self.limit)
        return query, parameters

class DataAccess():
    """
        Class DataAccess
        ----------------
    Singleton DataAccess class provides:
        - populate:     ->    Populate model object from record of result set
        - fetch:        ->    fetch model objects from database with jointures according to conditions and order by clause
        - find:         ->    fetch first model object from database with jointures according to conditions and order by clause.
                              Send warning when several or none row are returned.  
        - execute:      ->    execute one SQL order.
        - executescript ->    exeute order contained in a SQL script file
        - merge:        ->    Update database object from model object
        - persist:      ->    Insert database object from model object
        - remove:       ->    Delete database object corresponding to model object
    """
    __instance = None
    __modelDict = ModelDict()
    __connection = None
    
    """
    Check for singleton
    """
    def __new__(cls):
        """
        if previous instance is null instantiate and connect to database, elsewhere return current instance        
        """
        if DataAccess.__instance is None:
            postgresql = Config().config['postgresql']
            import base64
            cryptedpassword = postgresql['password']
            totalpassword = str(base64.b64decode(bytearray(cryptedpassword, "utf8")), "utf8")
            password = totalpassword[:int((len(totalpassword) - 6) / 2)]
            if 'loggingConnection' in postgresql:
                from psycopg2.extras import LoggingConnection
                DataAccess.__connection = p.connect(connection_factory=LoggingConnection, host=postgresql['host'], database=postgresql['database'], user=postgresql['user'], password=password)
                loggingConnection = postgresql['loggingConnection']
                logger = None
                if not loggingConnection is None:
                    logger = logging.getLogger(loggingConnection)
                    if logger is None:
                        logging.warn("No logger '" + loggingConnection + "' found. Standard logger is assumed!")
                if logger is None:
                    logger = logging.getLogger()
                DataAccess.__connection.initialize(logger)
            else:
                DataAccess.__connection = p.connect(host=postgresql['host'], database=postgresql['database'], user=postgresql['user'], password=password)

            DataAccess.__instance = object.__new__(cls)
        return DataAccess.__instance

    def populate(self, record, model, start):
        modelobject = model.new_instance()
        i = start
        for field in model.get_fields():
            if not isinstance(field, ListField):
                value = field.check(modelobject, record[i])
                setattr(modelobject,field.name,value)
                i += 1
        return (modelobject, i)
    
    def get_model_class(self, record):
        model_name = type(record).get_model_name()
        return ModelDict().get_model_class(model_name), model_name
        
    def set_elements(self, record, listfieldname):
        (model, _) = self.get_model_class(record)
        listfield = model.get_field(listfieldname)
        setjoin = (listfieldname, listfieldname[0].upper(), ModelDict().get_model_class(listfield.modelname), listfield)
        setattr(record, listfieldname, self.get_elements(model.get_id(record), setjoin))
        
    def get_elements(self, _id, setjoin):
        """
        setjoin--> 0:fieldName, 1:suffix, 2:join model, 3:Set field 
        """
        objects = []
        with DataAccess.__connection.cursor() as cursor:            
            cursor.execute(setjoin[3].select, (_id,))
            records = cursor.fetchall()
            for record in records:
                (modelobject, _) = self.populate(record, setjoin[2], 0)
                objects.append(modelobject)
        return objects;

    def __get_model_attr(self, record, field):
        try:
            attr = getattr(record, field.name)
            if isinstance(attr, ModelObject):
                fieldmodel = ModelDict().get_model_class(field.modelname)
                attr = fieldmodel.get_id(attr)
            return attr
        except (AttributeError):
            setattr(record, field, None)
            return None
            
    def __fetch_records(self, model, conditions, leftjoins, whereaddon, orderby, limit):
        query, parameters = Query(model, conditions, leftjoins, whereaddon, orderby, limit).build_query()
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            records = cursor.fetchall()
            return records

    def fetch(self, model_name, conditions=[], joins=[], whereaddon=None, orderby=None, limit=None):
        model = ModelDict().get_model_class(model_name)
        objects = []
        """
        leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        leftjoins = [] 
        setjoins = [] 
        if not type(joins) is list:
            joins = [joins]
        for join in joins:
            suffix = None
            if type(join) is tuple:
                join_name = join[0]
                suffix =  join[1]
            else:
                join_name = join
            if suffix is None:
                suffix = join_name[0].upper()
            try:
                joinModel = ModelDict().get_model_class(model.get_field(join_name).modelname)
                joinfield = model.get_field(join_name)          
                leftjoin = (join_name, suffix, joinModel, joinfield)
                if not isinstance(joinfield, ListField):
                    leftjoins.append(leftjoin)
                else:
                    setjoins.append(leftjoin)
            except (ValueError) as e:
                logging.error("Bad jointure '"+ join_name +"' for class " + model.name + ": " + str(e))
        records = self.__fetch_records(model, conditions, leftjoins, whereaddon, orderby, limit)
        for record in records:
            (modelobject, start) = self.populate(record, model, 0)
            objects.append(modelobject)
            for leftjoin in leftjoins:
                (joinobject, start) = self.populate(record, leftjoin[2], start)
                setattr(modelobject,leftjoin[0],joinobject)
            for setjoin in setjoins:
                _id = getattr(modelobject, model.get_key_field().name)
                setattr(modelobject, setjoin[0], self.get_elements(_id, setjoin))
        return objects

    def find(self, model_name, conditions=[], joins=[], whereaddon=None, orderby=None):
        objects = self.fetch(model_name, conditions, joins, whereaddon, orderby)
        size = len(objects)
        if 1 != size:
            message = ' for model object ' + model_name
            if joins:
                message += ', joins=' + str(joins)
            if conditions:
                message += ', conditions='+ str(conditions)
            if 0 == size:
                logging.debug("No record found" + message + '.')
                return None
            else:
                logging.warning("Several records found ("+ str(len(objects)) + ")" + message + '.')           
        return objects[0]
        
    def execute(self, cmd, parameters=None, model=None, record=None, autocommit=True):
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(cmd, parameters)   
            if not record is None:
                updatedrecord = cursor.fetchone()
                i = 0
                for field in model.get_fields():
                    if field.iscomputed:
                        setattr(record,field.name,updatedrecord[i])
                    i += 1
                returnvalue = record
            else:
                if cmd.startswith('select '):
                    return cursor.fetchall()
                else:
                    if autocommit:
                        self.commit()
                    return None
            return returnvalue
        
    def executescript(self, filepath):
        """
        Execute sql script contained in file 'filepath'.
        """
        logging.info("Excecute script:" + filepath)
        with DataAccess.__connection.cursor() as cursor:
            script = open(filepath,'r').read()
            cursor.execute(script)
        
    def merge(self, record, autocommit=True):
        record.check()
        model, model_name = self.get_model_class(record)
        model.pre_merge(record)
        cmd = "update " + model_name + " set"
        addon = ' '
        parameters = tuple()
        for field in model.get_fields():
            if not field.iskey and not field.iscomputed and not isinstance(field, ListField):
                cmd += addon + field.name + " = %s"
                addon = ', '
                parameters += (self.__get_model_attr(record,field),)
            elif 'last_update' == field.name and field.iscomputed:
                cmd += addon + "last_update = DEFAULT"
        key_field = model.get_key_field().name
        cmd += ' where ' +  key_field + ' = ' + str(getattr(record, key_field)) + ' returning *'
        self.execute(cmd, parameters, model, record, autocommit=autocommit)
                   
    def persist(self, record, autocommit=True):
        model, model_name = self.get_model_class(record)
        model.pre_persist(record)
        cmd = "insert into " + model_name
        columns = ''
        values = ''
        addon = '('
        parameters = tuple()
        for field in model.get_fields():
            if not field.iscomputed and not isinstance(field, ListField):
                columns += addon + field.name
                values += addon + '%s'
                parameters += (self.__get_model_attr(record,field),)
                addon = ', '
        cmd += columns + ') values ' + values + ') returning *'
        self.execute(cmd, parameters, model, record, autocommit=autocommit)

    def remove(self, record, autocommit=True):
        model, model_name = self.get_model_class(record)
        model.pre_remove(record)
        key_field = model.get_key_field()
        parameters = (self.__get_model_attr(record,key_field),)
        cmd = 'delete from ' + model_name + ' where ' +  key_field.name + ' = %s'
        self.execute(cmd, parameters, autocommit=autocommit)
        
    def call_procedure(self, procedure, parameters=None, autocommit=True):
        with DataAccess.__connection.cursor() as cursor:
            cmd = 'call '+ procedure + '('
            addon = ''
            for _ in range(len(parameters)):
                cmd += (addon +  '%s')
                addon = ', '
            cmd += ')'
            cursor.execute(cmd, parameters)
            if autocommit:
                self.commit()
        
    def commit(self):
        DataAccess.__connection.commit()

