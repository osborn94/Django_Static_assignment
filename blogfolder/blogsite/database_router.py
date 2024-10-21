class AppDatabaseRouter:
    """
    A router to control database operations for different apps.
    """

    def db_for_read(self, model, **hints):
        """
        Direct read operations for specific models to a different database.
        """
        if model._meta.app_label == 'home':
            return 'default'
        elif model._meta.app_label == 'student':
            return 'other_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Direct write operations for specific models to a different database.
        """
        if model._meta.app_label == 'home':
            return 'default'
        elif model._meta.app_label == 'student':
            return 'other_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if models are from the same app or between the 'home' and 'student' apps.
        """
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        elif (obj1._meta.app_label == 'home' and obj2._meta.app_label == 'student') or \
             (obj1._meta.app_label == 'student' and obj2._meta.app_label == 'home'):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that models are only migrated to the appropriate database.
        """
        if app_label == 'home':
            return db == 'default'
        elif app_label == 'student':
            return db == 'other_db'
        return None
