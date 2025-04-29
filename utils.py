import os
import re
from datetime import datetime
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

# secrets retrieval
credential = DefaultAzureCredential()

# environment variables
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
AZURE_STORAGE_BLOB_URL = os.environ.get("AZURE_STORAGE_BLOB_URL")
AZURE_STORAGE_CONTAINER_PLANNER_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_PLANNER_NAME")
AZURE_STORAGE_CONTAINER_FEEDBACK_NAME = os.environ.get("AZURE_STORAGE_CONTAINER_FEEDBACK_NAME")
POSTGRESQL_USERNAME = os.environ.get("POSTGRESQL_USERNAME")
POSTGRESQL_HOST = os.environ.get("POSTGRESQL_HOST")
POSTGRESQL_DATABASE = os.environ.get("POSTGRESQL_DATABASE")

def get_secret(secret_name:str, credential)-> str:
    """Get secret from Azure Key Vault

    Args:
        secret_name (str): the name of the secret
        credential (_type_): the credential to access the key vault

    Returns:
        str: the value of the secret
    """
    secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
    retrieved_secret = secret_client.get_secret(secret_name)
    return retrieved_secret.value

# postresql utils
def connect_to_postgres(username:str = POSTGRESQL_USERNAME, 
                        password:str = get_secret("POSTGRESQL-PASSWORD", credential),
                        host:str = POSTGRESQL_HOST, 
                        database:str = POSTGRESQL_DATABASE):
    """Connect to the PostgreSQL database

    Args:
        username (str): the username to access the database
        password (str): the password to access the database
        host (str): the host of the database
        database (str): the name of the database

    Returns:
        _type_: the connection to the database
    """
    conn = psycopg2.connect(
    host = host,
    database = database,
    user = username,
    password = password)
    return conn

def get_list_passport(conn) -> list[str]:
    """Get a list of passports 
    from table 'passport_table' Azure database for PostgreSQL server

    Returns:
        List[str]: a list of passports
    """
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM passport_table;")
    return [r[0] for r in cursor.fetchall()]

def get_list_airport(conn) -> list[str]:
    """Get a list of airports excluding Thai airports
    from table 'airport' Azure database for PostgreSQL server

    Returns:
        List[str]: a list of airports excluding Thai airports
    """
    
    cursor = conn.cursor()
    cursor.execute("SELECT name | ' ' | aid FROM airport WHERE cid != 'TH';")
    return [r[0] for r in cursor.fetchall()]

# blob util
def upload_files_to_blob(files_to_upload: list[str], 
                         container_name: str,
                         account_url: str=AZURE_STORAGE_BLOB_URL,
                         credential=credential) -> None:
    """Upload files to Azure Blob Storage

    Args:
        files_to_upload (List[str]): file names to upload into the blob storage
        account_url (str): the url of the account
        credential (_type_): the credential to access the blob storage
        container_name (str): the name of the container

    Returns:
        None
    """
    
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    for local_file_path in files_to_upload:
        # Extract just the filename (e.g., 'my_text_file.txt')
        file_name = os.path.basename(local_file_path)

        # Add current datetime to the file name
        file_name = current_datetime+file_name
        
        # Create a blob client
        blob_client = blob_service_client.get_blob_client(container=container_name, 
                                                          blob=file_name)
        
        print(f"Uploading {file_name} to Azure Blob Storage...")

        # Open the local file and upload
        with open(local_file_path, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    print("✅ All files uploaded successfully!")

def upload_planner_files_to_blob():
    pattern = re.compile(r".*\.(txt|pdf)$")

    log_planner_path = "./log/planner"
    log_planner_files = [
        os.path.join(log_planner_path, filename)
        for filename in os.listdir(log_planner_path)
        if pattern.match(filename)
    ]

    result_planner_path = "./result/planner"
    result_planner_files = [
        os.path.join(result_planner_path, filename)
        for filename in os.listdir(result_planner_path)
        if pattern.match(filename)
    ]
    files_to_upload = log_planner_files + result_planner_files

    # upload them to blob
    upload_files_to_blob(files_to_upload=files_to_upload, container_name=AZURE_STORAGE_CONTAINER_PLANNER_NAME)

def upload_feedback_files_to_blob():
    feedback_path = "./result/feedback"
    files_to_upload = [
        os.path.join(feedback_path, filename)
        for filename in os.listdir(feedback_path)
    ]

    # upload them to blob
    upload_files_to_blob(files_to_upload=files_to_upload, container=AZURE_STORAGE_CONTAINER_FEEDBACK_NAME)

def upload_streamlit_multi_files_to_blob(uploaded_files: list,
                                         container_name: str=AZURE_STORAGE_CONTAINER_FEEDBACK_NAME,
                                         account_url: str=AZURE_STORAGE_BLOB_URL,
                                         credential=credential):

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    for uploaded_file in uploaded_files:
        # Extract just the filename (e.g., 'my_text_file.txt')
        file_name = uploaded_file.name

        # Add current datetime to the file name
        file_name = current_datetime+file_name
        
        # Create a blob client
        blob_client = blob_service_client.get_blob_client(container=container_name, 
                                                          blob=file_name)
        blob_client.upload_blob(uploaded_file, overwrite=True)

    print("✅ All files uploaded successfully!")
