from ibm_watson_machine_learning import APIClient
import json

with open("config.json", "r") as f:
    config = json.load(f)

wml_credentials = {
                   "url": config["url"],
                   "apikey":config["apiKey"]
                  }

client = APIClient(wml_credentials)
client.set.default_space(config["spaceUID"])
print(client.software_specifications.list())
sw_spec_uid = client.software_specifications.get_uid_by_name(config["softwareSpecification"])

meta_props = {
    client.repository.ModelMetaNames.NAME: "SeaShellClassifier",
    client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: sw_spec_uid,
    client.repository.ModelMetaNames.TYPE: config["modelType"]}

client.repository.store_model(model="../model_prod", meta_props=meta_props)