import domino_mlflow_client as dmc
import domino_mlflow_client.tag_constants as constants
import secrets
from kubernetes import client, config
from kubernetes.client.models.v1_secret import V1Secret
from domino_mlflow_client import DominoMLFlowClient as dmc
import os

class ServiceAccountClient:
    @staticmethod
    def generate_service_account(domino_project_id, domino_project_name, domino_project_owner,
                                 tags={}):
        tags[constants.TAG_DOMINO_HARDWARE_TIER_ID] = os.getenv("DOMINO_HARDWARE_TIER_ID", "")
        tags[constants.TAG_DOMINO_PROJECT_OWNER] = os.getenv("DOMINO_PROJECT_OWNER", "")
        tags[constants.TAG_DOMINO_PROJECT_OWNER] = domino_project_owner
        tags[constants.TAG_DOMINO_PROJECT_ID] = domino_project_id
        domino_run_id = None
        encoded_jwt = dmc.generate_mlflow_token(secrets.token_urlsafe(64),domino_project_name,domino_run_id,tags)
        return encoded_jwt

    @staticmethod
    def save_mlflow_service_account(domino_project_id, mlflow_api_token, k8s_namespace,
                                    k8s_secret_name='mlflow-model-secret'):
        try:
            config.load_incluster_config()
        except:
            print('Loading local k8s config')
            config.load_kube_config()
        v1 = client.CoreV1Api()
        secrets_body: V1Secret = v1.read_namespaced_secret(k8s_secret_name, k8s_namespace)
        if (secrets_body.string_data == None):
            secrets_body.string_data = {}
        secrets_body.string_data[f'{domino_project_id}.apikey'] = mlflow_api_token
        #print(v1.patch_namespaced_secret(k8s_secret_name,k8s_namespace,secrets_body))
        #print(v1.read_namespaced_secret(k8s_secret_name, k8s_namespace))

if __name__ == "__main__":
    from domino_mlflow_client import  ServiceAccountClient as sac
    svc_jwt = sac.generate_service_account("abc","abc_name", "abc_owner")
    sac.save_mlflow_service_account("abc",svc_jwt,"mlflow-efs")