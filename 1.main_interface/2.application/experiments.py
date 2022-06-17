user_list =[{"id": 1, "username": "neo25722", "balance": 80}, {"id": 2, "username": "nqobile", "balance": 120}, {"id": 3, "username": "pride", "balance": 100}]

user_name = "nqobile"

for x,y in enumerate(user_list):
     if user_name ==user_list[x]["username"]:
          print("you exist")
     else:
          print("you don't exist")


