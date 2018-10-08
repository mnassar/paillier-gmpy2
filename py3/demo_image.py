from paillier_gmpy2 import *
import cv2
import numpy as np
img_file= './lena512.bmp'
img = cv2.imread(img_file,0)
height, width = img.shape
priv, pub=generate_keypair(128)
all_enc = np.zeros([height,width], dtype=object)
all_dec = np.zeros([height,width])
for x in range(height):
    for y in range(width):
        cpixel = img[x, y]
        all_enc[x,y]=encrypt(pub, int(cpixel))

for x in range(height):
    for y in range(width):
        cpixel = all_enc[x, y]
        all_dec[x,y]=decrypt(priv, pub, cpixel)

Re_img = all_dec.astype(np.uint8)
cv2.imshow('image',Re_img)
cv2.waitKey(0)
cv2.imwrite('./reimage.bmp',Re_img)
cv2.destroyAllWindows()
