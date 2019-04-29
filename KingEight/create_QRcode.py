import requests
from uuid import uuid4
import time,os
import hashlib
from settings import MONGO_DB,QR_URL,QRCODE_PATH

rq_text_list = []

for i in range(5):
    qr_text = hashlib.md5(f"{uuid4()}{time.time()}{uuid4()}".encode("utf8")).hexdigest()
    res = requests.get(QR_URL % (qr_text))

    qr_path = os.path.join(QRCODE_PATH,qr_text)
    with open(f"{qr_path}.jpg","wb") as f:
        f.write(res.content)

    device_dict = {"device_key":qr_text}
    rq_text_list.append(device_dict)



MONGO_DB.devices.insert_many(rq_text_list)