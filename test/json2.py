import json
from datetime import datetime
 
  
class Student(object):
    def __init__(self, first_name: str, last_name: str, note: float, created: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.note= note
        self.created = created
  
  
class Team(object):
    def __init__(self, students: []):
        self.students = students
  
if __name__ == '__main__':  
    student1 = Student(first_name="Geeky", last_name="Guy", note=10.5, created=datetime.now())
    student2 = Student(first_name="GFG", last_name="Rocks", note=12.4, created=datetime.now())
    team = Team(students=[student1, student2])
   
    print(dir(student1.created))
    print('Student1:', student1.__dict__)
       
    # Serialization
    json_data = json.dumps(team, default=lambda o: o.__dict__, indent=4)
    print(json_data)
      
    # Deserialization
    decoded_team = Team(**json.loads(json_data))
    print(decoded_team.students[0])