from flask import Flask, request, render_template_string, redirect, url_for
import boto3
from uuid import uuid4
import os
import json

app = Flask(__name__)

# Version will be updated during the lab
VERSION = "v1.0.0"
ENVIRONMENT = "ENVIRONMENT_PLACEHOLDER"

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('multi-stage-app-user-data')

# Simple HTML template with form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Stage Deployment Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            display: inline-block;
            min-width: 80%;
            margin: 0 auto;
        }
        h1 {
            color: #333;
        }
        .version {
            font-weight: bold;
        }
        .environment {
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px;
        }
        .dev {
            background-color: #ffeb3b;
            color: #333;
        }
        .test {
            background-color: #03a9f4;
            color: white;
        }
        .prod {
            background-color: #4caf50;
            color: white;
        }
        form {
            margin: 20px 0;
            text-align: left;
            max-width: 500px;
            margin: 0 auto;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-Stage Deployment Demo</h1>
        <p>Running version: <span class="version">{{ version }}</span></p>
        <div class="environment {{ environment.lower() }}">
            Environment: {{ environment }}
        </div>
        
        <form method="post">
            <h3>Add User Data</h3>
            <div>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div>
                <label for="message">Message:</label>
                <textarea id="message" name="message" rows="3"></textarea>
            </div>
            <button type="submit">Submit</button>
        </form>
        
        <div>
            <h3>Stored User Data</h3>
            <table>
                <thead>
                    <tr>
                        <th>User ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.user_id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.message }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Generate a unique ID
        user_id = str(uuid4())
        
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Save to DynamoDB
        table.put_item(
            Item={
                'user_id': user_id,
                'name': name,
                'email': email,
                'message': message
            }
        )
        
        return redirect(url_for('index'))
    
    # Get all items from DynamoDB
    try:
        response = table.scan()
        users = response.get('Items', [])
    except Exception as e:
        users = []
        print(f"Error scanning DynamoDB: {e}")
    
    return render_template_string(
        HTML_TEMPLATE, 
        version=VERSION, 
        environment=ENVIRONMENT,
        users=users
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)