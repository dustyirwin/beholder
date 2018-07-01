from django.contrib import admin
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from .models import ItemData
from .models import SessionData


class ItemDataAdmin(admin.ModelAdmin):
    readonly_fields = ('data_prettified',)

    def data_prettified(self, instance):
        """Function to display pretty version of our data"""

        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'


admin.site.register(ItemData, ItemDataAdmin)
