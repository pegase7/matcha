import psycopg2 as p
import matcha.config
import logging
from matcha.orm.reflection import ListField, ModelDict, ModelObject

"""
Append member to value whith prefix, returning value
    if first equal true append firstprefix otherwise otherprefix, then concatenate member
    return False (for first), concatenated strings   
"""
def appendif(first, value, member, firstprefix, otherprefix):
    if first:
        return False, ('' if value is None else value) + firstprefix + member
    else:
        return False, value + otherprefix + member


class Query():
    """
    Class Query for buildinq a sql command from parameters list
    """
    def __init__(self, model, leftjoins, conditions, whereaddon, orderby):
        self.model = model
        self.leftjoins = leftjoins
        self.conditions = conditions
        self.orderby = orderby
        self.whereaddon = whereaddon
    
    """
    get formatted condition from raw condition
    """
    def get_condition(self, condition):
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
    
    """
    Build where clause from conditions
    """
    def build_where(self, conditions):
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
    
    """
    Build query
        - return query string and tuple of parameters
    """
    def build_query(self):
        model_name  = self.model.name
        self.suffix = model_name[0]
        query = "select "
        from_clause = " from " + self.model.name + ' ' + self.suffix
        first = True
        model = ModelDict().get_model(model_name)
        for field in model.get_fields():
            if not isinstance(field.type, ListField):
#                query += (" " if first else ", ") + self.suffix + '.' + field.name
                first, query = appendif(first, query, self.suffix + '.' + field.name, ' ', ', ')
        """
        leftjoin--> 0:fieldName, 1:suffix, 2:join model, 3:ManyToOne field 
        """
        for leftjoin in self.leftjoins:
            field = leftjoin[3]          
            from_clause += " left outer join " + field.type.modelname + ' ' + leftjoin[1]
            for field in leftjoin[2].get_fields():
                if not isinstance(field.type, ListField):
                    query += ", " + leftjoin[1] + '.' + field.name
                    if field.type.iskey:
                        from_clause += " on " +self.suffix + '.' + leftjoin[0] + ' = ' + leftjoin[1] + '.' + field.name
        query += from_clause
        where_clause, parameters = self.build_where(self.conditions)
        if not self.whereaddon is None:
            _, where_clause = appendif(where_clause is None, where_clause, self.whereaddon[0], " where ", " and ")
            size = len(self.whereaddon)
            for i in range(1,size):
                parameters += (self.whereaddon[i],)
        if not where_clause is None:
            query += where_clause
        if not self.orderby is None:
            query += ' order by ' + self.orderby
        logging.debug("query:" + query)
        return query, parameters

"""
    Class DataAccess
    ----------------
"""
class DataAccess():
    """
    Singleton DataAccess class provides:
        - get_connection ->    connection
        - sql:      ->    Populate model object from record of result set
        - fetch:         ->    fetch model object from database with jointures according to conditions and order by clause
        - merge:         ->    Update database object from model object
        - persist:       ->    Insert database object from model object
        - remove:        ->    Delete database object corresponding to model object
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
            postgresql = matcha.config.config['postgresql']
            DataAccess.__connection = p.connect(host=postgresql['host'], database=postgresql['database'], user=postgresql['user'], password=postgresql['password'])
            DataAccess.__instance = object.__new__(cls)
        return DataAccess.__instance

    def populate(self, record, model, start):
        modelobject = model.new_instance()
        i = start
        for field in model.get_fields():
            if not isinstance(field.type, ListField):
                setattr(modelobject,field.name,record[i])
                i += 1
        return (modelobject, i)
    
    def get_model(self, record):
        model_name = type(record).get_model_name()
        return ModelDict().get_model(model_name), model_name
        
    def set_elements(self, record, listfieldname):
        (model, _) = self.get_model(record)
        listfield = model.get_field(listfieldname)
        setjoin = (listfieldname, listfieldname[0].upper(), ModelDict().get_model(listfield.type.modelname), listfield)
        setattr(record, listfieldname, self.get_elements(model.get_id(record), setjoin))
        
    def get_elements(self, _id, setjoin):
        """
        setjoin--> 0:fieldName, 1:suffix, 2:join model, 3:Set field 
        """
        objects = []
        logging.debug("Excecute:" + setjoin[3].type.select)
        with DataAccess.__connection.cursor() as cursor:            
            cursor.execute(setjoin[3].type.select, (_id,))
            records = cursor.fetchall()
            for record in records:
                (modelobject, _) = self.populate(record, setjoin[2], 0)
                objects.append(modelobject)
        return objects;

    def get_model_attr(self, record, field):
        attr = getattr(record, field.name)
        if isinstance(attr, ModelObject):
            fieldmodel = ModelDict.get_model(self, field.type.modelname)
            attr = fieldmodel.get_id(attr)
        return attr

    def __fetch_records(self, model, leftjoins, conditions, whereaddon, orderby):
        query, parameters = Query(model, leftjoins, conditions, whereaddon, orderby).build_query()
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            records = cursor.fetchall()
            return records

    def fetch(self, model_name, joins=[], conditions=[], whereaddon=None, orderby=None):
        model = ModelDict().get_model(model_name)
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
                joinModel = ModelDict().get_model(model.get_field(join_name).type.modelname)
                joinfield = model.get_field(join_name)          
                leftjoin = (join_name, suffix, joinModel, joinfield)
                if not isinstance(joinfield.type, ListField):
                    leftjoins.append(leftjoin)
                else:
                    setjoins.append(leftjoin)
            except (ValueError) as e:
                logging.error("Bad jointure '"+ join_name +"' for class " + model.name + ": " + str(e))
        records = self.__fetch_records(model, leftjoins, conditions, whereaddon, orderby)
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

    def find(self, model_name, joins=[], conditions=[], orderby=None):
        objects = self.fetch(model_name, joins, conditions, orderby)
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
        logging.debug("Excecute:" + cmd)
        with DataAccess.__connection.cursor() as cursor:
            cursor.execute(cmd, parameters)
            if not record is None:
                updatedrecord = cursor.fetchone()
                i = 0
                for field in model.get_fields():
                    if field.type.iskey or field.type.iscomputed:
                        setattr(record,field.name,updatedrecord[i])
                    i += 1
                returnvalue = record
            else:
                returnvalue = None
            if autocommit:
                self.commit()
            return returnvalue
        
    def merge(self, record, autocommit=True):
        model, model_name = self.get_model(record)
        print('Model:', type(model))
        model.pre_merge(record)
        cmd = "update " + model_name + " set"
        addon = ' '
        parameters = tuple()
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed and not isinstance(field.type, ListField):
                cmd += addon + field.name + " = %s"
                addon = ', '
                parameters += (self.get_model_attr(record,field),)
            elif 'last_update' == field.name and field.type.iscomputed:
                cmd += addon + "last_update = DEFAULT"
        key_field = model.get_key_field().name
        cmd += ' where ' +  key_field + ' = ' + str(getattr(record, key_field)) + ' returning *'
        self.execute(cmd, parameters, model, record, autocommit=autocommit)
                   
    def persist(self, record, autocommit=True):
        model, model_name = self.get_model(record)
        model.pre_persist(record)
        cmd = "insert into " + model_name
        columns = ''
        values = ''
        addon = '('
        parameters = tuple()
        for field in model.get_fields():
            if not field.type.iskey and not field.type.iscomputed and not isinstance(field.type, ListField):
                columns += addon + field.name
                values += addon + '%s'
                parameters += (self.get_model_attr(record,field),)
                addon = ', '
        cmd += columns + ') values ' + values + ') returning *'
        self.execute(cmd, parameters, model, record, autocommit=autocommit)

    def remove(self, record, autocommit=True):
        model, model_name = self.get_model(record)
        model.pre_remove(record)
        key_field = model.get_key_field()
        parameters = (self.get_model_attr(record,key_field),)
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
            logging.debug("procedure: " + cmd)
            cursor.execute(cmd, parameters)
            if autocommit:
                self.commit()
        
    def commit(self):
        DataAccess.__connection.commit()

