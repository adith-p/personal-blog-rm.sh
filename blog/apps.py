from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        from .utls.filesystem import FileSystem

        if not FileSystem.does_exist():
            FileSystem.create_folder("posts")
