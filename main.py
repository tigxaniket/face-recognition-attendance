############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import shutil
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import re
import json

import mysql.connector
from mysql.connector import Error

import tkinter as tk
from tkinter import ttk, messagebox as mess


# Path to save configuration file
config_file = "config.json"

# Initialize global configuration dictionary
H = {}

# Create main window
window = tk.Tk()
window.title("Face Recognition Based Attendance Monitoring System")

# Create database configuration labels and entries
label_host = tk.Label(window, text="Host", font=('Arial', 12))
label_host.grid(row=0, column=0, padx=10, pady=10)
entry_host = tk.Entry(window, width=20, font=('Arial', 12))
entry_host.grid(row=0, column=1, padx=10, pady=10)

label_user = tk.Label(window, text="Username", font=('Arial', 12))
label_user.grid(row=1, column=0, padx=10, pady=10)
entry_user = tk.Entry(window, width=20, font=('Arial', 12))
entry_user.grid(row=1, column=1, padx=10, pady=10)

label_password = tk.Label(window, text="Password", font=('Arial', 12))
label_password.grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(window, show='*', width=20, font=('Arial', 12))
entry_password.grid(row=2, column=1, padx=10, pady=10)

label_database = tk.Label(window, text="Database", font=('Arial', 12))
label_database.grid(row=3, column=0, padx=10, pady=10)
entry_database = tk.Entry(window, width=20, font=('Arial', 12))
entry_database.grid(row=3, column=1, padx=10, pady=10)

def delete_config():
    config_file = 'config.json'
    
    if os.path.exists(config_file):
        os.remove(config_file)
        mess._show(title='Success', message='Configuration deleted successfully!')
    else:
        mess._show(title='Error', message='No configuration file found!')


# Save configuration function
def save_config():
    global H
    host = entry_host.get()
    user = entry_user.get()
    password = entry_password.get()
    database = entry_database.get()

    if not all([host, user, password, database]):
        mess._show(title='Error', message='Please fill all fields!')
        return

    H = {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }

    with open('config.json', 'w') as config_file:
        json.dump(H, config_file)

    mess._show(title='Success', message='Configuration saved successfully!')



def load_config():
    global H
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            
            # Update the entry fields
            entry_host.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            entry_database.delete(0, tk.END)

            entry_host.insert(0, config.get('host', ''))
            entry_user.insert(0, config.get('user', ''))
            entry_password.insert(0, config.get('password', ''))
            entry_database.insert(0, config.get('database', ''))

            # Update global H dictionary with loaded configuration
            H = config

        mess.showinfo("Success", "Configuration loaded!")
    else:
        mess.showerror("Error", "No saved configuration to load.")

# Define the function to go to the next window
def next_window(event=None):
    # Example: Destroy the current window and open a new one
    window.destroy()

# Create buttons for saving and loading configuration
button_save_config = tk.Button(window, text="Save Configuration", command=save_config)
button_save_config.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

button_load_config = tk.Button(window, text="Load Configuration", command=load_config)
button_load_config.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create button to delete configuration
button_delete_config = tk.Button(window, text="Delete Configuration", command=delete_config)
button_delete_config.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Bind the Enter key to open the next window
window.bind("<Return>", next_window)

# Run the application
window.mainloop()

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=H['host'],
            user=H['user'],
            password=H['password'],
            database=H['database'],

        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def create_tables():
    connection = connect_to_db()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS StudentDetails (
                serial_no INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                registration_date VARCHAR(100) NOT NULL,
                registration_time VARCHAR(100) NOT NULL
    
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Attendance (
                Sl_No INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) NOT NULL, 
                name VARCHAR(100) NOT NULL,
                date VARCHAR(100) NOT NULL,
                time VARCHAR(100) NOT NULL,
                FOREIGN KEY (student_id) REFERENCES StudentDetails(student_id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        mess._show(title='Success', message='Tables created successfully!')
    except Error as e:
        mess._show(title='Error', message=str(e))
    finally:
        if connection:
            connection.close()


# Function to get total registrations from the database
def get_total_registrations():
    connection = connect_to_db()
    if connection is None:
        return 0  # Return 0 if the connection fails

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM StudentDetails")
        total_registrations = cursor.fetchone()[0]  # Get the count
    except Error as e:
        print(f"Error: {e}")
        return 0  # Return 0 in case of an error
    finally:
        if connection:
            connection.close()

    return total_registrations

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

##################################################################################

def tick():
    # Get the current time
    current_time = time.strftime('%I:%M:%S %p')
    
    # Update the clock label with the current time
    clock.config(text=current_time)
    
    # Schedule the next update after 1000 milliseconds (1 second)
    clock.after(1000, tick)

###################################################################################

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'aniket22602@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('comic', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('comic', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('comic', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('comic', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height = 1,width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################


import re
import datetime
import cv2
import mysql.connector
from mysql.connector import Error

# Function to capture and save images of students for training
def TakeImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImage/")  # Ensure the image folder path exists

    # Retrieve database credentials from the predefined dictionary H
    try:
        connection = mysql.connector.connect(
            host=H['host'],
            user=H['user'],
            password=H['password'],
            database=H['database']
        )
    except mysql.connector.Error as err:
        mess._show(title='Error', message=f"Database connection error: {err}")
        return

    # Retrieve the latest serial number
    serial = 0
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM StudentDetails")
        serial = cursor.fetchone()[0] + 1  # Increment serial for new student

    except Error as e:
        mess._show(title='Error', message=f"Error querying the database: {e}")
        return

    # Retrieve ID and name from GUI fields
    Id = txt.get()
    name = txt2.get()

    # Debugging: Print the captured name
    print(f"Captured Name: '{name}'")

    # Validate name to ensure it's non-empty and contains valid characters
    if name and re.match(r"^[A-Za-z\s'-]+$", name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y+h, x:x+w])
                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum > 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        try:
            # Insert new student record into the database
            now = datetime.datetime.now()
            formatted_date = now.strftime('%d-%m-%Y')
            formatted_time = now.strftime('%I:%M:%S %p')
            cursor.execute(
                "INSERT INTO StudentDetails (student_id, name, registration_date, registration_time) VALUES (%s, %s, %s, %s)",
                (Id, name, formatted_date, formatted_time)
            )
            connection.commit()

            res = f"Images Taken for ID : {Id}"
            total_registrations = get_total_registrations(H['host'], H['user'], H['password'], H['database'])
            message1.configure(text=res)
            message.configure(text=f'Total Registrations till now: {total_registrations}')

        except Error as e:
            mess._show(title='Error', message=f"Error inserting student data: {e}")
            return

    else:
        print("Validation failed for name input.")
        if not name:
            print("Error: Name is empty.")
        elif not re.match(r"^[A-Za-z\s'-]+$", name):
            print("Error: Name contains invalid characters.")
        message.configure(text="Enter a valid name")

    if connection:
        connection.close()



########################################################################################

def TrainImages():
    # Check if the Haarcascade file exists and create necessary folders
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")

    # Create a face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)

    # Get images and labels from the TrainingImage directory
    faces, IDs = getImagesAndLabels("TrainingImage")

    try:
        # Train the recognizer with the faces and their corresponding IDs
        recognizer.train(faces, np.array(IDs))
        
        # Save the trained model to a file
        recognizer.save("TrainingImageLabel/Trainner.yml")
        
        # Display success message and total registrations
        res = "Profile Saved Successfully"
        total_registrations = get_total_registrations()  # Get updated count from the database
        
        # Update the GUI to show the success message
        message1.configure(text=res)
        message.configure(text='Total Registrations till now: ' + str(total_registrations))  # Update GUI

    except Exception as e:
        # Handle any exceptions that occur during training or saving
        mess._show(title='Error', message=str(e))





############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

import cv2
import datetime
from mysql.connector import connect, Error  # Adjust based on your DB

def TrackImages():
    check_haarcascadefile()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    attendance = []
    recorded_students = set()  # Set to keep track of recorded student IDs

    # Clear previous attendance records from the Treeview at the start
    tv.delete(*tv.get_children())  

    try:
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 50:
                    connection = connect_to_db()
                    try:
                        cursor = connection.cursor()
                        cursor.execute("SELECT name FROM StudentDetails WHERE student_id = %s", (serial,))
                        result = cursor.fetchone()
                        if result:
                            name = result[0]
                            
                            # Check if the student ID is already recorded
                            if serial not in recorded_students:
                                recorded_students.add(serial)  # Add to the set to prevent duplicates
                                attendance.append((serial, name))
                                
                                # Log attendance in the database
                                now = datetime.datetime.now()
                                formatted_date = now.strftime('%d-%m-%Y')
                                
                                formatted_time = now.strftime('%I:%M:%S %p')  # 12-hour format with AM/PM


                                
                                cursor.execute("INSERT INTO Attendance (student_id, name, date, time) VALUES (%s, %s, %s, %s)",
                                               (serial, name, formatted_date, formatted_time))
                                connection.commit()
                                
                                # Update the Treeview with attendance details
                                tv.insert('', 'end', text=serial, values=(name, formatted_date, formatted_time))  # This adds the new record

                    except Error as e:
                        print(f"Database error: {e}")
                    finally:
                        if connection:
                            connection.close()
                else:
                    serial = 'Unknown'
                    name = 'Unknown'

                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, f'ID: {serial} NAME: {name}', (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Tracking', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        cam.release()
        cv2.destroyAllWindows()
        print("Attendance session ended.")
        print(attendance)  # Optionally print the attendance list

from tkinter import messagebox

# Function to truncate the attendance table
def delete_attendance():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host=H['host'],
            user=H['user'],
            password=H['password'],
            database=H['database']

        )
        cursor = db.cursor()

        # Truncate the attendance table
        cursor.execute("TRUNCATE TABLE Attendance")
        db.commit()

        # Display success message
        messagebox.showinfo("Success", "Attendance records deleted and reset!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        # Close the cursor and connection if they exist
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

# Function to truncate the StudentDetails table and delete images
def delete_registration():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host=H['host'],
            user=H['user'],
            password=H['password'],
            database=H['database']

        )
        cursor = db.cursor()

        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Truncate the StudentDetails table
        cursor.execute("TRUNCATE TABLE StudentDetails")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        db.commit()

        # Delete all files in the TrainingImage folder
        folder_path = "TrainingImage"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)  # Removes the folder and all its contents
            os.makedirs(folder_path)  # Recreate the folder after deleting

        # Display success message
        messagebox.showinfo("Success", "All registrations and images deleted successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        # Close the cursor and connection if they exist
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#2d420a')

frame1 = tk.Frame(window, bg="#c79cff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#c79cff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance Monitoring System by Aniket" ,fg="white",bg="#2d420a" ,width=55 ,height=1,font=('comic', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="#ff61e5",bg="#2d420a" ,width=55 ,height=1,font=('comic', 15, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="#ff61e5",bg="#2d420a" ,width=55 ,height=1,font=('comic', 15, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#00fcca" ,font=('comic', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#00fcca" ,font=('comic', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#c79cff" ,font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('comic', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#c79cff" ,fg="black"  ,width=39 ,height=1, activebackground = "#3ffc00" ,font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#c79cff" ,fg="black"  ,width=39,height=1, activebackground = "#3ffc00" ,font=('comic', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#c79cff"  ,height=1 ,font=('comic', 17, ' bold '))
lbl3.place(x=100, y=115)

    # Fetch and display total registrations
total_registrations = get_total_registrations()
message.configure(text=f'Total Registrations till now: {total_registrations}')

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('comic', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ff7221"  ,width=11 ,activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ff7221"  ,width=11 , activebackground = "white" ,font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=175) 
delete_button = tk.Button(window, text="Delete Attendance", command=delete_attendance)
delete_button.place(x=150,y=230)
delete_btn = tk.Button(frame2, text="Delete All Registrations", command=delete_registration, fg="white", bg="red", height=1, width=25, font=('comic', 12, ' bold ')) # Adding a button in the GUI for deleting registrations and images
delete_btn.place(x=80, y=500)  # Adjust the x, y coordinates as needed
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="#6d00fc"  ,width=34  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="#3ffc00"  ,width=35  ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#eb4600"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=30, y=450)
create_tables_button = tk.Button(window, text="Create Tables", command=create_tables) # Create a button to create tables
create_tables_button.place(x=500, y=230)


##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
