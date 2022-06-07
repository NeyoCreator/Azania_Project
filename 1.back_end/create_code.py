import qrcode

#1.Obtain data
icon_url = input("What is icon url")
name= input("What is your name?")
first_location= input("What is your first location?")
last_location=input("What is your last location")

#2.Store Data Dictionary
user_data= {"icon_url":icon_url,"name": name, "first_location":first_location,"last_location":last_location}

#CREATE QR CODE
img=qrcode.make(user_data)
img.save(f"{name}_code.png")
