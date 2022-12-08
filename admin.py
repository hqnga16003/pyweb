from pyweb.models import User, Category, Medicine, UserRole, Unit
from pyweb import db, app, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login import logout_user
from flask import redirect, request, render_template

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


class TaoDanhSachKham(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        if request.method.__eq__('POST'):
            dao.create_medicalist(name=request.form.get('medicalexaminationday'))
        return self.render('admin/taodanhsachkham.html')


class XemDanhSachKham(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        medicalists = dao.load_medicalist()
        medi_id = request.args.get('medicalist_id')
        patients = dao.load_patient(medi_id)
        return self.render('admin/xemdanhsachkham.html',medicalists = medicalists,patients=patients)

class LapPhieuKham(AuthenticatedBaseView):
    @expose('/')
    def __index__(self):
        patients = dao.load_patient(dao.get_date_now())
        return self.render('admin/lapphieukham.html',patients=patients)

    @expose('/')
    def lap_phieu_kham(self):
        return self.render('admin/lapphieukham.html')


admin.add_view(AuthenticatedModelView(Category, db.session, name=" Danh Sach Loai thuoc"))
admin.add_view(AuthenticatedModelView(Unit, db.session, name="Đơn vị thuốc"))

admin.add_view(MedicineView(Medicine, db.session, name="Danh Sach Thuoc"))

admin.add_view(TaoDanhSachKham(name="Tạo danh sách khám"))
admin.add_view(XemDanhSachKham(name="Xem danh sách khám"))
admin.add_view(LapPhieuKham(name="Lập phiếu khám"))

admin.add_view(LogoutView(name='Đăng xuất'))
