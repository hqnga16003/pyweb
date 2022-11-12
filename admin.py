from pyweb.models import TaiKhoan, LoaiThuoc, Thuoc
from pyweb import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

admin = Admin(app=app, name='QUẢN TRỊ VIÊN', template_mode='bootstrap4')


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated


# class UserView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/listuser.html')
#
#     def is_accessible(self):
#         return current_user.is_authenticated


admin.add_view(ModelView(LoaiThuoc, db.session, name=" Danh Sach Loai thuoc"))
admin.add_view(ModelView(Thuoc, db.session, name="Danh Sach Thuoc"))
admin.add_view(ModelView(TaiKhoan, db.session, name='danh sách user'))
admin.add_view(StatsView(name='Thông kê'))
