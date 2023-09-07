import os

def random_id():
  return os.system("""python -c "import secrets; print(secrets.token_hex()[:7])"""")
                   
def random_uid():
  return os.system("""python -c "import uuid; print(uuid.uuid4())"""")
