from sqladmin.models import ModelView

from app.users.models import Users


class UserAdminView(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [Users.id, Users.email, Users.booking]
    column_searchable_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.password]
    icon = "fa-solid fa-user"
    can_create = False
    can_delete = False
    can_export = False
