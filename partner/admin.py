
from django.contrib import admin

from accounts.models import partenaire, structure, option




admin.site.register(structure)

admin.site.register(partenaire)

admin.site.register(option)