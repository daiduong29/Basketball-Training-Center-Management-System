import os
import json
from datetime import datetime, date
import copy

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'database.json')

def get_initial_seed_data():
    today_str = datetime.now().strftime("%Y-%m-%d")
    return {
        "users": [
            {
                "id": "U001",
                "username": "admin",
                "password": "admin123",
                "role": "admin",
                "full_name": "Quản Trị Viên Zone",
                "email": "admin@zonesport.vn",
                "phone": "0909123456",
                "coach_id": None,
                "avatar": "/static/images/default-avatar.png",
                "bio": "Quản trị viên toàn hệ thống Zone Sport Center"
            },
            {
                "id": "U002",
                "username": "coach_nam",
                "password": "coach123",
                "role": "coach",
                "full_name": "Nguyễn Thành Nam",
                "email": "nam.nguyen@zonesport.vn",
                "phone": "0912345678",
                "coach_id": "HLV001",
                "avatar": "/static/images/default-avatar.png",
                "bio": "Cựu VĐV bóng rổ quốc gia, 8 năm kinh nghiệm huấn luyện đào tạo trẻ"
            },
            {
                "id": "U003",
                "username": "coach_hoang",
                "password": "coach123",
                "role": "coach",
                "full_name": "Trần Minh Hoàng",
                "email": "hoang.tran@zonesport.vn",
                "phone": "0987654321",
                "coach_id": "HLV002",
                "avatar": "/static/images/default-avatar.png",
                "bio": "Chuyên gia đào tạo kỹ thuật ném bóng và tư duy chiến thuật thi đấu"
            },
            {
                "id": "U004",
                "username": "coach_duy",
                "password": "coach123",
                "role": "coach",
                "full_name": "Lê Quốc Duy",
                "email": "duy.le@zonesport.vn",
                "phone": "0933889900",
                "coach_id": "HLV003",
                "avatar": "/static/images/default-avatar.png",
                "bio": "Huấn luyện viên thể lực và kỹ năng phòng ngự nâng cao"
            }
        ],
        "coaches": [
            {
                "id": "HLV001",
                "name": "Nguyễn Thành Nam",
                "phone": "0912345678",
                "email": "nam.nguyen@zonesport.vn",
                "experience": "8 năm",
                "specialty": "Kỹ thuật cơ bản & Đào tạo trẻ U12-U15",
                "bio": "Cựu tuyển thủ trẻ, tốt nghiệp ĐH TDTT TP.HCM chuyên ngành Bóng rổ.",
                "status": "Đang hoạt động"
            },
            {
                "id": "HLV002",
                "name": "Trần Minh Hoàng",
                "phone": "0987654321",
                "email": "hoang.tran@zonesport.vn",
                "experience": "6 năm",
                "specialty": "Kỹ thuật ném 3 điểm & Thể lực thi đấu",
                "bio": "HLV đạt chứng chỉ FIBA Level 1, kinh nghiệm dẫn dắt nhiều đội học sinh vô địch giải trẻ.",
                "status": "Đang hoạt động"
            },
            {
                "id": "HLV003",
                "name": "Lê Quốc Duy",
                "phone": "0933889900",
                "email": "duy.le@zonesport.vn",
                "experience": "5 năm",
                "specialty": "Chiến thuật phối hợp & Phòng ngự phản công",
                "bio": "Trợ lý HLV tại giải bóng rổ bán chuyên VBA Development League.",
                "status": "Đang hoạt động"
            }
        ],
        "students": [
            {
                "id": "HV001",
                "name": "Nguyễn Văn An",
                "dob": "2012-05-14",
                "gender": "Nam",
                "phone": "0901112233",
                "address": "Số 12 Võ Văn Ngân, TP. Thủ Đức, TP.HCM",
                "created_date": "2026-09-01",
                "status": "Đang học",
                "note": "Tiềm năng ném bóng tốt, đam mê vị trí Hậu vệ"
            },
            {
                "id": "HV002",
                "name": "Lê Hoàng Bảo",
                "dob": "2011-08-20",
                "gender": "Nam",
                "phone": "0902223344",
                "address": "45 Lê Văn Việt, Tăng Nhơn Phú B, TP. Thủ Đức",
                "created_date": "2026-09-05",
                "status": "Đang học",
                "note": "Chiều cao tốt 1m75, phù hợp vị trí Tiền phong"
            },
            {
                "id": "HV003",
                "name": "Phạm Mai Chi",
                "dob": "2013-11-03",
                "gender": "Nữ",
                "phone": "0903334455",
                "address": "120 Đặng Văn Bi, Bình Thọ, TP. Thủ Đức",
                "created_date": "2026-09-10",
                "status": "Đang học",
                "note": "Kỹ năng dẫn bóng khéo léo, tập luyện chăm chỉ"
            },
            {
                "id": "HV004",
                "name": "Vũ Đăng Khoa",
                "dob": "2010-02-18",
                "gender": "Nam",
                "phone": "0904445566",
                "address": "88 Hoàng Diệu 2, Linh Chiểu, TP. Thủ Đức",
                "created_date": "2026-09-12",
                "status": "Đang học",
                "note": "Đang chuẩn bị thi đấu giải học sinh Quận"
            },
            {
                "id": "HV005",
                "name": "Trịnh Gia Huy",
                "dob": "2014-04-25",
                "gender": "Nam",
                "phone": "0905556677",
                "address": "25 Tô Ngọc Vân, Tam Phú, TP. Thủ Đức",
                "created_date": "2026-09-15",
                "status": "Đang học",
                "note": "Mới bắt đầu làm quen bóng rổ, rất năng nổ"
            },
            {
                "id": "HV006",
                "name": "Đỗ Ngọc Ánh",
                "dob": "2012-09-12",
                "gender": "Nữ",
                "phone": "0906667788",
                "address": "77 Kha Vạn Cân, Hiệp Bình Chánh, TP. Thủ Đức",
                "created_date": "2026-09-18",
                "status": "Đang học",
                "note": "Tập ném cự ly trung bình và thể lực"
            },
            {
                "id": "HV007",
                "name": "Huỳnh Tấn Phát",
                "dob": "2009-12-30",
                "gender": "Nam",
                "phone": "0907778899",
                "address": "15 Quang Trung, Hiệp Phú, TP. Thủ Đức",
                "created_date": "2026-09-22",
                "status": "Đang học",
                "note": "Nhóm Nâng cao, thể lực và tốc độ xuất sắc"
            },
            {
                "id": "HV008",
                "name": "Ngô Quốc Thịnh",
                "dob": "2011-06-19",
                "gender": "Nam",
                "phone": "0908889911",
                "address": "33 Trần Hưng Đạo, P. Dĩ An, Bình Dương",
                "created_date": "2026-10-01",
                "status": "Đang học",
                "note": "Học lớp Trung cấp buổi tối"
            },
            {
                "id": "HV009",
                "name": "Bùi Thảo My",
                "dob": "2013-03-08",
                "gender": "Nữ",
                "phone": "0909990022",
                "address": "62 Tây Hòa, Phước Long A, TP. Thủ Đức",
                "created_date": "2026-10-05",
                "status": "Đang học",
                "note": "Thích bóng rổ nghệ thuật và ném phạt"
            },
            {
                "id": "HV010",
                "name": "Lý Gia Bảo",
                "dob": "2010-07-27",
                "gender": "Nam",
                "phone": "0911223344",
                "address": "104 Nguyễn Duy Trinh, Bình Trưng Tây, TP. Thủ Đức",
                "created_date": "2026-10-10",
                "status": "Đang học",
                "note": "Học sinh lớp Nâng cao thi đấu"
            }
        ],
        "classes": [
            {
                "id": "LH001",
                "name": "Bóng Rổ Cơ Bản U12 (Zone Rookies A)",
                "level": "Beginner",
                "coach_id": "HLV001",
                "max_students": 15,
                "tuition_fee": 1500000,
                "status": "Đang học",
                "schedule": "Thứ 2 - Thứ 4 (17:30 - 19:00)",
                "location": "Sân Zone Arena 1",
                "description": "Lớp học dành cho học viên mới bắt đầu làm quen bóng rổ, rèn luyện kỹ năng nhồi bóng, chuyền bóng và ném rổ cơ bản."
            },
            {
                "id": "LH002",
                "name": "Bóng Rổ Cơ Bản U15 (Zone Rookies B)",
                "level": "Beginner",
                "coach_id": "HLV001",
                "max_students": 15,
                "tuition_fee": 1600000,
                "status": "Đang học",
                "schedule": "Thứ 3 - Thứ 5 (18:00 - 19:30)",
                "location": "Sân Zone Arena 2",
                "description": "Phát triển nền tảng kỹ năng cá nhân, bộ chân (footwork) và luật thi đấu cơ bản cho lứa tuổi U15."
            },
            {
                "id": "LH003",
                "name": "Bóng Rổ Trung Cấp (Zone All-Stars)",
                "level": "Intermediate",
                "coach_id": "HLV002",
                "max_students": 12,
                "tuition_fee": 1800000,
                "status": "Đang học",
                "schedule": "Thứ 2 - Thứ 6 (19:30 - 21:00)",
                "location": "Sân Zone Arena 1",
                "description": "Nâng cao cảm giác bóng, kỹ năng ném cự ly trung bình và 3 điểm, rèn luyện kỹ năng phòng thủ 1-1."
            },
            {
                "id": "LH004",
                "name": "Bóng Rổ Nâng Cao & Chiến Thuật (Zone Elite)",
                "level": "Advanced",
                "coach_id": "HLV003",
                "max_students": 10,
                "tuition_fee": 2200000,
                "status": "Đang học",
                "schedule": "Thứ 4 - Thứ 7 (19:30 - 21:00)",
                "location": "Sân Zone Arena VIP",
                "description": "Đào tạo chuyên sâu chiến thuật đội hình (Pick & Roll, Fast Break, Zone Defense), cọ xát thi đấu thực tế."
            },
            {
                "id": "LH005",
                "name": "Lớp Kỹ Năng Cuối Tuần (Weekend Skills)",
                "level": "Beginner",
                "coach_id": "HLV002",
                "max_students": 16,
                "tuition_fee": 1400000,
                "status": "Đang mở đăng ký",
                "schedule": "Thứ 7 - Chủ Nhật (08:00 - 09:30)",
                "location": "Sân Zone Arena 2",
                "description": "Lớp học cuối tuần bổ ích giúp các bạn trẻ xả stress, tăng cường chiều cao và kết nối bạn bè."
            }
        ],
        "enrollments": [
            {
                "id": "DK001",
                "student_id": "HV001",
                "class_id": "LH001",
                "enroll_date": "2026-09-02",
                "status": "Đang học"
            },
            {
                "id": "DK002",
                "student_id": "HV002",
                "class_id": "LH002",
                "enroll_date": "2026-09-06",
                "status": "Đang học"
            },
            {
                "id": "DK003",
                "student_id": "HV003",
                "class_id": "LH001",
                "enroll_date": "2026-09-11",
                "status": "Đang học"
            },
            {
                "id": "DK004",
                "student_id": "HV004",
                "class_id": "LH003",
                "enroll_date": "2026-09-14",
                "status": "Đang học"
            },
            {
                "id": "DK005",
                "student_id": "HV005",
                "class_id": "LH001",
                "enroll_date": "2026-09-16",
                "status": "Đang học"
            },
            {
                "id": "DK006",
                "student_id": "HV006",
                "class_id": "LH002",
                "enroll_date": "2026-09-20",
                "status": "Đang học"
            },
            {
                "id": "DK007",
                "student_id": "HV007",
                "class_id": "LH004",
                "enroll_date": "2026-09-23",
                "status": "Đang học"
            },
            {
                "id": "DK008",
                "student_id": "HV008",
                "class_id": "LH003",
                "enroll_date": "2026-10-02",
                "status": "Đang học"
            },
            {
                "id": "DK009",
                "student_id": "HV009",
                "class_id": "LH005",
                "enroll_date": "2026-10-06",
                "status": "Đang học"
            },
            {
                "id": "DK010",
                "student_id": "HV010",
                "class_id": "LH004",
                "enroll_date": "2026-10-11",
                "status": "Đang học"
            },
            {
                "id": "DK011",
                "student_id": "HV001",
                "class_id": "LH005",
                "enroll_date": "2026-10-15",
                "status": "Đang học"
            }
        ],
        "payments": [
            {
                "id": "HP001",
                "student_id": "HV001",
                "class_id": "LH001",
                "amount": 1500000,
                "paid_amount": 1500000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-02",
                "payment_method": "Chuyển khoản QR",
                "note": "Đã đóng đủ học phí tháng 9-10"
            },
            {
                "id": "HP002",
                "student_id": "HV002",
                "class_id": "LH002",
                "amount": 1600000,
                "paid_amount": 1600000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-06",
                "payment_method": "Tiền mặt",
                "note": "Thanh toán tại quầy lễ tân"
            },
            {
                "id": "HP003",
                "student_id": "HV003",
                "class_id": "LH001",
                "amount": 1500000,
                "paid_amount": 1500000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-11",
                "payment_method": "Chuyển khoản QR",
                "note": "Phụ huynh chuyển khoản ngân hàng"
            },
            {
                "id": "HP004",
                "student_id": "HV004",
                "class_id": "LH003",
                "amount": 1800000,
                "paid_amount": 1800000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-14",
                "payment_method": "Thẻ tín dụng",
                "note": "Cà thẻ POS"
            },
            {
                "id": "HP005",
                "student_id": "HV005",
                "class_id": "LH001",
                "amount": 1500000,
                "paid_amount": 0,
                "status": "Chưa thanh toán",
                "payment_date": None,
                "payment_method": None,
                "note": "Hẹn nộp vào buổi học kế tiếp"
            },
            {
                "id": "HP006",
                "student_id": "HV006",
                "class_id": "LH002",
                "amount": 1600000,
                "paid_amount": 1600000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-20",
                "payment_method": "Chuyển khoản QR",
                "note": "Đã hoàn thành học phí"
            },
            {
                "id": "HP007",
                "student_id": "HV007",
                "class_id": "LH004",
                "amount": 2200000,
                "paid_amount": 2200000,
                "status": "Đã thanh toán",
                "payment_date": "2026-09-23",
                "payment_method": "Chuyển khoản QR",
                "note": "Học phí khóa Elite"
            },
            {
                "id": "HP008",
                "student_id": "HV008",
                "class_id": "LH003",
                "amount": 1800000,
                "paid_amount": 1000000,
                "status": "Chưa thanh toán",
                "payment_date": "2026-10-02",
                "payment_method": "Tiền mặt",
                "note": "Đặt cọc 1,000,000đ, còn nợ 800,000đ"
            },
            {
                "id": "HP009",
                "student_id": "HV009",
                "class_id": "LH005",
                "amount": 1400000,
                "paid_amount": 1400000,
                "status": "Đã thanh toán",
                "payment_date": "2026-10-06",
                "payment_method": "Chuyển khoản QR",
                "note": "Thanh toán khóa cuối tuần"
            },
            {
                "id": "HP010",
                "student_id": "HV010",
                "class_id": "LH004",
                "amount": 2200000,
                "paid_amount": 0,
                "status": "Chưa thanh toán",
                "payment_date": None,
                "payment_method": None,
                "note": "Chờ xác nhận từ phụ huynh"
            },
            {
                "id": "HP011",
                "student_id": "HV001",
                "class_id": "LH005",
                "amount": 1400000,
                "paid_amount": 1400000,
                "status": "Đã thanh toán",
                "payment_date": "2026-10-15",
                "payment_method": "Chuyển khoản QR",
                "note": "Học viên đăng ký thêm lớp thứ 2"
            }
        ],
        "attendances": [
            {"id": "AT001", "class_id": "LH001", "student_id": "HV001", "date": "2026-10-20", "status": "Có mặt"},
            {"id": "AT002", "class_id": "LH001", "student_id": "HV003", "date": "2026-10-20", "status": "Có mặt"},
            {"id": "AT003", "class_id": "LH001", "student_id": "HV005", "date": "2026-10-20", "status": "Vắng có phép"},
            {"id": "AT004", "class_id": "LH001", "student_id": "HV001", "date": "2026-10-22", "status": "Có mặt"},
            {"id": "AT005", "class_id": "LH001", "student_id": "HV003", "date": "2026-10-22", "status": "Có mặt"},
            {"id": "AT006", "class_id": "LH001", "student_id": "HV005", "date": "2026-10-22", "status": "Có mặt"},
            {"id": "AT007", "class_id": "LH002", "student_id": "HV002", "date": "2026-10-21", "status": "Có mặt"},
            {"id": "AT008", "class_id": "LH002", "student_id": "HV006", "date": "2026-10-21", "status": "Có mặt"},
            {"id": "AT009", "class_id": "LH003", "student_id": "HV004", "date": "2026-10-21", "status": "Có mặt"},
            {"id": "AT010", "class_id": "LH003", "student_id": "HV008", "date": "2026-10-21", "status": "Có mặt"},
            {"id": "AT011", "class_id": "LH004", "student_id": "HV007", "date": "2026-10-22", "status": "Có mặt"},
            {"id": "AT012", "class_id": "LH004", "student_id": "HV010", "date": "2026-10-22", "status": "Có mặt"}
        ]
    }

class DataManager:
    def __init__(self):
        self._load_data()

    def _load_data(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(DATA_FILE):
            self.data = get_initial_seed_data()
            self._save_data()
        else:
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = get_initial_seed_data()
                self._save_data()

    def _save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def reset_to_seed(self):
        self.data = get_initial_seed_data()
        self._save_data()

    # --- USER & AUTH ---
    def get_user_by_username(self, username):
        for u in self.data.get("users", []):
            if u["username"].lower() == username.lower():
                return u
        return None

    def get_user_by_id(self, user_id):
        for u in self.data.get("users", []):
            if u["id"] == user_id:
                return u
        return None

    def update_user_profile(self, user_id, full_name, email, phone, bio=None):
        for u in self.data.get("users", []):
            if u["id"] == user_id:
                u["full_name"] = full_name
                u["email"] = email
                u["phone"] = phone
                if bio is not None:
                    u["bio"] = bio
                # If this user is also a coach, sync coach info
                if u.get("coach_id"):
                    coach = self.get_coach_by_id(u["coach_id"])
                    if coach:
                        coach["name"] = full_name
                        coach["email"] = email
                        coach["phone"] = phone
                        if bio:
                            coach["bio"] = bio
                self._save_data()
                return True
        return False

    def change_user_password(self, user_id, old_pwd, new_pwd):
        for u in self.data.get("users", []):
            if u["id"] == user_id:
                if u["password"] == old_pwd:
                    u["password"] = new_pwd
                    self._save_data()
                    return True, "Password changed successfully!"
                else:
                    return False, "Current password is incorrect!"
        return False, "User does not exist!"

    # --- RAW HELPERS TO PREVENT RECURSION ---
    def _get_raw_student(self, student_id):
        for s in self.data.get("students", []):
            if s["id"] == student_id:
                return copy.deepcopy(s)
        return None

    def _get_raw_class(self, class_id):
        for c in self.data.get("classes", []):
            if c["id"] == class_id:
                return copy.deepcopy(c)
        return None

    def _get_raw_coach(self, coach_id):
        for c in self.data.get("coaches", []):
            if c["id"] == coach_id:
                return copy.deepcopy(c)
        return None

    # --- STUDENTS ---
    def calculate_age(self, dob_str):
        if not dob_str:
            return None
        try:
            born = datetime.strptime(dob_str, "%Y-%m-%d").date()
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        except Exception:
            return None

    def get_all_students(self, query=None):
        students = copy.deepcopy(self.data.get("students", []))
        for s in students:
            s["age"] = self.calculate_age(s.get("dob"))
            # Count enrolled classes
            enrolled = [e for e in self.data.get("enrollments", []) if e["student_id"] == s["id"] and e.get("status") != "Đã hủy"]
            s["enrolled_count"] = len(enrolled)

        if query:
            q = query.strip().lower()
            students = [
                s for s in students
                if q in s["name"].lower() or q in s["phone"].lower() or q in s["id"].lower()
            ]
        return sorted(students, key=lambda x: x["id"], reverse=True)

    def get_student_by_id(self, student_id):
        for s in self.data.get("students", []):
            if s["id"] == student_id:
                res = copy.deepcopy(s)
                res["age"] = self.calculate_age(res.get("dob"))
                # Get enrolled classes info
                enrolls = [e for e in self.data.get("enrollments", []) if e["student_id"] == student_id]
                classes_info = []
                for e in enrolls:
                    c = self._get_raw_class(e["class_id"])
                    if c:
                        c["enroll_date"] = e["enroll_date"]
                        c["enrollment_status"] = e.get("status", "Đang học")
                        c["enrollment_id"] = e["id"]
                        classes_info.append(c)
                res["classes"] = classes_info

                # Get payments
                payments = [p for p in self.data.get("payments", []) if p["student_id"] == student_id]
                for p in payments:
                    c = self._get_raw_class(p["class_id"])
                    p["class_name"] = c["name"] if c else "Không rõ lớp"
                res["payments"] = sorted(payments, key=lambda x: x.get("payment_date") or "1970-01-01", reverse=True)
                return res
        return None

    def generate_student_id(self):
        max_num = 0
        for s in self.data.get("students", []):
            try:
                num = int(s["id"].replace("HV", ""))
                if num > max_num:
                    max_num = num
            except Exception:
                pass
        return f"HV{max_num + 1:03d}"

    def add_student(self, name, dob, gender, phone, address, note=""):
        student_id = self.generate_student_id()
        created_date = datetime.now().strftime("%Y-%m-%d")
        new_student = {
            "id": student_id,
            "name": name.strip(),
            "dob": dob,
            "gender": gender,
            "phone": phone.strip(),
            "address": address.strip(),
            "created_date": created_date,
            "status": "Đang học",
            "note": note.strip()
        }
        self.data["students"].append(new_student)
        self._save_data()
        return new_student

    def update_student(self, student_id, name, dob, gender, phone, address, status, note=""):
        for s in self.data.get("students", []):
            if s["id"] == student_id:
                s["name"] = name.strip()
                s["dob"] = dob
                s["gender"] = gender
                s["phone"] = phone.strip()
                s["address"] = address.strip()
                s["status"] = status
                s["note"] = note.strip()
                self._save_data()
                return True
        return False

    def delete_student(self, student_id):
        self.data["students"] = [s for s in self.data.get("students", []) if s["id"] != student_id]
        # Also clean up or flag enrollments and payments
        self.data["enrollments"] = [e for e in self.data.get("enrollments", []) if e["student_id"] != student_id]
        self.data["payments"] = [p for p in self.data.get("payments", []) if p["student_id"] != student_id]
        self.data["attendances"] = [a for a in self.data.get("attendances", []) if a["student_id"] != student_id]
        self._save_data()
        return True

    # --- COACHES ---
    def get_all_coaches(self, query=None):
        coaches = copy.deepcopy(self.data.get("coaches", []))
        for c in coaches:
            # Find classes taught
            classes = [cl for cl in self.data.get("classes", []) if cl["coach_id"] == c["id"]]
            c["classes_count"] = len(classes)
            c["classes"] = classes

        if query:
            q = query.strip().lower()
            coaches = [
                c for c in coaches
                if q in c["name"].lower() or q in c["phone"].lower() or q in c["email"].lower() or q in c["id"].lower()
            ]
        return coaches

    def get_coach_by_id(self, coach_id):
        for c in self.data.get("coaches", []):
            if c["id"] == coach_id:
                res = copy.deepcopy(c)
                # Find classes taught
                classes = [cl for cl in self.data.get("classes", []) if cl["coach_id"] == coach_id]
                for cl in classes:
                    enrolled = [e for e in self.data.get("enrollments", []) if e["class_id"] == cl["id"] and e.get("status") != "Đã hủy"]
                    cl["current_students"] = len(enrolled)
                res["classes"] = classes
                return res
        return None

    def generate_coach_id(self):
        max_num = 0
        for c in self.data.get("coaches", []):
            try:
                num = int(c["id"].replace("HLV", ""))
                if num > max_num:
                    max_num = num
            except Exception:
                pass
        return f"HLV{max_num + 1:03d}"

    def add_coach(self, name, phone, email, experience="", specialty="", bio="", create_user_account=True, username=None, password=None):
        coach_id = self.generate_coach_id()
        new_coach = {
            "id": coach_id,
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "experience": experience.strip(),
            "specialty": specialty.strip(),
            "bio": bio.strip(),
            "status": "Đang hoạt động"
        }
        self.data["coaches"].append(new_coach)

        if create_user_account:
            u_name = username.strip() if username else f"coach_{coach_id.lower()}"
            pwd = password.strip() if password else "coach123"
            u_id = f"U{len(self.data.get('users', [])) + 1:03d}"
            new_user = {
                "id": u_id,
                "username": u_name,
                "password": pwd,
                "role": "coach",
                "full_name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "coach_id": coach_id,
                "avatar": "/static/images/default-avatar.png",
                "bio": bio.strip()
            }
            self.data["users"].append(new_user)

        self._save_data()
        return new_coach

    def update_coach(self, coach_id, name, phone, email, experience="", specialty="", bio="", status="Đang hoạt động"):
        for c in self.data.get("coaches", []):
            if c["id"] == coach_id:
                c["name"] = name.strip()
                c["phone"] = phone.strip()
                c["email"] = email.strip()
                c["experience"] = experience.strip()
                c["specialty"] = specialty.strip()
                c["bio"] = bio.strip()
                c["status"] = status

                # Sync user account if present
                for u in self.data.get("users", []):
                    if u.get("coach_id") == coach_id:
                        u["full_name"] = name.strip()
                        u["email"] = email.strip()
                        u["phone"] = phone.strip()
                        u["bio"] = bio.strip()

                self._save_data()
                return True
        return False

    def delete_coach(self, coach_id):
        self.data["coaches"] = [c for c in self.data.get("coaches", []) if c["id"] != coach_id]
        # Unassign coach from classes
        for cl in self.data.get("classes", []):
            if cl.get("coach_id") == coach_id:
                cl["coach_id"] = None
        # Remove user account linked to this coach
        self.data["users"] = [u for u in self.data.get("users", []) if u.get("coach_id") != coach_id]
        self._save_data()
        return True

    # --- CLASSES ---
    def get_all_classes(self, level=None, status=None, coach_id=None, query=None):
        classes = copy.deepcopy(self.data.get("classes", []))
        for cl in classes:
            coach = self.get_coach_by_id(cl.get("coach_id"))
            cl["coach_name"] = coach["name"] if coach else "Chưa phân công"
            enrolled = [e for e in self.data.get("enrollments", []) if e["class_id"] == cl["id"] and e.get("status") != "Đã hủy"]
            cl["current_students"] = len(enrolled)
            cl["available_slots"] = max(0, cl.get("max_students", 0) - cl["current_students"])
            cl["fill_percentage"] = round((cl["current_students"] / cl.get("max_students", 1)) * 100) if cl.get("max_students") else 0

        if level:
            classes = [c for c in classes if c.get("level") == level]
        if status:
            classes = [c for c in classes if c.get("status") == status]
        if coach_id:
            classes = [c for c in classes if c.get("coach_id") == coach_id]
        if query:
            q = query.strip().lower()
            classes = [c for c in classes if q in c["name"].lower() or q in c["id"].lower() or q in c["coach_name"].lower()]

        return classes

    def get_class_by_id(self, class_id):
        for cl in self.data.get("classes", []):
            if cl["id"] == class_id:
                res = copy.deepcopy(cl)
                coach = self._get_raw_coach(res.get("coach_id"))
                res["coach"] = coach
                res["coach_name"] = coach["name"] if coach else "Chưa phân công"

                # Get students enrolled
                enrolls = [e for e in self.data.get("enrollments", []) if e["class_id"] == class_id and e.get("status") != "Đã hủy"]
                students_in_class = []
                for e in enrolls:
                    s = self._get_raw_student(e["student_id"])
                    if s:
                        s_info = {
                            "id": s["id"],
                            "name": s["name"],
                            "phone": s["phone"],
                            "dob": s.get("dob"),
                            "age": self.calculate_age(s.get("dob")),
                            "gender": s.get("gender"),
                            "enroll_date": e["enroll_date"],
                            "enrollment_id": e["id"]
                        }
                        # Payment status in this class
                        pay = next((p for p in self.data.get("payments", []) if p["student_id"] == s["id"] and p["class_id"] == class_id), None)
                        s_info["payment_status"] = pay["status"] if pay else "Chưa tạo học phí"
                        s_info["paid_amount"] = pay["paid_amount"] if pay else 0
                        students_in_class.append(s_info)

                res["students"] = students_in_class
                res["current_students"] = len(students_in_class)
                res["available_slots"] = max(0, res.get("max_students", 0) - res["current_students"])
                res["fill_percentage"] = round((res["current_students"] / res.get("max_students", 1)) * 100) if res.get("max_students") else 0
                return res
        return None

    def generate_class_id(self):
        max_num = 0
        for cl in self.data.get("classes", []):
            try:
                num = int(cl["id"].replace("LH", ""))
                if num > max_num:
                    max_num = num
            except Exception:
                pass
        return f"LH{max_num + 1:03d}"

    def add_class(self, name, level, coach_id, max_students, tuition_fee, status="Đang học", schedule="", location="", description=""):
        class_id = self.generate_class_id()
        new_class = {
            "id": class_id,
            "name": name.strip(),
            "level": level,
            "coach_id": coach_id if coach_id else None,
            "max_students": int(max_students),
            "tuition_fee": int(tuition_fee),
            "status": status,
            "schedule": schedule.strip(),
            "location": location.strip(),
            "description": description.strip()
        }
        self.data["classes"].append(new_class)
        self._save_data()
        return new_class

    def update_class(self, class_id, name, level, coach_id, max_students, tuition_fee, status, schedule="", location="", description=""):
        for cl in self.data.get("classes", []):
            if cl["id"] == class_id:
                cl["name"] = name.strip()
                cl["level"] = level
                cl["coach_id"] = coach_id if coach_id else None
                cl["max_students"] = int(max_students)
                cl["tuition_fee"] = int(tuition_fee)
                cl["status"] = status
                cl["schedule"] = schedule.strip()
                cl["location"] = location.strip()
                cl["description"] = description.strip()
                self._save_data()
                return True
        return False

    def delete_class(self, class_id):
        self.data["classes"] = [cl for cl in self.data.get("classes", []) if cl["id"] != class_id]
        self.data["enrollments"] = [e for e in self.data.get("enrollments", []) if e["class_id"] != class_id]
        self.data["payments"] = [p for p in self.data.get("payments", []) if p["class_id"] != class_id]
        self.data["attendances"] = [a for a in self.data.get("attendances", []) if a["class_id"] != class_id]
        self._save_data()
        return True

    # --- ENROLLMENTS ---
    def generate_enrollment_id(self):
        max_num = 0
        for e in self.data.get("enrollments", []):
            try:
                num = int(e["id"].replace("DK", ""))
                if num > max_num:
                    max_num = num
            except Exception:
                pass
        return f"DK{max_num + 1:03d}"

    def enroll_student(self, student_id, class_id, enroll_date=None, auto_create_payment=True):
        if not enroll_date:
            enroll_date = datetime.now().strftime("%Y-%m-%d")

        target_class = self.get_class_by_id(class_id)
        if not target_class:
            return False, "Class not found!"

        student = self.get_student_by_id(student_id)
        if not student:
            return False, "Student not found!"

        # Check duplicate
        for e in self.data.get("enrollments", []):
            if e["student_id"] == student_id and e["class_id"] == class_id and e.get("status") != "Đã hủy":
                return False, f"Student '{student['name']}' is already enrolled in class '{target_class['name']}'!"

        # Check capacity
        current_count = target_class["current_students"]
        if current_count >= target_class["max_students"]:
            return False, f"Class is already at maximum capacity ({target_class['max_students']} students)!"

        # Create enrollment
        enrollment_id = self.generate_enrollment_id()
        new_enrollment = {
            "id": enrollment_id,
            "student_id": student_id,
            "class_id": class_id,
            "enroll_date": enroll_date,
            "status": "Đang học"
        }
        self.data["enrollments"].append(new_enrollment)

        # Automatically create fee payment record if not exists
        if auto_create_payment:
            existing_pay = next((p for p in self.data.get("payments", []) if p["student_id"] == student_id and p["class_id"] == class_id), None)
            if not existing_pay:
                self.record_payment(
                    student_id=student_id,
                    class_id=class_id,
                    amount=target_class["tuition_fee"],
                    paid_amount=0,
                    status="Chưa thanh toán",
                    payment_date=None,
                    payment_method=None,
                    note="Generated automatically upon class enrollment"
                )

        self._save_data()
        return True, "Student enrolled in class successfully!"

    def cancel_enrollment(self, enrollment_id):
        for e in self.data.get("enrollments", []):
            if e["id"] == enrollment_id:
                e["status"] = "Đã hủy"
                self._save_data()
                return True, "Enrollment cancelled successfully!"
        return False, "Enrollment record not found!"

    def get_all_enrollments(self, class_id=None, student_id=None, status=None):
        enrolls = copy.deepcopy(self.data.get("enrollments", []))
        result = []
        for e in enrolls:
            s = self.get_student_by_id(e["student_id"])
            c = self.get_class_by_id(e["class_id"])
            e["student_name"] = s["name"] if s else "Học viên không tồn tại"
            e["student_phone"] = s["phone"] if s else ""
            e["class_name"] = c["name"] if c else "Lớp không tồn tại"
            e["class_level"] = c["level"] if c else ""
            e["tuition_fee"] = c["tuition_fee"] if c else 0

            # Payment
            pay = next((p for p in self.data.get("payments", []) if p["student_id"] == e["student_id"] and p["class_id"] == e["class_id"]), None)
            e["payment_status"] = pay["status"] if pay else "Chưa có"

            if class_id and e["class_id"] != class_id:
                continue
            if student_id and e["student_id"] != student_id:
                continue
            if status and e.get("status") != status:
                continue
            result.append(e)

        return sorted(result, key=lambda x: x["enroll_date"], reverse=True)

    # --- PAYMENTS ---
    def generate_payment_id(self):
        max_num = 0
        for p in self.data.get("payments", []):
            try:
                num = int(p["id"].replace("HP", ""))
                if num > max_num:
                    max_num = num
            except Exception:
                pass
        return f"HP{max_num + 1:03d}"

    def record_payment(self, student_id, class_id, amount, paid_amount, status, payment_date=None, payment_method="Tiền mặt", note=""):
        payment_id = self.generate_payment_id()
        if not payment_date and paid_amount > 0:
            payment_date = datetime.now().strftime("%Y-%m-%d")

        new_pay = {
            "id": payment_id,
            "student_id": student_id,
            "class_id": class_id,
            "amount": int(amount),
            "paid_amount": int(paid_amount),
            "status": status,
            "payment_date": payment_date,
            "payment_method": payment_method,
            "note": note.strip()
        }
        self.data["payments"].append(new_pay)
        self._save_data()
        return new_pay

    def update_payment(self, payment_id, paid_amount, status, payment_method, payment_date=None, note=""):
        for p in self.data.get("payments", []):
            if p["id"] == payment_id:
                p["paid_amount"] = int(paid_amount)
                p["status"] = status
                p["payment_method"] = payment_method
                if payment_date:
                    p["payment_date"] = payment_date
                elif not p.get("payment_date") and int(paid_amount) > 0:
                    p["payment_date"] = datetime.now().strftime("%Y-%m-%d")
                if note:
                    p["note"] = note.strip()
                self._save_data()
                return True
        return False

    def get_all_payments(self, status=None, query=None):
        payments = copy.deepcopy(self.data.get("payments", []))
        result = []
        for p in payments:
            s = self.get_student_by_id(p["student_id"])
            c = self.get_class_by_id(p["class_id"])
            p["student_name"] = s["name"] if s else "Không rõ"
            p["student_phone"] = s["phone"] if s else ""
            p["class_name"] = c["name"] if c else "Không rõ"
            p["remaining"] = max(0, p.get("amount", 0) - p.get("paid_amount", 0))

            if status and p.get("status") != status:
                continue
            if query:
                q = query.strip().lower()
                if q not in p["student_name"].lower() and q not in p["id"].lower() and q not in p["student_phone"].lower() and q not in p["class_name"].lower():
                    continue
            result.append(p)

        return sorted(result, key=lambda x: x.get("id"), reverse=True)

    # --- ATTENDANCE ---
    def record_attendance(self, class_id, attendance_list, date_str=None):
        """attendance_list is a list of dict: [{'student_id': 'HV001', 'status': 'Có mặt'}]"""
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        # Remove existing records for this class & date
        self.data["attendances"] = [
            a for a in self.data.get("attendances", [])
            if not (a["class_id"] == class_id and a["date"] == date_str)
        ]

        count = len(self.data["attendances"])
        for item in attendance_list:
            count += 1
            self.data["attendances"].append({
                "id": f"AT{count:03d}",
                "class_id": class_id,
                "student_id": item["student_id"],
                "date": date_str,
                "status": item["status"]
            })
        self._save_data()
        return True

    def get_class_attendance_rate(self, class_id=None):
        attendances = self.data.get("attendances", [])
        if class_id:
            attendances = [a for a in attendances if a["class_id"] == class_id]
        if not attendances:
            return 92.5 # baseline default demo rate if none yet
        present = sum(1 for a in attendances if a.get("status") in ["Có mặt", "Present"])
        return round((present / len(attendances)) * 100, 1)

    # --- DASHBOARD & REPORTS ---
    def get_dashboard_summary(self):
        students = self.data.get("students", [])
        coaches = self.data.get("coaches", [])
        classes = self.data.get("classes", [])
        enrollments = [e for e in self.data.get("enrollments", []) if e.get("status") != "Đã hủy"]
        payments = self.data.get("payments", [])

        total_collected = sum(p.get("paid_amount", 0) for p in payments)
        total_receivable = sum(p.get("amount", 0) for p in payments)
        total_debt = max(0, total_receivable - total_collected)

        # Class enrollment stats for chart
        class_stats = []
        for cl in classes:
            enr_count = sum(1 for e in enrollments if e["class_id"] == cl["id"])
            class_stats.append({
                "id": cl["id"],
                "name": cl["name"],
                "level": cl["level"],
                "count": enr_count,
                "max": cl.get("max_students", 15),
                "fill": round((enr_count / cl.get("max_students", 1)) * 100) if cl.get("max_students") else 0
            })

        active_classes = sum(1 for cl in classes if cl.get("status") == "Đang học" or cl.get("status") == "Đang mở đăng ký")

        return {
            "total_students": len(students),
            "total_coaches": len(coaches),
            "total_classes": len(classes),
            "active_classes": active_classes,
            "total_enrollments": len(enrollments),
            "total_collected": total_collected,
            "total_debt": total_debt,
            "attendance_rate": self.get_class_attendance_rate(),
            "class_stats": class_stats,
            "recent_students": sorted(students, key=lambda x: x["created_date"], reverse=True)[:5],
            "recent_payments": sorted(payments, key=lambda x: x.get("payment_date") or "", reverse=True)[:5]
        }

    def get_monthly_reports(self, target_year=2026):
        # Generate monthly statistics for reports
        months_data = []
        for m in range(1, 13):
            m_str = f"{target_year}-{m:02d}"
            # Enrollments in month
            enroll_in_m = sum(1 for e in self.data.get("enrollments", []) if e.get("enroll_date", "").startswith(m_str))
            # New students in month
            students_in_m = sum(1 for s in self.data.get("students", []) if s.get("created_date", "").startswith(m_str))
            # Revenue collected in month
            revenue_in_m = sum(p.get("paid_amount", 0) for p in self.data.get("payments", []) if (p.get("payment_date") or "").startswith(m_str))

            months_data.append({
                "month": f"Tháng {m}",
                "month_code": m_str,
                "enrollments": enroll_in_m,
                "new_students": students_in_m,
                "revenue": revenue_in_m
            })
        return months_data

db = DataManager()
