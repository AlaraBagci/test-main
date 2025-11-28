from build_connection import BuildConnection
db = BuildConnection()

class TableDefinition:
    def __init__(self):
        self.conn, self.cursor = db.make_connection()

    def create_triggers(self):
        try:
            self.cursor.execute("DROP PROCEDURE IF EXISTS check_module_roles;")
            proc_sql = """
            CREATE PROCEDURE check_module_roles(IN welfare_staff_id VARCHAR(8), IN module_staff_id VARCHAR(8))
            BEGIN
                DECLARE welfare_staff_role_check VARCHAR(20);
                DECLARE module_staff_role_check VARCHAR(20);

                SELECT role INTO welfare_staff_role_check FROM users WHERE user_id = welfare_staff_id;
                IF welfare_staff_role_check IS NULL OR welfare_staff_role_check != 'welfare_staff' THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid welfare_staff_id: user is not welfare staff';
                END IF;

                SELECT role INTO module_staff_role_check FROM users WHERE user_id = module_staff_id;
                IF module_staff_role_check IS NULL OR module_staff_role_check != 'module_staff' THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid module_staff_id: user is not module staff';
                END IF;
            END;
            """
            self.cursor.execute(proc_sql)

            self.cursor.execute("DROP TRIGGER IF EXISTS module_insert_trigger;")
            trig_insert = """
            CREATE TRIGGER module_insert_trigger
            BEFORE INSERT ON module
            FOR EACH ROW
            BEGIN
                CALL check_module_roles(NEW.welfare_staff_id, NEW.module_staff_id);
            END;
            """
            self.cursor.execute(trig_insert)

            self.cursor.execute("DROP TRIGGER IF EXISTS module_update_trigger;")
            trig_update = """
            CREATE TRIGGER module_update_trigger
            BEFORE UPDATE ON module
            FOR EACH ROW
            BEGIN
                CALL check_module_roles(NEW.welfare_staff_id, NEW.module_staff_id);
            END;
            """
            self.cursor.execute(trig_update)

            self.conn.commit()
            print("Procedure and triggers created successfully!")
            
        except Exception as e:
            print(f"Error creating triggers: {e}")

    def table_definition(self):
        try:
            self.cursor.execute("CREATE TABLE course(`course_id` varchar(6) PRIMARY KEY, `course_name` varchar(100) NOT NULL);")
            self.cursor.execute("CREATE TABLE student (`stud_id` varchar(8) PRIMARY KEY, `stud_name` varchar(30) NOT NULL, `year` INT NOT NULL, `email` varchar(40), `course_id` varchar(6) ,`hash_pass` varchar(20) NOT NULL, FOREIGN KEY (course_id) REFERENCES course(course_id) ON UPDATE CASCADE ON DELETE CASCADE );")
            self.cursor.execute("CREATE table users(`user_id` varchar(8) PRIMARY KEY, `user_name` varchar(30) NOT NULL, `role` ENUM ('module_staff','welfare_staff','admin') NOT NULL, `email` varchar(40) , `hash_pass` varchar(20) NOT NULL );")
            self.cursor.execute("CREATE TABLE module (`mod_id` varchar(8) PRIMARY KEY, `mod_name` varchar(100) NOT NULL, `course_id` varchar(6), `year` INT, `welfare_staff_id` varchar(8), `module_staff_id` varchar(8), FOREIGN KEY (welfare_staff_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE ,FOREIGN KEY (module_staff_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,FOREIGN KEY (course_id) REFERENCES course(course_id) ON UPDATE CASCADE ON DELETE CASCADE);")
            self.cursor.execute("CREATE TABLE attendance (`week_no` INT, `mod_id` varchar(8), `stud_id` varchar(8) , `att_per` DECIMAL(5,2) , UNIQUE KEY unique_stu_att_per_week(week_no, mod_id, stud_id), FOREIGN KEY (stud_id) REFERENCES student(stud_id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (mod_id) REFERENCES module(mod_id) ON UPDATE CASCADE ON DELETE CASCADE);")
            self.cursor.execute("CREATE TABLE surveys (`sur_id` INT PRIMARY KEY, `week_no` INT, `stud_id` varchar(8), `mod_id` varchar(8), `stress_levels` INT CHECK(`stress_levels` > 0 AND `stress_levels` <=5), `hours_slept` DECIMAL(3,1) CHECK(`hours_slept` < 24), `comments` varchar(200) DEFAULT 'NO COMMENTS', UNIQUE KEY unique_stu_per_week (week_no, stud_id, mod_id), FOREIGN KEY (stud_id) REFERENCES student(stud_id) ON UPDATE CASCADE ON DELETE CASCADE, FOREIGN KEY (mod_id) REFERENCES module(mod_id) ON UPDATE CASCADE ON DELETE CASCADE);")
            self.cursor.execute("CREATE TABLE deadlines (`dead_id` INT PRIMARY KEY, `mod_id` varchar(8) , `week_no` INT, `ass_name` varchar(100) DEFAULT 'Assessment', `due_date` DATE, FOREIGN KEY (mod_id) REFERENCES module(mod_id) ON UPDATE CASCADE ON DELETE CASCADE);")
            self.conn.commit()
            print("Tables created successfully !!")
            self.create_triggers()
        except Exception as e:
            print("ERROR: ",e)

