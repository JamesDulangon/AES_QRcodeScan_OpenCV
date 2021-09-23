import cv2
import numpy
from pyzbar.pyzbar import decode

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()

    for qrcode in decode(frame):
        data = qrcode.data.decode('utf-8')
        print(data)

        # AES Decryption
        ct = b64decode(data)
        cipher = AES.new("11111111111111111111111111111111".encode(
            'utf-8'), AES.MODE_CBC, "1111111111111111".encode('utf-8'))
        data = unpad(cipher.decrypt(ct), AES.block_size)
        data = data.decode()

        cd = numpy.array([qrcode.polygon], numpy.int32)
        cd = cd.reshape((-1, 1, 2))
        cv2.polylines(frame, [cd], True, (0, 255, 0), 3)
        cd_rect = qrcode.rect
        cv2.putText(frame, data, (cd_rect[0], cd_rect[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('QR code scan', frame)
    cv2.waitKey(1)
