############################################# MODERN GUI MODULE ################################################
import tkinter as tk
from tkinter import ttk, messagebox as mess
import tkinter.simpledialog as tsd
from datetime import datetime
import os
import csv
import pandas as pd
from core_logic import AttendanceSystem

class ModernAttendanceGUI:
    def __init__(self):
        try:
            self.attendance_system = AttendanceSystem()
            self.setup_main_window()
            self.setup_styles()
            self.create_widgets()
            self.load_initial_data()
        except Exception as e:
            print(f"Error initializing GUI: {e}")
            # Show error message and exit gracefully
            import tkinter.messagebox as mess
            mess.showerror("Initialization Error", f"Failed to initialize the application:\n{e}\n\nPlease check your OpenCV installation.")
            return
        
    def setup_main_window(self):
        """Setup the main application window"""
        self.root = tk.Tk()
        self.root.title("Face Recognition-based Attendance System")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to 90% of screen size for better full-screen experience
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)
        self.root.configure(bg='#F8F9FA')
        
        # Center the window
        self.root.update_idletasks()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(1200, 800)
        
    def setup_styles(self):
        """Setup modern color scheme and styles"""
        self.COLORS = {
            'primary': '#2C3E50',      # Dark blue-gray
            'secondary': '#3498DB',    # Blue
            'accent': '#E74C3C',       # Red
            'success': '#27AE60',      # Green
            'warning': '#F39C12',      # Orange
            'info': '#17A2B8',         # Cyan
            'light': '#ECF0F1',        # Light gray
            'dark': '#34495E',         # Dark gray
            'white': '#FFFFFF',
            'background': '#F8F9FA'    # Very light gray
        }
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Notebook (tab) style
        self.style.configure('TNotebook', background=self.COLORS['white'], borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                           background=self.COLORS['light'],
                           foreground=self.COLORS['dark'],
                           padding=[25, 12],
                           font=('Segoe UI', 12, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.COLORS['secondary']),
                                ('active', self.COLORS['info'])],
                      foreground=[('selected', self.COLORS['white']),
                                ('active', self.COLORS['white'])])
        
        # Configure Treeview style
        self.style.configure("Treeview",
                            background=self.COLORS['light'],
                            foreground=self.COLORS['dark'],
                            rowheight=35,
                            fieldbackground=self.COLORS['light'],
                            font=('Segoe UI', 10))
        self.style.configure("Treeview.Heading",
                            background=self.COLORS['secondary'],
                            foreground=self.COLORS['white'],
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        self.create_header()
        self.create_tabs()
        self.create_footer()
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg=self.COLORS['primary'], height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Main header content
        header_content = tk.Frame(header_frame, bg=self.COLORS['primary'])
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Title
        title_label = tk.Label(header_content, 
                              text="Face Recognition-based Attendance System", 
                              fg=self.COLORS['white'], 
                              bg=self.COLORS['primary'], 
                              font=('Segoe UI', 24, 'bold'))
        title_label.pack(pady=(10, 5))
        
        # Date and time
        datetime_frame = tk.Frame(header_content, bg=self.COLORS['primary'])
        datetime_frame.pack(pady=(0, 10))
        
        self.date_label = tk.Label(datetime_frame, 
                                  text=f"📅 {datetime.now().strftime('%B %d, %Y')}", 
                                  fg=self.COLORS['light'], 
                                  bg=self.COLORS['primary'], 
                                  font=('Segoe UI', 12, 'bold'))
        self.date_label.pack(side='left', padx=(0, 30))
        
        self.time_label = tk.Label(datetime_frame, 
                                  text=f"🕐 {datetime.now().strftime('%H:%M:%S')}", 
                                  fg=self.COLORS['light'], 
                                  bg=self.COLORS['primary'], 
                                  font=('Segoe UI', 12, 'bold'))
        self.time_label.pack(side='left')
        
        # Update time every second
        self.update_time()
        
    def create_tabs(self):
        """Create the main tabbed interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_registration_tab()
        self.create_attendance_tab()
        self.create_view_attendance_tab()
        self.create_analytics_tab()
        
    def create_dashboard_tab(self):
        """Create the dashboard/overview tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Dashboard content
        dashboard_container = tk.Frame(dashboard_frame, bg=self.COLORS['background'])
        dashboard_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.Frame(dashboard_container, bg=self.COLORS['white'], relief='flat', bd=1)
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        welcome_label = tk.Label(welcome_frame, 
                                text="👋 Welcome to Face Recognition-based Attendance System", 
                                fg=self.COLORS['primary'], 
                                bg=self.COLORS['white'], 
                                font=('Segoe UI', 18, 'bold'),
                                pady=20)
        welcome_label.pack()
        
        # Quick stats
        stats_frame = tk.Frame(dashboard_container, bg=self.COLORS['background'])
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Stats cards
        self.create_stat_card(stats_frame, "👥 Total Students", "0", self.COLORS['secondary'], 0, 0)
        self.create_stat_card(stats_frame, "📚 Total Subjects", "0", self.COLORS['success'], 0, 1)
        self.create_stat_card(stats_frame, "📅 Today's Attendance", "0", self.COLORS['warning'], 0, 2)
        self.create_stat_card(stats_frame, "✅ Attendance Rate", "0%", self.COLORS['info'], 0, 3)
        
        # Quick actions
        actions_frame = tk.Frame(dashboard_container, bg=self.COLORS['white'], relief='flat', bd=1)
        actions_frame.pack(fill='x', pady=(0, 20))
        
        actions_label = tk.Label(actions_frame, 
                                text="🚀 Quick Actions", 
                                fg=self.COLORS['dark'], 
                                bg=self.COLORS['white'], 
                                font=('Segoe UI', 14, 'bold'))
        actions_label.pack(pady=(20, 10))
        
        # Quick action buttons
        quick_actions = tk.Frame(actions_frame, bg=self.COLORS['white'])
        quick_actions.pack(pady=(0, 20))
        
        self.create_quick_button(quick_actions, "📸 Take Attendance", 
                                lambda: self.notebook.select(2), self.COLORS['warning'], 0, 0)
        self.create_quick_button(quick_actions, "👤 Register Student", 
                                lambda: self.notebook.select(1), self.COLORS['success'], 0, 1)
        self.create_quick_button(quick_actions, "📊 View Reports", 
                                lambda: self.notebook.select(3), self.COLORS['info'], 0, 2)
        self.create_quick_button(quick_actions, "⚙️ Settings", 
                                self.show_settings, self.COLORS['accent'], 0, 3)
        
    def create_registration_tab(self):
        """Create the student registration tab"""
        reg_frame = ttk.Frame(self.notebook)
        self.notebook.add(reg_frame, text="👤 Student Registration")
        
        # Main container with scrollable content
        main_container = tk.Frame(reg_frame, bg=self.COLORS['background'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create a canvas and scrollbar for scrollable content
        canvas = tk.Canvas(main_container, bg=self.COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form header
        form_header = tk.Frame(scrollable_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        form_header.pack(fill='x', pady=(0, 20), padx=20)
        
        header_label = tk.Label(form_header, 
                               text="📝 Student Registration Form", 
                               fg=self.COLORS['primary'], 
                               bg=self.COLORS['white'], 
                               font=('Segoe UI', 20, 'bold'))
        header_label.pack(pady=25)
        
        # Form content
        form_content = tk.Frame(scrollable_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        form_content.pack(fill='x', padx=20, pady=(0, 20))
        
        # Create form fields
        self.create_registration_form(form_content)
        
    def create_attendance_tab(self):
        """Create the take attendance tab"""
        att_frame = ttk.Frame(self.notebook)
        self.notebook.add(att_frame, text="📸 Take Attendance")
        
        # Attendance container
        att_container = tk.Frame(att_frame, bg=self.COLORS['background'])
        att_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Attendance header
        att_header = tk.Frame(att_container, bg=self.COLORS['white'], relief='flat', bd=1)
        att_header.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(att_header, 
                               text="📸 Take Attendance", 
                               fg=self.COLORS['primary'], 
                               bg=self.COLORS['white'], 
                               font=('Segoe UI', 18, 'bold'))
        header_label.pack(pady=20)
        
        # Attendance form
        att_form = tk.Frame(att_container, bg=self.COLORS['white'], relief='flat', bd=1)
        att_form.pack(fill='both', expand=True)
        
        # Create attendance form
        self.create_attendance_form(att_form)
        
    def create_view_attendance_tab(self):
        """Create the view attendance tab"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="📊 View Attendance")
        
        # View container
        view_container = tk.Frame(view_frame, bg=self.COLORS['background'])
        view_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # View header
        view_header = tk.Frame(view_container, bg=self.COLORS['white'], relief='flat', bd=1)
        view_header.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(view_header, 
                               text="📊 Attendance Records", 
                               fg=self.COLORS['primary'], 
                               bg=self.COLORS['white'], 
                               font=('Segoe UI', 18, 'bold'))
        header_label.pack(pady=20)
        
        # Filters and search
        filter_frame = tk.Frame(view_container, bg=self.COLORS['white'], relief='flat', bd=1)
        filter_frame.pack(fill='x', pady=(0, 20))
        
        self.create_attendance_filters(filter_frame)
        
        # Attendance table
        table_frame = tk.Frame(view_container, bg=self.COLORS['white'], relief='flat', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        self.create_attendance_table(table_frame)
        
    def create_analytics_tab(self):
        """Create the analytics tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📈 Analytics")
        
        # Analytics container
        analytics_container = tk.Frame(analytics_frame, bg=self.COLORS['background'])
        analytics_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Analytics header
        analytics_header = tk.Frame(analytics_container, bg=self.COLORS['white'], relief='flat', bd=1)
        analytics_header.pack(fill='x', pady=(0, 20))
        
        header_label = tk.Label(analytics_header, 
                               text="📈 Attendance Analytics", 
                               fg=self.COLORS['primary'], 
                               bg=self.COLORS['white'], 
                               font=('Segoe UI', 18, 'bold'))
        header_label.pack(pady=20)
        
        # Placeholder for analytics content
        placeholder = tk.Label(analytics_container, 
                              text="📊 Analytics and Reports will be displayed here", 
                              fg=self.COLORS['dark'], 
                              bg=self.COLORS['background'], 
                              font=('Segoe UI', 14))
        placeholder.pack(expand=True)
        
    def create_footer(self):
        """Create the footer section"""
        footer_frame = tk.Frame(self.root, bg=self.COLORS['primary'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(footer_frame, 
                               text="© 2024 Face Recognition-based Attendance System", 
                               fg=self.COLORS['light'], 
                               bg=self.COLORS['primary'], 
                               font=('Segoe UI', 9))
        footer_label.pack(pady=10)
        
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='flat', bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        title_label = tk.Label(card, text=title, fg=self.COLORS['white'], 
                              bg=color, font=('Segoe UI', 10))
        title_label.pack(pady=(15, 5))
        
        value_label = tk.Label(card, text=value, fg=self.COLORS['white'], 
                              bg=color, font=('Segoe UI', 20, 'bold'))
        value_label.pack(pady=(0, 15))
        
        # Store reference for updates
        clean_title = title.replace(" ", "_").replace("'", "").lower()
        attr_name = f'stat_{clean_title}'
        setattr(self, attr_name, value_label)
        
    def create_quick_button(self, parent, text, command, color, row, col):
        """Create a quick action button"""
        btn = tk.Button(parent, text=text, command=command, 
                       fg=self.COLORS['white'], bg=color,
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat', bd=0, padx=20, pady=15,
                       cursor='hand2')
        btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
    def create_registration_form(self, parent):
        """Create the student registration form with modern layout"""
        # Main form container
        form_container = tk.Frame(parent, bg=self.COLORS['white'])
        form_container.pack(fill='x', padx=30, pady=30)
        
        # Create two-column layout
        main_content = tk.Frame(form_container, bg=self.COLORS['white'])
        main_content.pack(fill='x', pady=(0, 30))
        
        # Left Column - Personal Information
        left_column = tk.Frame(main_content, bg=self.COLORS['white'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Personal Information Section
        personal_section = tk.LabelFrame(left_column, 
                                       text="👤 Personal Information", 
                                       fg=self.COLORS['primary'], 
                                       bg=self.COLORS['white'],
                                       font=('Segoe UI', 16, 'bold'),
                                       relief='solid', bd=2,
                                       padx=20, pady=20)
        personal_section.pack(fill='x', pady=(0, 20))
        
        # Personal fields with better spacing (reduced to 6 fields for symmetry)
        fields_personal = [
            ("🆔 Student PRN *", "prn_entry"),
            ("👤 First Name *", "first_name_entry"),
            ("👤 Last Name *", "last_name_entry"),
            ("⚥ Gender *", "gender_combo"),
            ("📅 Date of Birth *", "dob_entry"),
            ("🎫 Roll Number *", "roll_number_entry")
        ]
        
        for i, (label_text, field_name) in enumerate(fields_personal):
            # Label
            label = tk.Label(personal_section, text=label_text, 
                           fg=self.COLORS['dark'], bg=self.COLORS['white'],
                           font=('Segoe UI', 12, 'bold'))
            label.pack(anchor='w', pady=(15 if i > 0 else 0, 8))
            
            # Field
            if field_name == "gender_combo":
                self.gender_var = tk.StringVar(value="Male")
                field = ttk.Combobox(personal_section, textvariable=self.gender_var,
                                   values=["Male", "Female", "Other"],
                                   font=('Segoe UI', 12), state="readonly")
                setattr(self, field_name.replace("_combo", "_var"), self.gender_var)
            else:
                field = tk.Entry(personal_section, font=('Segoe UI', 12), 
                               relief='solid', bd=1, highlightthickness=1)
                setattr(self, field_name, field)
            
            field.pack(fill='x', pady=(0, 10))
            
            # Special formatting for DOB
            if field_name == "dob_entry":
                dob_hint = tk.Label(personal_section, text="(DD/MM/YYYY)", 
                                  fg=self.COLORS['dark'], bg=self.COLORS['white'],
                                  font=('Segoe UI', 9, 'italic'))
                dob_hint.pack(anchor='w', pady=(0, 5))
        
        # Right Column - Academic Information
        right_column = tk.Frame(main_content, bg=self.COLORS['white'])
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Academic Information Section
        academic_section = tk.LabelFrame(right_column,
                                       text="🎓 Academic Information",
                                       fg=self.COLORS['primary'],
                                       bg=self.COLORS['white'],
                                       font=('Segoe UI', 16, 'bold'),
                                       relief='solid', bd=2,
                                       padx=20, pady=20)
        academic_section.pack(fill='x', pady=(0, 20))
        
        # Academic fields (expanded to 6 fields for symmetry)
        academic_fields = [
            ("🏛️ Department *", "dept_var", ["Computer Engineering", "Information Technology", 
                                            "Electronics & Communication", "Mechanical Engineering",
                                            "Civil Engineering", "Electrical Engineering"]),
            ("📖 Course *", "course_var", ["B.Tech", "B.E.", "M.Tech", "M.E.", "B.Sc", "M.Sc", "BBA", "MBA"]),
            ("📚 Academic Year *", "year_var", ["First Year", "Second Year", "Third Year", "Fourth Year"]),
            ("📅 Semester *", "semester_var", ["Semester 1", "Semester 2", "Semester 3", "Semester 4",
                                              "Semester 5", "Semester 6", "Semester 7", "Semester 8"]),
            ("📧 Email Address *", "email_entry", None),
            ("📱 Phone Number *", "phone_entry", None)
        ]
        
        for i, (label_text, var_name, values) in enumerate(academic_fields):
            # Label
            label = tk.Label(academic_section, text=label_text,
                           fg=self.COLORS['dark'], bg=self.COLORS['white'],
                           font=('Segoe UI', 12, 'bold'))
            label.pack(anchor='w', pady=(15 if i > 0 else 0, 8))
            
            # Field (ComboBox or Entry)
            if values is not None:  # ComboBox
                var = tk.StringVar(value=values[0])
                field = ttk.Combobox(academic_section, textvariable=var,
                                   values=values, font=('Segoe UI', 12), state="readonly")
                setattr(self, var_name, var)
            else:  # Entry field
                field = tk.Entry(academic_section, font=('Segoe UI', 12), 
                               relief='solid', bd=1, highlightthickness=1)
                setattr(self, var_name, field)
            
            field.pack(fill='x', pady=(0, 10))
        
        # Action Buttons Section - Full Width
        action_section = tk.LabelFrame(form_container,
                                     text="⚡ Action Buttons",
                                     fg=self.COLORS['primary'],
                                     bg=self.COLORS['white'],
                                     font=('Segoe UI', 16, 'bold'),
                                     relief='solid', bd=2,
                                     padx=20, pady=20)
        action_section.pack(fill='x', pady=(20, 0))
        
        # Button container
        button_container = tk.Frame(action_section, bg=self.COLORS['white'])
        button_container.pack(fill='x', pady=10)
        
        # Create buttons with better styling
        buttons = [
            ("📸 Take Face Images", self.take_student_images, self.COLORS['secondary']),
            ("💾 Save Student Profile", self.save_student_profile, self.COLORS['success']),
            ("🗑️ Clear Form", self.clear_registration_form, self.COLORS['warning'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_container, text=text, command=command,
                          fg=self.COLORS['white'], bg=color,
                          font=('Segoe UI', 13, 'bold'),
                          relief='flat', bd=0,
                          padx=30, pady=15,
                          cursor='hand2',
                          activebackground=color,
                          activeforeground=self.COLORS['white'])
            btn.pack(side='left', padx=(0, 20) if i < len(buttons) - 1 else 0)
        
        # Status message
        self.reg_status_label = tk.Label(form_container,
                                       text="✅ Ready to register new student",
                                       fg=self.COLORS['success'],
                                       bg=self.COLORS['white'],
                                       font=('Segoe UI', 12, 'bold'))
        self.reg_status_label.pack(pady=(20, 0))
        
    def create_attendance_form(self, parent):
        """Create the attendance form"""
        form_frame = tk.Frame(parent, bg=self.COLORS['white'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Session Information Section
        session_frame = tk.LabelFrame(form_frame, text="📚 Session Information", 
                                     fg=self.COLORS['primary'], bg=self.COLORS['white'],
                                     font=('Segoe UI', 12, 'bold'), pady=10)
        session_frame.pack(fill='x', pady=(0, 20))
        
        # Row 1: Subject and Faculty
        row1 = tk.Frame(session_frame, bg=self.COLORS['white'])
        row1.pack(fill='x', pady=10)
        
        tk.Label(row1, text="📖 Subject *", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 20))
        self.subject_var = tk.StringVar()
        subject_combo = ttk.Combobox(row1, textvariable=self.subject_var, 
                                    values=["Data Structures", "Database Management", "Computer Networks",
                                           "Software Engineering", "Machine Learning", "Web Development"], 
                                    font=('Segoe UI', 11), width=25, state="readonly")
        subject_combo.grid(row=0, column=1, padx=(0, 40))
        
        tk.Label(row1, text="👨‍🏫 Faculty Name *", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=2, sticky='w', padx=(0, 20))
        self.faculty_entry = tk.Entry(row1, font=('Segoe UI', 11), width=25)
        self.faculty_entry.grid(row=0, column=3)
        
        # Row 2: Date and Time
        row2 = tk.Frame(session_frame, bg=self.COLORS['white'])
        row2.pack(fill='x', pady=10)
        
        tk.Label(row2, text="📅 Date *", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 20))
        self.attendance_date = tk.StringVar(value=datetime.now().strftime('%d/%m/%Y'))
        date_entry = tk.Entry(row2, textvariable=self.attendance_date, 
                             font=('Segoe UI', 11), width=25)
        date_entry.grid(row=0, column=1, padx=(0, 40))
        
        tk.Label(row2, text="🕐 Time *", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=2, sticky='w', padx=(0, 20))
        self.attendance_time = tk.StringVar(value=datetime.now().strftime('%H:%M'))
        time_entry = tk.Entry(row2, textvariable=self.attendance_time, 
                             font=('Segoe UI', 11), width=25)
        time_entry.grid(row=0, column=3)
        
        # Action Buttons
        button_frame = tk.Frame(form_frame, bg=self.COLORS['white'])
        button_frame.pack(fill='x', pady=20)
        
        # Start Attendance button
        start_btn = tk.Button(button_frame, text="🎯 Start Face Recognition", 
                             command=self.start_attendance,
                             fg=self.COLORS['white'], bg=self.COLORS['warning'],
                             font=('Segoe UI', 14, 'bold'), relief='flat', 
                             padx=30, pady=15, cursor='hand2')
        start_btn.pack(side='left', padx=(0, 20))
        
        # Stop Attendance button
        stop_btn = tk.Button(button_frame, text="⏹️ Stop Attendance", 
                            command=self.stop_attendance,
                            fg=self.COLORS['white'], bg=self.COLORS['accent'],
                            font=('Segoe UI', 14, 'bold'), relief='flat', 
                            padx=30, pady=15, cursor='hand2')
        stop_btn.pack(side='left')
        
        # Status message
        self.att_status_label = tk.Label(form_frame, text="Ready to take attendance", 
                                        fg=self.COLORS['success'], bg=self.COLORS['white'],
                                        font=('Segoe UI', 10, 'bold'))
        self.att_status_label.pack(pady=(10, 0))
        
    def create_attendance_filters(self, parent):
        """Create attendance filters"""
        filter_frame = tk.Frame(parent, bg=self.COLORS['white'])
        filter_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(filter_frame, text="🔍 Filters:", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 11, 'bold')).pack(side='left', padx=(0, 20))
        
        tk.Label(filter_frame, text="📅 Date:", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 10)).pack(side='left', padx=(0, 10))
        self.filter_date = tk.StringVar(value=datetime.now().strftime('%d/%m/%Y'))
        date_filter = tk.Entry(filter_frame, textvariable=self.filter_date, 
                              font=('Segoe UI', 10), width=12)
        date_filter.pack(side='left', padx=(0, 20))
        
        tk.Label(filter_frame, text="📖 Subject:", fg=self.COLORS['dark'], 
                bg=self.COLORS['white'], font=('Segoe UI', 10)).pack(side='left', padx=(0, 10))
        self.filter_subject = tk.StringVar()
        subject_filter = ttk.Combobox(filter_frame, textvariable=self.filter_subject, 
                                     values=["All", "Data Structures", "Database Management", "Computer Networks"],
                                     font=('Segoe UI', 10), width=15, state="readonly")
        subject_filter.pack(side='left', padx=(0, 20))
        subject_filter.set("All")
        
        # Filter button
        filter_btn = tk.Button(filter_frame, text="🔍 Apply Filters", 
                              command=self.apply_filters,
                              fg=self.COLORS['white'], bg=self.COLORS['secondary'],
                              font=('Segoe UI', 10, 'bold'), relief='flat', 
                              padx=15, pady=5, cursor='hand2')
        filter_btn.pack(side='left', padx=(20, 0))
        
    def create_attendance_table(self, parent):
        """Create the attendance table"""
        table_frame = tk.Frame(parent, bg=self.COLORS['white'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview
        columns = ('student_id', 'name', 'subject', 'faculty', 'date', 'time', 'status')
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.attendance_tree.heading('student_id', text='🆔 Student ID')
        self.attendance_tree.heading('name', text='👤 Name')
        self.attendance_tree.heading('subject', text='📖 Subject')
        self.attendance_tree.heading('faculty', text='👨‍🏫 Faculty')
        self.attendance_tree.heading('date', text='📅 Date')
        self.attendance_tree.heading('time', text='🕐 Time')
        self.attendance_tree.heading('status', text='✅ Status')
        
        # Configure column widths
        self.attendance_tree.column('student_id', width=100)
        self.attendance_tree.column('name', width=150)
        self.attendance_tree.column('subject', width=150)
        self.attendance_tree.column('faculty', width=150)
        self.attendance_tree.column('date', width=100)
        self.attendance_tree.column('time', width=100)
        self.attendance_tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.attendance_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
        
    def load_initial_data(self):
        """Load initial data and update statistics"""
        # This will be implemented to load data from the core logic
        pass
        
    def clear_registration_form(self):
        """Clear the registration form"""
        # Clear entry fields
        self.prn_entry.delete(0, 'end')
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')
        self.roll_number_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        
        # Reset combo boxes to default values
        self.gender_var.set("Male")
        self.dept_var.set("Computer Engineering")
        self.course_var.set("B.Tech")
        self.year_var.set("First Year")
        self.semester_var.set("Semester 1")
        
        self.reg_status_label.config(text="✅ Form cleared successfully", fg=self.COLORS['warning'])
        
    def take_student_images(self):
        """Take face images for student registration"""
        # Validate form first
        if not self.validate_registration_form():
            return
            
        # Call core logic to take images
        try:
            result = self.attendance_system.take_student_images(
                prn=self.prn_entry.get(),
                first_name=self.first_name_entry.get(),
                last_name=self.last_name_entry.get(),
                gender=self.gender_var.get(),
                dob=self.dob_entry.get(),
                roll_number=self.roll_number_entry.get(),
                email=self.email_entry.get(),
                phone=self.phone_entry.get(),
                department=self.dept_var.get(),
                course=self.course_var.get(),
                year=self.year_var.get(),
                semester=self.semester_var.get()
            )
            self.reg_status_label.config(text=result, fg=self.COLORS['success'])
            
            # Show success message
            mess.showinfo("Images Captured", f"📸 {result}\n\nNow click 'Save Profile' to train the face recognition model.")
            
        except Exception as e:
            error_msg = f"❌ Error taking images: {str(e)}"
            self.reg_status_label.config(text=error_msg, fg=self.COLORS['accent'])
            mess.showerror("Error", error_msg)
            
    def save_student_profile(self):
        """Save student profile"""
        try:
            result = self.attendance_system.save_student_profile()
            self.reg_status_label.config(text=result, fg=self.COLORS['success'])
            
            # Show success message box
            mess.showinfo("Success", "✅ Profile Saved Successfully!\n\nThe student's face recognition model has been trained and saved. The student can now be recognized for attendance.")
            
            # Clear the form after successful save
            self.clear_registration_form()
            self.reg_status_label.config(text="Ready to register new student", fg=self.COLORS['success'])
            
            self.update_statistics()
        except Exception as e:
            error_msg = f"❌ Error saving profile: {str(e)}"
            self.reg_status_label.config(text=error_msg, fg=self.COLORS['accent'])
            mess.showerror("Error", error_msg)
            
    def start_attendance(self):
        """Start taking attendance"""
        # Validate attendance form
        if not self.validate_attendance_form():
            return
            
        try:
            result = self.attendance_system.start_attendance(
                subject=self.subject_var.get(),
                faculty=self.faculty_entry.get(),
                date=self.attendance_date.get(),
                time=self.attendance_time.get()
            )
            self.att_status_label.config(text=result, fg=self.COLORS['success'])
        except Exception as e:
            self.att_status_label.config(text=f"Error: {str(e)}", fg=self.COLORS['accent'])
            
    def stop_attendance(self):
        """Stop taking attendance"""
        try:
            result = self.attendance_system.stop_attendance()
            self.att_status_label.config(text=result, fg=self.COLORS['success'])
            self.update_statistics()
            self.refresh_attendance_table()
        except Exception as e:
            self.att_status_label.config(text=f"Error: {str(e)}", fg=self.COLORS['accent'])
            
    def apply_filters(self):
        """Apply filters to attendance table"""
        self.refresh_attendance_table()
        
    def refresh_attendance_table(self):
        """Refresh the attendance table with current data"""
        # Clear existing items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
            
        # Load attendance data from core logic
        try:
            attendance_data = self.attendance_system.get_attendance_records(
                date=self.filter_date.get(),
                subject=self.filter_subject.get()
            )
            
            for record in attendance_data:
                self.attendance_tree.insert('', 'end', values=record)
        except Exception as e:
            mess.showerror("Error", f"Failed to load attendance data: {str(e)}")
            
    def validate_registration_form(self):
        """Validate the registration form"""
        # Check required fields
        required_fields = [
            (self.prn_entry.get().strip(), "Student PRN"),
            (self.first_name_entry.get().strip(), "First name"),
            (self.last_name_entry.get().strip(), "Last name"),
            (self.dob_entry.get().strip(), "Date of birth"),
            (self.roll_number_entry.get().strip(), "Roll number"),
            (self.email_entry.get().strip(), "Email address"),
            (self.phone_entry.get().strip(), "Phone number")
        ]
        
        for value, field_name in required_fields:
            if not value:
                mess.showerror("Validation Error", f"{field_name} is required!")
                return False
        
        # Basic email validation
        email = self.email_entry.get().strip()
        if '@' not in email or '.' not in email:
            mess.showerror("Validation Error", "Please enter a valid email address!")
            return False
            
        return True
        
    def validate_attendance_form(self):
        """Validate the attendance form"""
        if not self.subject_var.get():
            mess.showerror("Validation Error", "Please select a subject!")
            return False
        if not self.faculty_entry.get().strip():
            mess.showerror("Validation Error", "Faculty name is required!")
            return False
        return True
        
    def update_statistics(self):
        """Update the statistics on dashboard"""
        try:
            stats = self.attendance_system.get_statistics()
            # Update statistics labels if they exist
            if hasattr(self, 'stat_total_students'):
                self.stat_total_students.config(text=str(stats['total_students']))
            if hasattr(self, 'stat_total_subjects'):
                self.stat_total_subjects.config(text=str(stats['total_subjects']))
            if hasattr(self, 'stat_todays_attendance'):
                self.stat_todays_attendance.config(text=str(stats['todays_attendance']))
            if hasattr(self, 'stat_attendance_rate'):
                self.stat_attendance_rate.config(text=f"{stats['attendance_rate']}%")
        except Exception as e:
            print(f"Error updating statistics: {e}")
            
    def show_settings(self):
        """Show settings dialog"""
        mess.showinfo("Settings", "Settings dialog will be implemented here")
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernAttendanceGUI()
    app.run()
