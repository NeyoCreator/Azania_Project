user_list =[{"id": 1, "username": "neo25722", "balance": 80}, {"id": 2, "username": "nqobile", "balance": 120}, {"id": 3, "username": "pride", "balance": 100}]

user_name = "nqobile"


for index, value in enumerate(user_list):
     if user_name == value["username"]:
          print("we have a match")
     else :
          print("we have nothing")


