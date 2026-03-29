from import_export import resources

#clase para personalizar los nombres de las columnas

class CustomExportResource(resources.ModelResource):
    def get_export_headers(self, *args, **kwargs):
        headers = super().get_export_headers(*args, **kwargs)
        return [str(header).replace('_', ' ') for header in headers]
