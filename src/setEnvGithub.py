import requests
import json
from base64 import b64encode
from nacl import encoding, public
from os import getenv
import os
from dotenv import find_dotenv, load_dotenv
import glob

load_dotenv(find_dotenv())

GITHUB_TOKEN = getenv('GITHUB_TOKEN')
GITHUB_OWNER = getenv('GITHUB_OWNER')
GITHUB_REPO = getenv('GITHUB_REPO')

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

def setHeaders(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }
    return headers

def createEnvironment(owner, repo, token, environment):
    headers = setHeaders(token)
    response = requests.put(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}', headers=headers)
    print(f'Created environment {environment}: {response.status_code}')
    print(response.text)

def getPublicKey(owner, repo, token, environment):
    headers = setHeaders(token)
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}/secrets/public-key', headers=headers)
    publicKey = response.json()
    print(f'Public key: {publicKey}')
    return publicKey

def createEncryptSecret(owner, repo, token, environment, secretName, secretValue, publicKey):
    headers = setHeaders(token)
    encrypted_secret = requests.put(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}/secrets/{secretName}', headers=headers, data=json.dumps({
            'encrypted_value': secretValue,
            'key_id': publicKey['key_id'],
        }))
    print(f'Added secret to {environment}: {encrypted_secret.status_code}')
    print(f'Secret {secretName} added to {owner}/{repo}')

def removeSecret(owner, repo, token, environment, secretName):
    headers = setHeaders(token)
    response = requests.delete(f'https://api.github.com/repos/{owner}/{repo}/environments/{environment}/secrets/{secretName}', headers=headers)
    print(f'Removed secret {secretName} from {environment}: {response.status_code}')
    print(response.text)

def getEnvironment():
    # Find all .env.xxx files
    env_files = glob.glob('env/.env.*')
    env_suffixes = [os.path.splitext(file)[1][1:] for file in env_files]

    # Print the list of files
    print(env_suffixes)
    return env_suffixes
    
def getSecrets(environment):
    # Load the .env file
    print(f'ENV - Loading .env.{environment}')
    dotenvPath = 'env/.env.' + environment
    # Secret to add
    load_dotenv(dotenvPath, override=True)
    # Set the environment variables
    env_vars = {}
    env_vars['OBJECTSTORAGE_ENDPOINT'] = getenv('OBJECTSTORAGE_ENDPOINT')
    env_vars['OBJECTSTORAGE_BUCKET'] = getenv('OBJECTSTORAGE_BUCKET')
    env_vars['OBJECTSTORAGE_REGION'] = getenv('OBJECTSTORAGE_REGION')
    env_vars['OBJECTSTORAGE_ACCESS_KEY'] = getenv('OBJECTSTORAGE_ACCESS_KEY')
    env_vars['OBJECTSTORAGE_SECRET_ACCESS_KEY'] = getenv('OBJECTSTORAGE_SECRET_ACCESS_KEY')
    env_vars['OBJECTSTORAGE_EXPORT_PATH'] = getenv('OBJECTSTORAGE_EXPORT_PATH')
    env_vars['OBJECTSTORAGE_CDN'] = getenv('OBJECTSTORAGE_CDN')
    env_vars['MASCH_URL'] = getenv('MASCH_URL')
    env_vars['MASCH_PULL_URL'] = getenv('MASCH_PULL_URL')
    env_vars['MASCH_PUSH_URL'] = getenv('MASCH_PUSH_URL')
    env_vars['MASCH_USER'] = getenv('MASCH_USER')
    env_vars['MASCH_PASSWORD'] = getenv('MASCH_PASSWORD')

    return env_vars

def main():
    # Personal Access Token
    token = GITHUB_TOKEN

    # Repository details
    owner = GITHUB_OWNER
    repo = GITHUB_REPO

    # Headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
    }

    # Environments to create
    #environments = ['test1', 'test2', 'test3']
    environments = getEnvironment()

    # Create environments
    # https://docs.github.com/de/rest/deployments/environments?apiVersion=2022-11-28#create-or-update-an-environment
    print(f'ENV - Creating environments for {owner}/{repo}')
    for env in environments:
        createEnvironment(owner, repo, token, env)

    # Add secret to environments
    # https://docs.github.com/de/rest/guides/encrypting-secrets-for-the-rest-api?apiVersion=2022-11-28#example-encrypting-a-secret-using-python
    print(f'SECRETS - Adding secrets to {owner}/{repo}')
    for env in environments:
        publicKeyEnv = getPublicKey(owner, repo, token, env)
        #print(f'Public key: {publicKeyEnv}')

        # Get secrets from .env file
        print(f'ENV - Getting secrets from .env.{env}')
        secrets = getSecrets(env)
        for key, value in secrets.items():
            print(f'{key}: {value}')
            secretValue = encrypt(publicKeyEnv['key'], value)
            print(f'Adding secret {key} to {env}')
            createEncryptSecret(owner, repo, token, env, key, secretValue, publicKeyEnv)

if __name__ == '__main__':
    main()