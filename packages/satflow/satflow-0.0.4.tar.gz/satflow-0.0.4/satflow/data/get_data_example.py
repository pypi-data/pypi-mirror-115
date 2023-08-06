import numpy as np
# NIR1.6, VIS0.8 and VIS0.6 RGB for near normal view
from satflow.data.datamodules import SatFlowDataModule
import webdataset as wds
import yaml
import torch
import urllib.request
url = "https://github.com/openclimatefix/satflow/releases/download/v0.0.3/input_0.pth"
filename, headers = urllib.request.urlretrieve(url, filename="input_0.pth")
data = torch.load(filename)
print(data.size())
exit()
def load_config(config_file):
    with open(config_file, "r") as cfg:
        return yaml.load(cfg, Loader=yaml.FullLoader)

config = load_config("/home/jacob/Development/satflow/satflow/configs/datamodule/metnet_datamodule.yaml")

cloudflow = SatFlowDataModule(**config)

cloudflow.setup()

for i, b in enumerate(cloudflow.train_dataloader()):
    image, target = b
    torch.save(image, f"input_{i}.pth")
    torch.save(target, f"output_{i}.pth")
    if i > 10:
        exit()
