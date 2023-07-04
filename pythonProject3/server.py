from flask import Flask, request, render_template, jsonify
from llama_index.readers import ChatGPTRetrievalPluginReader
from llama_index import ListIndex
import requests
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# 삭제 요청
@app.route('/send_delete', methods=['POST'])
def send_delete():
    delete_name = request.form.get('dname')

    url = 'http://127.0.0.1:8000/delete'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZscWhlbDMwODZAZ21haWwuY29tIiwibmFtZSI6IlNldW5nS3l1IExlZSIsInBhc3N3b3JkIjoiZG9uZ3lhbmcifQ.lZa62X2IVa-j4sGGoi1vQXKjiGle8Rki_fctf9KC4hg'
    }

    data = {
        "filter": {
            "document_id": delete_name,
        },
        "delete_all": False
    }
    response = requests.delete(url, headers=headers, json=data)

    return render_template('index.html', response='삭제 요청 완료')

# 전체 삭제 요청
@app.route('/send_all_delete', methods=['POST'])
def send_all_delete():
    url = 'http://127.0.0.1:8000/delete'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZscWhlbDMwODZAZ21haWwuY29tIiwibmFtZSI6IlNldW5nS3l1IExlZSIsInBhc3N3b3JkIjoiZG9uZ3lhbmcifQ.lZa62X2IVa-j4sGGoi1vQXKjiGle8Rki_fctf9KC4hg'
    }
    data = {
        "delete_all": True
    }

    response = requests.delete(url, headers=headers, json=data)

    return render_template('index.html', response='삭제 요청 완료')


# 파일 업로드 요청
@app.route('/send_request', methods=['POST'])
def send_request():
    url = 'http://127.0.0.1:8000/upsert-file'

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZscWhlbDMwODZAZ21haWwuY29tIiwibmFtZSI6IlNldW5nS3l1IExlZSIsInBhc3N3b3JkIjoiZG9uZ3lhbmcifQ.lZa62X2IVa-j4sGGoi1vQXKjiGle8Rki_fctf9KC4hg'
    }

    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    if file:
        # Check file extension to set the correct MIME type
        if file.filename.endswith('.pdf'):
            mime_type = 'application/pdf'
        elif file.filename.endswith('.csv'):
            mime_type = 'text/csv'
        else:
            return 'Unsupported file type'

        files = {
            'file': (file.filename, file, mime_type)
        }
        data = {
            'metadata': 'your metadata here'
        }
        response = requests.post(url, headers=headers, files=files, data=data)

    return render_template('index.html', response='업로드 요청 완료')


# GPT 통신
@app.route('/action_page', methods=['POST'])
def action_page():
    first_name = request.form.get('fname')
    bearer_token = os.getenv("BEARER_TOKEN")

    reader = ChatGPTRetrievalPluginReader(
        endpoint_url="http://127.0.0.1:8000",
        bearer_token=bearer_token
    )

    documents = reader.load_data(first_name)
    print(len(documents))

    index = ListIndex(documents)
    query_engine = index.as_query_engine(response_mode="compact")
    response = query_engine.query(first_name)

    print(response)
    return render_template('index.html', response=response)


# 입력한 값 확인
@app.route('/get_data', methods=['POST'])
def get_data():
    url = 'http://127.0.0.1:8000/get_data'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZscWhlbDMwODZAZ21haWwuY29tIiwibmFtZSI6IlNldW5nS3l1IExlZSIsInBhc3N3b3JkIjoiZG9uZ3lhbmcifQ.lZa62X2IVa-j4sGGoi1vQXKjiGle8Rki_fctf9KC4hg'
    }
    data = {}

    response = requests.post(url, headers=headers, json=data)
    files = response.json()

    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
