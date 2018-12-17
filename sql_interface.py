#-*- coding: utf-8 -*-

import sqlite3


class DbSchool():
    def __init__(self):
        self.connection = sqlite3.connect("rf_school.db")
        self.cur = self.connection.cursor()
        self.create_tables()
    

    def create_tables(self):    
        self.cur.execute('''CREATE TABLE IF NOT EXISTS                
                            subjects 
                            (subject_id INT PIMARY KEY,     
                            name TEXT NOT NULL);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS                
                            groups 
                            (group_id INT PRIMARY KEY,        
                            group_name TEXT NOT NULL);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS                
                            classrooms 
                            (classroom_id INT PRIMARY KEY,
                            classroom_name TEXT NOT NULL);''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS                
                            lesson_time
                            (lesson_number INT PRIMARY KEY,
                            begin_time TEXT NOT NULL,     
                            end_time TEXT NOT NULL); ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS                
                            pupils 
                            (pupil_id INT PRIMARY KEY,        
                            group_id INT,                     
                            name TEXT,                        
                            surname TEXT,                     
                            patronim TEXT,                    
                            FOREIGN KEY (group_id)            
                            REFERENCES groups(group_id)); ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS          
                            tags 
                            (tag_id INT PRIMARY KEY,       
                            key_code INT UNIQUE,                
                            pupil_id INT,                       
                            FOREIGN KEY (pupil_id)              
                            REFERENCES pupils(pupil_id)); ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS     
                            schedule 
                            (classroom_id INT NOT NULL,    
                            lesson_number INT NOT NULL,     
                            day_number INT NOT NULL,        
                            group_id INT,                   
                            subject_id INT,                 
                            PRIMARY KEY (classroom_id,      
                                         lesson_number,     
                                         day_number),       
                            FOREIGN KEY (classroom_id)      
                            REFERENCES classrooms(classroom_id),    
                            FOREIGN KEY (lesson_number)             
                            REFERENCES lesson_time(lesson_number),  
                            FOREIGN KEY (group_id)                  
                            REFERENCES groups(group_id),            
                            FOREIGN KEY (subject_id)                
                            REFERENCES subjects(subject_id)); ''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS               
                            presence
                            (pupil_id INT NOT NULL,          
                            _date TEXT   NOT NULL,          
                            lesson_number   INT NOT NULL,   
                            presence INT,  
                            first_mark INT,                 
                            PRIMARY KEY (pupil_id,          
                                        _date,             
                                        lesson_number),    
                            FOREIGN KEY (pupil_id)          
                            REFERENCES pupils(pupil_id),    
                            FOREIGN KEY (lesson_number)     
                            REFERENCES lesson_time(lesson_number));''')
        self.connection.commit()  
    
    def select(self, query, *args):
        if args:
            self.cur.execute(query, args)
        else:
            self.cur.execute(query) 
        return self.cur.fetchall()

    def update_insert(self, query, *args):
        if args:
            self.cur.execute(query, args)
        else:
            self.cur.execute(query) 
        self.connection.commit()
                            
if __name__ == '__main__':
    DbSchool()

