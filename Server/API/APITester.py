import os
import sys
sys.path.append(os.path.abspath("../../Client"))
import seeshell_client_common as common
import uuid

api = common.SeeShellAPIClient("http://localhost:5000")

print(api.createAccount("tester", "test@seeshell.com", "testPassword"))
print(api.checkPass("tester", "testPassword"))


file = open("/Users/eron/Downloads/genus/Aandara/Aandara_consociata_1_A.jpg", "rb")
print(api.uploadImage(str(uuid.uuid4()), file))