import os

def random_id():
  return os.system("""python -c "import secrets; print(secrets.token_hex()[:7])"""")

def random_uid():
  return os.system("""python -c "import uuid; print(uuid.uuid4())"""")

def remove_special_char():
  return os.system("""python -c "import re;print(re.sub(r'[^a-zA-Z0-9]+', '-', '').lower())"""")
