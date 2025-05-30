# client.py
import requests

url = "http://127.0.0.1:8000/run"

# payload = {
#     "code": "print('Hello from Python client!')",
#     "language": "python",
#     "input": ""
# }
payload = {
    "code": '''
#include <iostream>
using namespace std;
int main() {
    string name;
    cin >> name;
    cout << "Hello, " << name << "!" << endl;
    return 0;
}
''',
    "language": "cpp",
    "input": "Dinesh"
}




response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
