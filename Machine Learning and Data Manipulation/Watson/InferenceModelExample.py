import json
import tensorflow as tf
import matplotlib.pyplot as plt
from ibm_watson_machine_learning import APIClient

with open("../config.json", "r") as f:
    mlConfig = json.load(f)
with open("config.json", "r") as f:
    watsonConfig = json.load(f)

img = tf.keras.utils.img_to_array(tf.keras.utils.load_img("../../../genus/Aandara/Aandara_consociata_1_A.jpg", target_size=(mlConfig["imageSize"]["height"], mlConfig["imageSize"]["width"])))

print(img.shape)

plt.imshow(img/255)
plt.show()

wml_credentials = {
                   "url": watsonConfig["url"],
                   "apikey":watsonConfig["apiKey"]
                  }

client = APIClient(wml_credentials)
client.set.default_space(watsonConfig["spaceUID"])

scoring_payload = {"input_data": [{"values": [img.tolist()]}]}

predictions = client.deployments.score(watsonConfig["deploymentUID"], scoring_payload)

print(json.dumps(predictions, indent=2))