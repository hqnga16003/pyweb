import datetime

from pyweb.models import User, Category, Medicine, UserRole, Unit
from pyweb import db, app, dao
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login import logout_user
from flask import redirect, request, render_template, session, jsonify, url_for
from datetime import date



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
        mes = ''
        if request.method.__eq__('POST'):
            name = request.form.get('medicalexaminationday')
            if not dao.kiem_tra_danh_sach_kham(name):
                dao.create_medicalist(name=request.form.get('medicalexaminationday'))
            else:
                mes = 'Ngày khám đã tạo '
        return self.render('admin/taodanhsachkham.html', mes=mes)


class XemDanhSachKham(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        i = 0
        medicalists = dao.load_medicalist()
        medi_id = request.args.get('medicalist_id')
        patients = dao.load_patient(medi_id)
        return self.render('admin/xemdanhsachkham.html', medicalists=medicalists, patients=patients,i=i)


class DanhSachThuoc(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def __index__(self):
        medicines = dao.load_medicines()
        quantity = request.form.get('quantity')
        id = request.form.get('code')
        unit = request.form.get('unit')
        name = request.form.get('name')
        price = request.form.get('price')

        if request.method.__eq__('POST'):
            medical_report = session.get('medical_report')
            if not medical_report:
                medical_report = {}

            if id in medical_report:
                (medical_report[id]['quantity']) = int(medical_report[id]['quantity']) + int(quantity)

            else:
                medical_report[id] = {
                    'id': id,
                    'name': name,
                    'unit': unit,
                    'quantity': quantity,
                    'price': price

                }
            session['medical_report'] = medical_report
        return self.render('admin/danhsachthuoc.html', medicines=medicines)


class DanhSachBenhNhan(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def __index__(self):
        p = dao.load_patient_in_patient_medicaList()

        return self.render('admin/danhsachbenhnhan.html', p=p)


class PhieuKham(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def __index__(self):
        mes=''
        medical_report = session.get('medical_report')
        use = request.form.get('use')
        patient_medicalist_id = request.args.get('patient_medicalist_id')
        patient_id = request.args.get('patient_id')
        if patient_medicalist_id:
            if request.method.__eq__('POST'):
                symptom = request.form.get('trieuchung')
                diseaseprediction = request.form.get('dudoanbenh')

                if patient_medicalist_id:
                    dao.create_medical_report(symptom=symptom,
                                              diseaseprediction=diseaseprediction,
                                              patient_medicalist_id=patient_medicalist_id)
                    dao.tao_lich_su_benh_nhan(medicalreport_id=dao.lay_id_phieukham_by_id_benhnhan_dskham(
                        patient_medicalist_id), patient_id=patient_id)

                    if medical_report:
                        medicalreport_id = dao.lay_id_phieukham_by_id_benhnhan_dskham(patient_medicalist_id)
                        dao.save_DetailMedicalReport(medical_report=medical_report,
                                                     medicalreport_id=medicalreport_id, patient_id=patient_id)
                        medicinecash = dao.tinh_tien(medicalreport_id)

                        dao.tao_hoa_don(medicalreport_id=medicalreport_id, patient_id=patient_id
                                        , medicinecash=medicinecash[0])
                        del session['medical_report']
                    else:
                        medicalreport_id = dao.lay_id_phieukham_by_id_benhnhan_dskham(patient_medicalist_id)
                        dao.tao_hoa_don(medicalreport_id=medicalreport_id, patient_id=patient_id)
        else:
            mes = 'Chưa chọn bệnh nhân'

        return self.render('admin/phieukham.html',mes = mes)

class HoSoBenhNhan(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def __index__(self):
        patient_id = request.args.get('patient_id')
        patient_medicalist_id = request.args.get('patient_medicalist_id')
        lichsu = dao.load_lich_su_benh_nhan(patient_id)
        return self.render('admin/hosobenhnhan.html', lichsu=lichsu)






class DanhSachHoaDon(AuthenticatedBaseView):
    @expose('/', methods=['get', 'post'])
    def __index__(self):
        p = dao.load_danh_sach_hoa_don()

        return self.render('admin/danhsachhoadon.html', p=p)



class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        medical_report = session.get('medical_report')
        if medical_report:
            del session['medical_report']
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        stats = dao.baocaodoanhthu(from_date=from_date,to_date=to_date)

        return self.render('admin/index.html',stats=stats)


class ThongKe(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        stats = dao.thongke(from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))

        return self.render('admin/thongke.html',stats = stats)



admin = Admin(app=app, name='QUẢN TRỊ VIÊN', template_mode='bootstrap4',index_view=MyAdminView())

admin.add_view(AuthenticatedModelView(Category, db.session, name=" Danh Sach Loai thuoc"))
admin.add_view(AuthenticatedModelView(Unit, db.session, name="Đơn vị thuốc"))
admin.add_view(MedicineView(Medicine, db.session, name="Danh Sach Thuoc"))
admin.add_view(TaoDanhSachKham(name="Tạo danh sách khám"))
admin.add_view(XemDanhSachKham(name="Xem danh sách khám"))
admin.add_view(DanhSachThuoc(name="Danh sách thuốc"))
admin.add_view(DanhSachBenhNhan(name="Danh sách bệnh nhân"))
admin.add_view(PhieuKham(name="Phiếu khám"))
admin.add_view(HoSoBenhNhan(name="Hồ sơ"))
admin.add_view(DanhSachHoaDon(name='Danh sách hóa đơn'))
admin.add_view(ThongKe(name='Thống kê sử dụng thuốc'))
admin.add_view(LogoutView(name='Đăng xuất'))
