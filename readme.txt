
- python node1.py
- python node2.py
- python node3.py

--------------------------------------------------------------------------------------------

# Requests

# Node 1

[GET] - 
http://localhost:5000/read_file

[POST] -
http://localhost:5000/token_status
http://localhost:5000/request_token
http://localhost:5000/write_file
http://localhost:5000/append_file
http://localhost:5000/release_token


# Node 2

[GET] - 
http://localhost:5001/read_file

[POST] -
http://localhost:5001/token_status
http://localhost:5001/request_token
http://localhost:5001/write_file
http://localhost:5001/append_file


# Node 3

[GET] - 
http://localhost:5002/read_file

[POST] -
http://localhost:5002/token_status
http://localhost:5002/request_token
http://localhost:5002/write_file
http://localhost:5002/append_file