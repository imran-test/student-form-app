from flask import Flask, render_template, request, redirect
import boto3

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')

@app.route('/', methods=['GET'])
def index():
    # Fetch student list from DynamoDB
    response = table.scan()
    students = response.get('Items', [])
    return render_template('index.html', students=students)

@app.route('/submit', methods=['POST'])
def submit():
    student_id = request.form['student_id']
    name = request.form['name']
    age = request.form['age']
    course = request.form['course']

    table.put_item(Item={
        'student_id': student_id,
        'name': name,
        'age': age,
        'course': course
    })

    return redirect('/')
