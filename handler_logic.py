#-*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
                                  

class Pupil_mark():
    def __init__(self, classroom, key_uid_code, sql_conn):
        self.stamp = datetime.now()
        self.day = self.stamp.isoweekday()
        print "Day: ",self.day
        print classroom
        #print key_uid_code
        self.sql = sql_conn
        self.classroom = classroom
        self.key_uid = key_uid_code
        self.group_id = None
        self.group_name = ""
        self.TIME_FOR_CHECK = 5
        self.lesson_schedule = self.get_lesson_schedule()
        #print "Lesson schedule: ", self.lesson_schedule
        self.current_lesson = self.find_lesson_number()
		
        #прапорець позначає наявність учня у БД
        self.is_ready = False  
        self.pupil_info = self.get_pupil()
        #print self.pupil_info
        self.pupil_id = ""
        if len(self.pupil_info)!=0:
            self.pupil_id = self.pupil_info[0][0]
            self.is_ready = True
        print self.pupil_info
        print "Lesson num: ", self.current_lesson
        self.is_on_schedule = False
        if self.current_lesson:
            if self.verify_group_schedule()==True:
                self.is_on_schedule = True
    
    def get_pupil(self):
        query = self.sql.select("""SELECT pupils.pupil_id, name, surname FROM pupils 
                                   INNER JOIN tags on pupils.pupil_id = 
                                                      tags.pupil_id
                                   WHERE tags.key_code = ?;
                                """, int(self.key_uid))
        return query
    def get_lesson_schedule(self):
        """Повертає список кортежів у вигляді
        [(lesson_number, begin_time, end_time)]
        """
        lesson_schedule = self.sql.select(
                          """SELECT lesson_number, begin_time, end_time
                             FROM lesson_time;
                          """)
        return lesson_schedule

    def find_lesson_number(self): 
        """Повертає словник виду
        {"begin" : int, "end": None} з номером уроку , 
        який підходить під час спрацювання мітки, 
        і нічого, якщо такого уроку немає за розкладом
        """
        if self.day>5: 
            return None 
        # Кількість хвилин для правильної відмітки до уроку і після  
        delta = timedelta(minutes=self.TIME_FOR_CHECK)
        for lesson in self.lesson_schedule:
            lesson_begin = lesson[1].split(':')
            lesson_end = lesson[2].split(':')
            # Формування часу початку і кінця уроку в форматі datetime
            schedule_begin = self.stamp.replace(hour=int(lesson_begin[0]), 
                                    minute=int(lesson_begin[1]))
            schedule_end = self.stamp.replace(hour=int(lesson_end[0]), 
                                    minute=int(lesson_end[1]))
            #print "Begin: ", self.stamp>(schedule_begin-delta)
            #print "B2: ", self.stamp<(schedule_begin+delta)
            if self.stamp>(schedule_begin-delta) and self.stamp<(schedule_begin+delta):
                return {"begin" : int(lesson[0]), "end": None}
            elif self.stamp>(schedule_end-delta) and self.stamp<(schedule_end+delta):
                return {"begin": None, "end" : int(lesson[0])}
        return None

    def verify_group_schedule(self):
        query = self.sql.select("""SELECT p.group_id, t.group_name FROM pupils as p
                                   INNER JOIN groups as t
								   ON p.group_id=t.group_id
                                   WHERE pupil_id = ?;
                                """, self.pupil_id) 
        if query == []:
            return False
        if not self.current_lesson: 
            return False
        self.group_name = query[0][1]
        self.group_id = query[0][0]
        if self.current_lesson["begin"]:
            lesson_num = self.current_lesson["begin"]
        elif self.current_lesson["end"]:
            lesson_num = self.current_lesson["end"]
        #print "Cabinets",query 
        query = self.sql.select("""SELECT classroom_name FROM schedule
                                    INNER JOIN classrooms ON 
                                    schedule.classroom_id = classrooms.classroom_id
                                    WHERE schedule.group_id = ? 
                                    AND schedule.day_number = ?
                                    AND schedule.lesson_number = ?;
                                    """, self.group_id, self.day, 
                                    lesson_num)
        if query == []:
            return False
        classroom_rfid = query[0][0]
        #print classroom_rfid
        #print self.classroom
        if str(classroom_rfid) == str(self.classroom):
            #print "Insert"
            if self.current_lesson["begin"]:
                self.sql.update_insert("""INSERT OR IGNORE INTO presence 
                                      (pupil_id, _date, lesson_number, 
                                      presence, first_mark)
                                      VALUES (?,?,?,?,?);
                                   """, self.pupil_id, self.stamp.date(),
                                        lesson_num , 0, 1)
            elif self.current_lesson["end"]:
                self.sql.update_insert("""UPDATE presence
                                       SET presence=1
                                       WHERE pupil_id=?
                                       AND   _date=?
                                       AND   lesson_number=?
                                       """,self.pupil_id, 
                                           self.stamp.date(), lesson_num)
            
            return True
        return False




        

