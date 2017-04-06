import os
print os.environ.get('PORT')

print os.environ.get('HTTPS_PROXY')

print os.environ.get("PORT", 5000)