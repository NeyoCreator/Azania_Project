import qrcode
from pyzbar import pyzbar
from PIL import Image

#1.LOAD QR CODE
image = Image.open("pic.png")
qr_code = pyzbar.decode(image)[0]
#convert into string
data= qr_code.data.decode("utf-8")
type = qr_code.type
text = f"{type}-->, {data}"
print("----")
print(text)
print("----")