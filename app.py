from flask import Flask, render_template, request, redirect, flash, session
from models.database import get_connection
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/donor/register', methods=['GET', 'POST'])
def donor_register():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'email': request.form['email'],
            'blood_group': request.form['blood_group'],
            'mobile': request.form['mobile'],
            'city': request.form['city'],
            'zip_code': request.form['zip_code'],
            'state': request.form['state'],
            'donation_date': request.form['donation_date']
        }

        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO donors (name, age, email, blood_group, mobile, city, zip_code, state, donation_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['name'], data['age'], data['email'], data['blood_group'],
            data['mobile'], data['city'], data['zip_code'],
            data['state'], data['donation_date']
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        flash("Thank you for your donation!", "success")
        return redirect('/donor/register')

    return render_template('donor_form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM admins WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect('/admin/dashboard')
        else:
            flash("Invalid credentials. Try again.", "danger")
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect('/login')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # <-- Get column names dynamically
    cursor.close()
    conn.close()

    return render_template('dashboard.html', donors=donors, columns=columns)



@app.route('/anonymize/options', methods=['POST'])
def anonymize_options():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    method = request.form.get('method')
    k_value = request.form.get('k_value')
    l_value = request.form.get('l_value')
    selected_columns = request.form.getlist('columns')  # <-- Capture checked columns

    if method not in ['k', 'l', 'masking']:
        flash("Invalid method selected!", "danger")
        return redirect('/admin/dashboard')

    if not selected_columns:
        flash("Please select at least one column.", "danger")
        return redirect('/admin/dashboard')

    session['anonymization_method'] = method
    session['selected_columns'] = selected_columns  # <-- Save columns in session

    if method == 'k' and k_value:
        session['k_value'] = int(k_value)
    if method == 'l' and l_value:
        session['l_value'] = int(l_value)

    return redirect('/anonymize/preview')



from utils.anonymizer import apply_k_anonymity, apply_l_diversity, apply_data_masking

@app.route('/anonymize/preview')
def anonymize_preview():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    method = session.get('anonymization_method')
    selected_columns = session.get('selected_columns')
    if not method or not selected_columns:
        flash("Missing anonymization settings.", "danger")
        return redirect('/admin/dashboard')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    import pandas as pd
    df = pd.DataFrame(donors, columns=columns)

    # Dynamic K and L values
    k_value = session.get('k_value', 1)
    l_value = session.get('l_value', 1)

    if method == 'k':
        anonymized_df = apply_k_anonymity(df, selected_columns=selected_columns, k=k_value)
    elif method == 'l':
        anonymized_df = apply_l_diversity(df, selected_columns=selected_columns, k=k_value, l=l_value)
    elif method == 'masking':
        anonymized_df = apply_data_masking(df, selected_columns=selected_columns)

    import os
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    anonymized_df.to_csv('outputs/anonymized.csv', index=False)

    preview_html = anonymized_df.head(10).to_html(classes="table table-bordered", index=False)

    return render_template('preview.html', preview_html=preview_html)


from flask import send_file

from datetime import datetime
from flask import send_file, after_this_request

@app.route('/anonymize/download')
def anonymize_download():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f'outputs/anonymized_{timestamp}.csv'

    # Copy the last saved anonymized.csv to timestamped filename
    import shutil
    shutil.copy('outputs/anonymized.csv', new_filename)

    # After sending the file, clear session variables
    @after_this_request
    def clear_session(response):
        session.pop('anonymization_method', None)
        session.pop('selected_columns', None)
        session.pop('k_value', None)
        session.pop('l_value', None)
        return response

    flash('Anonymized file downloaded successfully!', 'success')
    return send_file(new_filename, as_attachment=True)




# Always put this LAST
if __name__ == '__main__':
    app.run(debug=True)
