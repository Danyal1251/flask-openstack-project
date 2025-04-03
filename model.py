from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    api = KaggleApi()
    api.authenticate()  # ✅ Important step
    
    dataset = "joelkunjachan/human-behaviour-analysis"
    api.dataset_download_files(dataset, path="./model", unzip=True)  # ✅ Correct method

download_dataset()
