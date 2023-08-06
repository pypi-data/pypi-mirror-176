import azure.core.exceptions
import azure.identity
import azure.storage.blob
import google.cloud.storage
import pytest
from cpg_utils.deploy_config import set_deploy_config_from_env
from cpg_utils.storage import clear_data_manager, DataManager, get_data_manager, get_dataset_bucket_url


class MockStorageResponse:
    def __init__(self, blob_contents):
        self.value = bytes(blob_contents, "UTF-8")
    def download_as_bytes(self):
        return self.value
    def readall(self):
        return self.value
    def open(self, mode):
        assert mode == "wb"
        return self
    def __enter__(self):
        return self
    def write(self, contents):
        pass
    def __exit__(self, type, value, traceback):
        pass

class MockStorageClientGCP:
    def bucket(self, bucket_name):
        assert bucket_name in ["cpg-dataset0-main-read", "cpg-config"]
        return self
    def get_blob(self, blob_path):
        if blob_path in ["missing.json", "missing.toml"]:
            return None
        if blob_path == "config.toml":
            return MockStorageResponse(
                """[hail]
                billing_project = "dataset0"
                bucket = "gs://cpg-dataset0-hail"
                [workflow]
                access_level = "pytestgcp"
                """
            )
        assert blob_path == "exists.json"
        return MockStorageResponse("GCP BLOB CONTENTS")
    def blob(self, blob_path):
        return MockStorageResponse("nothing")

class MockStorageClientAzure:
    def __init__(self, *args, **kwargs):
        if len(args) > 2:
            assert args[0] in ["https://dataset1_idsa.blob.core.windows.net", "https://analysis-runnersa.blob.core.windows.net"]
            assert args[1] in ["main-read", "config"]
            self.path = args[2]
    def download_blob(self):
        if self.path == "missing.json":
            raise azure.core.exceptions.ResourceNotFoundError()
        if self.path == "config.toml":
            return MockStorageResponse(
                """[hail]
                billing_project = "dataset1"
                bucket = "hail-az://dataset1_idsa/hail"
                [workflow]
                access_level = "pytestaz"
                """
            )
        assert self.path == "exists.json"
        return MockStorageResponse("AZURE BLOB CONTENTS")
    def upload_blob(self, data: bytes, overwrite: bool):
        pass

@pytest.fixture
def mock_config_fixture(json_load):
    def mock_get_server_config():
        return json_load("server_config_01.json")
    return mock_get_server_config


def test_gcp_storage(monkeypatch):
    monkeypatch.setattr(google.cloud.storage, "Client", MockStorageClientGCP)
    monkeypatch.setenv("CLOUD", "gcp")
    set_deploy_config_from_env()
    sm = get_data_manager()

    assert sm.get_blob("dataset0", "main-read", "exists.json").decode("UTF-8") == "GCP BLOB CONTENTS"
    assert sm.get_blob("dataset0", "main-read", "missing.json") == None
    sm.set_blob("dataset0", "main-read", "exists.json", bytes("GCP BLOB CONTENTS", "UTF-8"))

    assert get_dataset_bucket_url("dataset0", "test") == "gs://cpg-dataset0-test"


def test_azure_storage(monkeypatch, mock_config_fixture):
    monkeypatch.setattr("cpg_utils.storage.get_server_config", mock_config_fixture)
    monkeypatch.setattr(azure.identity, "DefaultAzureCredential", MockStorageClientAzure)
    monkeypatch.setattr(azure.storage.blob, "BlobClient", MockStorageClientAzure)
    monkeypatch.setenv("CLOUD", "azure")
    monkeypatch.delenv("CPG_DEPLOY_CONFIG", raising=False)
    set_deploy_config_from_env()
    sm = DataManager.get_data_manager()

    assert sm.get_blob("dataset1", "main-read", "exists.json").decode("UTF-8") == "AZURE BLOB CONTENTS"
    assert sm.get_blob("dataset1", "main-read", "missing.json") == None
    with pytest.raises(ValueError) as e:
        sm.get_blob("dataset0", "main-read", "exists.json")
        assert "No such dataset in server config" in str(e.value)
    sm.set_blob("dataset1", "main-read", "exists.json", bytes("AZURE BLOB CONTENTS", "UTF-8"))
    with pytest.raises(ValueError) as e:
        sm.set_blob("dataset0", "main-read", "exists.json", bytes("AZURE BLOB CONTENTS", "UTF-8"))
        assert "No such dataset in server config" in str(e.value)

    clear_data_manager()
    assert sm.get_dataset_bucket_url("dataset1", "test") == "hail-az://dataset1_idsa/test"
