from pyweb.models import User, Category, Medicine, UserRole
from pyweb import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login import logout_user
from flask import redirect

admin = Admin(app=app, name='QUẢN TRỊ VIÊN', template_mode='bootstrap4')


class AuthenticatedBaseView(BaseView):
    def is_visible(self):
        return current_user.is_authenticated


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')


class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_filters = ['name', 'price']
    column_searchable_list = ['name', 'describe']
    column_labels = {
        'name': 'tên thuốc',
        'describe': 'mô tả',
        'price': 'giá bán',
        'image': 'ảnh',
        'active': 'còn thuốc',
        'type': 'đơn vị thuốc',
        'category': ' loại thuốc',
    }
    # khoong biet len day tim hieu https://flask-admin.readthedocs.io/en/latest/api/mod_model/


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class UserView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/listuser.html')


admin.add_view(AuthenticatedModelView(Category, db.session, name=" Danh Sach Loai thuoc"))
admin.add_view(MedicineView(Medicine, db.session, name="Danh Sach Thuoc"))
admin.add_view(AuthenticatedModelView(User, db.session, name='danh sách user'))
admin.add_view(StatsView(name='Thông kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
