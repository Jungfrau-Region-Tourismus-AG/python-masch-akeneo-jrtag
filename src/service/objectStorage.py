import json
from os import getenv
from dotenv import find_dotenv, load_dotenv
import boto3
load_dotenv(find_dotenv())

OBJECTSTORAGE_ENDPOINT = getenv('OBJECTSTORAGE_ENDPOINT')
OBJECTSTORAGE_BUCKET = getenv('OBJECTSTORAGE_BUCKET')
OBJECTSTORAGE_REGION = getenv('OBJECTSTORAGE_REGION')
OBJECTSTORAGE_ACCESS_KEY = getenv('OBJECTSTORAGE_ACCESS_KEY')
OBJECTSTORAGE_SECRET_ACCESS_KEY = getenv('OBJECTSTORAGE_SECRET_ACCESS_KEY')
OBJECTSTORAGE_EXPORT_PATH = getenv('OBJECTSTORAGE_EXPORT_PATH')

OBJECTSTORAGE_EXPORT_PATH_PRODUCTS = OBJECTSTORAGE_EXPORT_PATH+str("products/")

def s3client():
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=OBJECTSTORAGE_ACCESS_KEY,
        aws_secret_access_key=OBJECTSTORAGE_SECRET_ACCESS_KEY,
        endpoint_url='https://sos-'+OBJECTSTORAGE_REGION+'.'+OBJECTSTORAGE_ENDPOINT,
    )
    return s3_client

def putObject(data, filename):
    s3 = s3client()
    s3.put_object(
        Bucket=OBJECTSTORAGE_BUCKET,
        Key=filename,
        Body=json.dumps(data),
        ACL='public-read',
        ContentType='application/json')
    
def loadProduct(product):
    putObject(product, OBJECTSTORAGE_BUCKET, OBJECTSTORAGE_EXPORT_PATH_PRODUCTS+product['identifier']+"/index.json")

def putPorductIndex(products):
    putObject(products, OBJECTSTORAGE_BUCKET, OBJECTSTORAGE_EXPORT_PATH_PRODUCTS+"index.json")

def load(products):
    print("Loading data to target")
    print(products)
    productIndex = []
    for product in products:
        print(product)
        putObject(product, OBJECTSTORAGE_BUCKET, OBJECTSTORAGE_EXPORT_PATH_PRODUCTS+product['identifier']+"/index.json")
        # Add to Product Index
        sku = product['identifier']
        productRow = {}
        if 'name' in product['values']:
            name = product['values']['name'][0]['data']
        else :
            name = ""
        if 'family' in product['values']:
            family = product['values']['family'][0]['data']
        else :
            family = ""
        productRow[sku] = {
            "identifier": product['identifier'],
            "name": name,
            "family": family,
            "created": product['created'],
            "updated": product['updated'],
        }
        productIndex.append(productRow)

    putPorductIndex(productIndex)

# clear Object Storage - all Objekct in export/contentdesk/products
def clearObjectStorage():
    s3 = s3client()
    response = s3.list_objects_v2(Bucket=OBJECTSTORAGE_BUCKET, Prefix=OBJECTSTORAGE_EXPORT_PATH_PRODUCTS)
    if 'Contents' in response:
        for content in response['Contents']:
            print("Deleting "+content['Key'])
            s3.delete_object(Bucket=OBJECTSTORAGE_BUCKET, Key=content['Key'])

# get Object from Object Storage
def getObject(filename):
    s3 = s3client()
    response = s3.get_object(Bucket=OBJECTSTORAGE_BUCKET, Key=filename)
    data = json.loads(response['Body'].read())
    return data

def getObjects(uploadList):
    productList = {}
    for product in uploadList:
        print(product)
        print(OBJECTSTORAGE_EXPORT_PATH_PRODUCTS+product+"/index.json")
        productList[product] = getObject(OBJECTSTORAGE_EXPORT_PATH_PRODUCTS+product+"/index.json")
    return productList

# remove Object from Object Storage
def removeObject(filename):
    s3 = s3client()
    s3.delete_object(Bucket=OBJECTSTORAGE_BUCKET, Key=filename)

# count files in folder in Object Storage
def countFilesInFolder(folder):
    s3 = s3client()
    response = s3.list_objects_v2(Bucket=OBJECTSTORAGE_BUCKET, Prefix=folder)
    if 'Contents' in response:
        return len(response['Contents'])
    else:
        return 0

# check if folder exist in Object Storage
def folderExist(folder):
    s3 = s3client()
    response = s3.list_objects_v2(Bucket=OBJECTSTORAGE_BUCKET, Prefix=folder)
    if 'Contents' in response:
        return True
    else:
        return False