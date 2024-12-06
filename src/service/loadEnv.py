import os
from dotenv import load_dotenv
import glob

def loadEnv(environment):
    # Load environment variables from the file
    print(f'ENV - Loading .env.{environment}')
    dotenvPath = '../env/.env.' + environment
    load_dotenv(dotenvPath, override=True)

    env = {}
    # Access the environment variables
    env['name'] = environment
    env['host'] = os.getenv("AKENEO_HOST")
    env['clientId'] = os.getenv("AKENEO_CLIENT_ID")
    env['secret'] = os.getenv("AKENEO_CLIENT_SECRET")
    env['user'] = os.getenv("AKENEO_USERNAME")
    env['passwd'] = os.getenv("AKENEO_PASSWORD")
    env['userLocal'] = os.getenv("USER")
    env['passwdLocal'] = os.getenv("PASSWORD")

    # Use the environment variables in your code
    return env

# Specify the path to your environment file
#env_file_path = "/path/to/your/env/file.env"

# Call the function to load the environment variables
#load_env_from_file(env_file_path)


def getEnvironment():
    # Find all .env.xxx files
    env_files = glob.glob('../../env/.env.*')
    env_suffixes = [os.path.splitext(file)[1][1:] for file in env_files]

    # Print the list of files
    print(env_suffixes)
    return env_suffixes