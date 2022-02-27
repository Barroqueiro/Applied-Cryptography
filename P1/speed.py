import uuid;
import subprocess
file_to_encrypt = "to_encrypt.txt"
n = 0
for i in range(n):
    enc_key = uuid.uuid4().hex.upper()
    shuffle_key = uuid.uuid4().hex.upper()
    #print('python3 encrypt.py '+ enc_key + " " + shuffle_key + " -t times_enc_saes.txt < " + file_to_encrypt + " > temp_file")
    result = subprocess.run(['python3 encrypt.py -n '+ enc_key + " -s " + shuffle_key + " -t times_enc_shuffle_saes.txt < " + file_to_encrypt + " > temp_file",''], stdout=subprocess.PIPE,shell=True)
    result = subprocess.run(['python3 decrypt.py -n '+ enc_key +" -s "+shuffle_key+ ' -t times_dec_shuffle_saes.txt < temp_file',''], stdout=subprocess.PIPE,shell=True)

for i in range(n):
    enc_key = uuid.uuid4().hex.upper()
    shuffle_key = uuid.uuid4().hex.upper()
    #print('python3 encrypt.py -n '+ enc_key + " -t times_enc_normal_saes.txt < " + file_to_encrypt + " > temp_file")
    result = subprocess.run(['python3 encrypt.py -n '+ enc_key + " -t times_enc_normal_saes.txt < " + file_to_encrypt + " > temp_file",''], stdout=subprocess.PIPE,shell=True)
    result = subprocess.run(['python3 decrypt.py -n '+ enc_key +' -t times_dec_normal_saes.txt < temp_file',''], stdout=subprocess.PIPE,shell=True)

for i in range(n):
    #print('python3 cryptography_speed.py < '+ file_to_encrypt)
    result = subprocess.run(['python3 cryptography_speed.py < '+ file_to_encrypt,''], stdout=subprocess.PIPE,shell=True)

for i in range(n):
    #print('python3 pycrypto_speed.py < '+ file_to_encrypt)
    result = subprocess.run(['python3 pycrypto_speed.py < '+ file_to_encrypt,''], stdout=subprocess.PIPE,shell=True)


files = ['times_dec_normal_saes.txt','times_enc_normal_saes.txt','times_dec_shuffle_saes.txt',
'times_enc_shuffle_saes.txt','times_dec_pycrypto_aes.txt','times_enc_pycrypto_aes.txt',
'times_dec_cryptography_aes.txt','times_enc_cryptography_aes.txt']

minimo = 99999999

for f in files:
    with open(f,"r") as fi:
        minimo = 99999999
        line = fi.readline()
        while line:
            flo = float(line)
            if flo < minimo:
                minimo = flo
            line = fi.readline()
    print(f+" -> "+ str(minimo))



