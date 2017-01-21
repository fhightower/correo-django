from django.contrib import admin

# from .models import Email, Attachment, Host, IPAddress, Url, UrlPath
# from .models import Email, Host, IPAddress
from .models import Email, Host


admin.site.register(Email)
# admin.site.register(Attachment)
admin.site.register(Host)
# admin.site.register(IPAddress)
# admin.site.register(Url)
# admin.site.register(UrlPath)
