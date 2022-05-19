# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# from Crypto.Protocol.KDF import PBKDF2

# salt = b'\xec\x86\xc6\xcao?3`.\xe8\x86\x0b\xcd?I\x8dV\x808c\x94\x03\x95~\xf3\xb7<iV\xd9\xe1\x01'
# passw = '$2b$12$EIYDWCtFLfqR1JFPEgDGgOz2xmUglTlTpzUHUNFRE80xI9zaZAcvq'
# key = PBKDF2(passw, salt, dkLen=32)

# # ciphered data
# string = b'\x904\xb6\x14\x88\xc9\x00p\x1d\x1a\xffi|\xc9\xcc\xf7'

# # file_in = open("test.bin", 'rb') 
# iv = b'`\xe0\x9a\xdc\xd8\x93\x96rD\x07\xb9\x06\x9d\\\xb6\xeb' # Read the iv out - this is 16 bytes long
# # file_in.close()

# # decryption
# cipher = AES.new(key, AES.MODE_CBC, iv=iv) 
# original_data = unpad(cipher.decrypt(string), AES.block_size)

# print(original_data.decode('utf-8'))

# data = {'driver' : {}}

# data['driver']['facebook'] = {}
# data['driver']['facebook']['tap'] = 1
# data['driver']['facebook']['status'] = 'connected'
# data['driver']['facebook']['expired'] = 20

# print(data)


# Python code to demonstrate
# to convert dictionary into string
# using json.dumps()

import ast
from webApplication.data import Facebook

# initialising dictionary
# test1 = { "testname" : "akshat",
# 		"test2name" : "manjeet",
# 		"test3name" : b"nikhil".decode('utf-8')}

# # print original dictionary
# print (type(test1))
# print ("initial dictionary = ", test1)

# # convert dictionary into string
# # using json.dumps()
# result = json.dumps(test1)

# # printing result as string
# result = json.loads(result)
# print ("\n", type(result))
# print ("final string = ", result['testname'])


# Python code to demonstrate
# to convert dictionary into string
# using str()
  
# initialising dictionary
test1 = { "testname" : "akshat",
          "test2name" : "manjeet",
          "test3name" : "nikhil"}
  
# print original dictionary
print (type(test1))
print ("initial dictionary = ", test1)
  
# convert dictionary into string
# using str
result = str(test1)
  
# print resulting string
print ("\n", type(result))
print ("final string = ", ast.literal_eval("ksjahgjskdlgkdslfghsdkljfh"))
print("Just TEsting")

# data = {
#     'driver': {
#         'facebook': {'tap': 1},
#         'twitter' : {'tap': -1}
#         }
#     }

# avialable = {}
# for account in data['driver']:
#     avialable[account] = data['driver'][account]['tap']

# print(avialable)

