from flask import Flask, render_template, request, redirect, url_for, session
from db_handler import DBHandler  # Import the DBHandler class
from mongodb import mongo_insert, patients_collection  # Import MongoDB functions and collection

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize the DBHandler
db_handler = DBHandler()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Register the user using DBHandler
        success = db_handler.add_user(first_name, last_name, username, email, password)
        if success:
            return redirect(url_for('home'))  # Registration successful
        else:
            return "Username or email already exists. Please choose a different one."

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for users."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify the user using DBHandler
        success = db_handler.verify_user(username, password)
        if success:
            # Set session with user details
            session['username'] = username
            session['role'] = db_handler.get_user_role(username)  # Fetch role from the database
            return redirect(url_for('home'))  # Login successful
        else:
            return "Invalid username or password."  # Login failed

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    return redirect(url_for('home'))

@app.route('/users', methods=['GET'])
def users():
    if 'username' not in session or session.get('role') != 'admin':
        return "Access Denied", 403

    all_users = db_handler.get_all_users()  # Fetch all users
    return render_template('users.html', users=all_users)


@app.route('/admin/patients', methods=['GET', 'POST'])
def admin_patients():
    """Display, add, edit, and delete patients for admins."""
    if 'username' not in session or session.get('role') != 'admin':
        return "Access denied. Admins only.", 403

    # Fetch all patients to display
    patients = list(patients_collection.find({}, {"_id": 0}))
    return render_template('admin_patients.html', patients=patients)



@app.route('/admin/patients/add', methods=['POST'])
def admin_add_patient():
    """Allow admins to add new patient records."""
    if session.get('role') != 'admin':
        return "Access denied. Admins only.", 403

    patient_data = {
        "id": request.form['id'],
        "gender": request.form['gender'],
        "age": request.form['age'],
        "hypertension": request.form['hypertension'],
        "heart_disease": request.form['heart_disease'],
        "ever_married": request.form['ever_married'],
        "work_type": request.form['work_type'],
        "Residence_type": request.form['Residence_type'],
        "avg_glucose_level": request.form['avg_glucose_level'],
        "bmi": request.form['bmi'],
        "smoking_status": request.form['smoking_status'],
        "owner": "admin"  # Explicitly mark records added by admin
    }

    patients_collection.insert_one(patient_data)
    return redirect(url_for('admin_patients'))


@app.route('/admin/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    """Allow admins to delete a patient record."""
    if session.get('role') != 'admin':
        return "Access denied. Admins only.", 403

    result = patients_collection.delete_one({"id": patient_id})
    if result.deleted_count > 0:
        return redirect(url_for('admin_patients'))
    else:
        return "Failed to delete patient. Record not found."


@app.route('/patients', methods=['GET', 'POST'])
def patients():
    """ Route to view and search patient records stored in MongoDB."""
    search_query = ""
    patients_list = []  # Default to an empty list

    if request.method == 'POST':
        # Handle search query
        search_query = request.form.get('search', '').strip()

        if search_query:
            try:
                if search_query.isdigit():  # If the query is numeric, search the `id` field
                    search_query = int(search_query)
                    patients = patients_collection.find({"id": search_query}, {"_id": 0})  # Exact match on `id`
                else:
                    # Perform case-insensitive regex search on other fields
                    patients = patients_collection.find(
                        {
                            "$or": [
                                {"gender": {"$regex": search_query, "$options": "i"}},
                                {"age": {"$regex": search_query, "$options": "i"}},
                                {"hypertension": {"$regex": search_query, "$options": "i"}},
                                {"ever_married": {"$regex": search_query, "$options": "i"}},
                                {"work_type": {"$regex": search_query, "$options": "i"}},
                                {"Residence_type": {"$regex": search_query, "$options": "i"}},
                                {"avg_glucose_level": {"$regex": search_query, "$options": "i"}},
                                {"bmi": {"$regex": search_query, "$options": "i"}},
                                {"smoking_status": {"$regex": search_query, "$options": "i"}}
                            ]
                        },
                        {"_id": 0}  # Exclude MongoDB `_id` field
                    )
            except ValueError:
                # Handle potential conversion errors
                patients = []
        else:
            # If no search query, fetch all records
            patients = patients_collection.find({}, {"_id": 0})
    else:
        # On GET, retrieve all records
        patients = patients_collection.find({}, {"_id": 0})

    # Convert MongoDB cursor to list of dictionaries
    patients_list = list(patients)

    # Render the template with the patient data
    return render_template('patients.html', data=patients_list, search_query=search_query)

# Editing a User
@app.route('/edit_user', methods=['POST', 'GET'])
def edit_user():
    if 'username' not in session or session.get('role') != 'admin':
        return "Access Denied", 403

    if request.method == 'POST':
        username = request.form['username']
        user = db_handler.get_user(username)
        if user:
            return render_template('edit_user.html', user=user)
    
    # For handling updates
    if request.method == 'GET':
        username = request.args.get('username')
        updated_data = {
            "first_name": request.args.get('first_name'),
            "last_name": request.args.get('last_name'),
            "role": request.args.get('role'),
        }
        db_handler.update_user(username, updated_data)
        return redirect(url_for('users'))
    
# Deleting a User
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'username' not in session or session.get('role') != 'admin':
        return "Access Denied", 403

    username = request.form['username']
    db_handler.delete_user(username)
    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)