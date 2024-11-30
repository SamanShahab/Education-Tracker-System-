import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar
import time

# Tree Node Class for Data Structure
class TreeNode:
    def __init__(self, name, status=None):
        self.name = name
        self.status = status  # Status for Pass/Fail (None for current courses)
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_children(self):
        return self.children

# Sample student data as tree
students_data = {
    "student01": {
        "password": "pass123",
        "tree": None
    },
    "student02": {
        "password": "mypassword",
        "tree": None
    }
}

# Initialize Trees
def initialize_student_tree():
    # Student 01 Tree
    student01_root = TreeNode("Student 01")
    current_courses = TreeNode("Current Courses")
    current_courses.add_child(TreeNode("Math 101"))
    current_courses.add_child(TreeNode("Physics 101"))
    current_courses.add_child(TreeNode("Chemistry 101"))

    previous_courses = TreeNode("Previous Courses")
    previous_courses.add_child(TreeNode("English 101", status="Pass"))
    previous_courses.add_child(TreeNode("Biology 101", status="Fail"))

    student01_root.add_child(current_courses)
    student01_root.add_child(previous_courses)
    students_data["student01"]["tree"] = student01_root

    # Student 02 Tree
    student02_root = TreeNode("Student 02")
    current_courses = TreeNode("Current Courses")
    current_courses.add_child(TreeNode("Programming 101"))
    current_courses.add_child(TreeNode("Data Science 101"))

    previous_courses = TreeNode("Previous Courses")
    previous_courses.add_child(TreeNode("AI 101", status="Pass"))
    previous_courses.add_child(TreeNode("Math 101", status="Pass"))

    student02_root.add_child(current_courses)
    student02_root.add_child(previous_courses)
    students_data["student02"]["tree"] = student02_root


initialize_student_tree()

class EducationTrackerSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Education Tracker System")
        self.root.geometry("900x700")  # Default size
        self.root.resizable(True, True)  # Enable resizing in both directions (horizontal & vertical)

        # Variables for login
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.current_user = None

        # Add a nice theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # You can try other themes like 'alt', 'classic', 'vista', 'xpnative', etc.

        self.create_login_page()

    def create_login_page(self):
        self.clear_frame()

        # Login Page Header with better font and color
        tk.Label(self.root, text="Education Tracker System", font=("Arial", 26, "bold"), fg="#004B8D").pack(pady=30)

        # Login Frame
        login_frame = ttk.Frame(self.root, padding=20, relief="solid", borderwidth=2)
        login_frame.pack(pady=20)

        ttk.Label(login_frame, text="Student ID:", font=("Arial", 14)).grid(row=0, column=0, pady=10, padx=5)
        ttk.Entry(login_frame, textvariable=self.username_var, font=("Arial", 14), width=30).grid(row=0, column=1, pady=10)

        ttk.Label(login_frame, text="Password:", font=("Arial", 14)).grid(row=1, column=0, pady=10, padx=5)
        ttk.Entry(login_frame, textvariable=self.password_var, font=("Arial", 14), show="*", width=30).grid(row=1, column=1, pady=10)

        ttk.Button(login_frame, text="Login", command=self.authenticate_user, width=20, style="TButton").grid(row=2, column=0, columnspan=2, pady=20)

    def authenticate_user(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username in students_data and students_data[username]["password"] == password:
            self.current_user = username
            self.create_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Student ID or Password!")

    def create_dashboard(self):
        self.clear_frame()

        # Dashboard Header with better design
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 22, "bold"), fg="#006400").pack(pady=20)

        # Dashboard Buttons with style
        ttk.Button(self.root, text="View All Courses", command=self.view_all_courses, width=30, style="TButton").pack(pady=10, padx=20)
        ttk.Button(self.root, text="Manage Current Courses", command=lambda: self.manage_courses("Current Courses"), width=30, style="TButton").pack(pady=10, padx=20)
        ttk.Button(self.root, text="Manage Previous Courses", command=lambda: self.manage_courses("Previous Courses"), width=30, style="TButton").pack(pady=10, padx=20)
        ttk.Button(self.root, text="Logout", command=self.logout, width=30, style="TButton").pack(pady=10, padx=20)

        # Display Calendar and Time
        self.display_calendar_and_time()

    def display_calendar_and_time(self):
        # Display Calendar with modern look
        cal_frame = ttk.Frame(self.root)
        cal_frame.pack(pady=20)

        cal = Calendar(cal_frame, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
        cal.pack(padx=10, pady=10)

        # Display Current Date and Time with design
        time_frame = ttk.Frame(self.root)
        time_frame.pack(pady=10)

        self.time_label = tk.Label(time_frame, text="", font=("Arial", 14), fg="#003366")
        self.time_label.pack()

        # Update the current time every second
        self.update_time()

    def update_time(self):
        # Get the current time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update every second

    def view_all_courses(self):
        self.clear_frame()

        # View All Courses Header with modern style
        tk.Label(self.root, text="All Courses", font=("Arial", 18, "bold"), fg="#0056B3").pack(pady=20)

        tree = students_data[self.current_user]["tree"]

        # Frame for current courses
        current_frame = ttk.Frame(self.root, padding=20, relief="solid", borderwidth=2)
        current_frame.pack(fill="x", pady=5)
        current_toggle_button = ttk.Button(current_frame, text="v Current Courses", width=30,
                                           command=lambda: self.toggle_section(current_courses_content, current_toggle_button), style="TButton")
        current_toggle_button.pack(anchor="w", padx=10)
        current_courses_content = ttk.Frame(current_frame)
        self.display_specific_tree(tree, "Current Courses", current_courses_content)

        # Frame for previous courses
        previous_frame = ttk.Frame(self.root, padding=20, relief="solid", borderwidth=2)
        previous_frame.pack(fill="x", pady=5)
        previous_toggle_button = ttk.Button(previous_frame, text="v Previous Courses", width=30,
                                            command=lambda: self.toggle_section(previous_courses_content, previous_toggle_button), style="TButton")
        previous_toggle_button.pack(anchor="w", padx=10)
        previous_courses_content = ttk.Frame(previous_frame)
        self.display_specific_tree(tree, "Previous Courses", previous_courses_content)

        ttk.Button(self.root, text="Back to Dashboard", command=self.create_dashboard, width=20, style="TButton").pack(pady=20)

    def toggle_section(self, content_frame, toggle_button):
        if content_frame.winfo_ismapped():
            content_frame.pack_forget()
            toggle_button.config(text=toggle_button.cget("text").replace("v", "^"))
        else:
            content_frame.pack(fill="x", pady=5)
            toggle_button.config(text=toggle_button.cget("text").replace("^", "v"))

    def display_specific_tree(self, tree, category_name, content_frame):
        # Find the category node from the tree
        category_node = self.find_node(tree, category_name)
        if category_node:
            for course in category_node.get_children():
                course_text = course.name
                if course.status:
                    course_text += f" ({course.status})"
                ttk.Label(content_frame, text=course_text, font=("Arial", 14)).pack(anchor="w", padx=20)

    def manage_courses(self, category_name):
        self.clear_frame()

        # Manage Courses Header
        tk.Label(self.root, text=f"Manage {category_name}", font=("Arial", 22, "bold"), fg="#0056B3").pack(pady=20)

        tree = students_data[self.current_user]["tree"]
        category_node = self.find_node(tree, category_name)

        # Frame for managing courses
        courses_frame = ttk.Frame(self.root, padding=20, relief="solid", borderwidth=2)
        courses_frame.pack(fill="x", pady=5)

        # Add Course Label and Entry (Single Box)
        tk.Label(courses_frame, text=f"Add a new course to {category_name}:", font=("Arial", 14)).grid(row=0, column=0, padx=10)
        course_var = tk.StringVar()
        ttk.Entry(courses_frame, textvariable=course_var, font=("Arial", 14)).grid(row=0, column=1, pady=10)

        # Functions to handle adding and deleting courses
        def add_course():
            course_name = course_var.get()
            if course_name:
                category_node.add_child(TreeNode(course_name))
                messagebox.showinfo("Course Added", f"{course_name} has been added to {category_name}!")
                self.create_dashboard()
            else:
                messagebox.showwarning("Invalid Input", "Please enter a course name.")

        def delete_course():
            selected_index = courses_listbox.curselection()
            if selected_index:
                selected_course = category_node.get_children()[selected_index[0]]
                category_node.get_children().remove(selected_course)
                messagebox.showinfo("Course Deleted", f"{selected_course.name} has been deleted!")
                self.create_dashboard()
            else:
                messagebox.showwarning("No Course Selected", "Please select a course to delete.")

        # Listbox for courses (for deletion)
        courses_listbox = tk.Listbox(courses_frame, font=("Arial", 14), height=5)
        courses_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        for course in category_node.get_children():
            courses_listbox.insert(tk.END, course.name)

        # Add/Delete Course buttons
        ttk.Button(courses_frame, text="Add Course", command=add_course, width=20, style="TButton").grid(row=2, column=0, pady=10)
        ttk.Button(courses_frame, text="Delete Course", command=delete_course, width=20, style="TButton").grid(row=2, column=1, pady=10)

        # Assignment Submission Section
        tk.Label(courses_frame, text="Submit an Assignment for this Course:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=15)

        # Textbox for Assignment Subject
        tk.Label(courses_frame, text="Enter the Subject of the Assignment:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
        assignment_subject_var = tk.StringVar()
        ttk.Entry(courses_frame, textvariable=assignment_subject_var, font=("Arial", 14)).grid(row=4, column=1, pady=10)

        def submit_assignment():
            subject = assignment_subject_var.get()
            file_path = askopenfilename(title="Select Assignment File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            if file_path and subject:
                messagebox.showinfo("Assignment Submitted", f"Your assignment for {subject} has been submitted from {file_path}!")
            elif not subject:
                messagebox.showwarning("Invalid Input", "Please enter the subject of the assignment.")
            else:
                messagebox.showwarning("No File Selected", "Please select an assignment file to submit.")

        ttk.Button(courses_frame, text="Submit Assignment", command=submit_assignment, width=20, style="TButton").grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(self.root, text="Back to Dashboard", command=self.create_dashboard, width=20, style="TButton").pack(pady=20)

    def find_node(self, tree, category_name):
        if tree.name == category_name:
            return tree
        for child in tree.get_children():
            found = self.find_node(child, category_name)
            if found:
                return found
        return None

    def logout(self):
        self.current_user = None
        self.create_login_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Running the Application
root = tk.Tk()
app = EducationTrackerSystem(root)
root.mainloop()
