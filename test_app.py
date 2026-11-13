import sys
import unittest
sys.stdout.reconfigure(encoding='utf-8')
from app import app
from data_manager import db

class ZoneSportCenterTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        # Reset to clean demo seed data for tests
        db.reset_to_seed()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_01_login_and_logout(self):
        print("Testing Login & Logout...")
        # Bad login
        res = self.login("admin", "wrongpass")
        self.assertIn("Invalid username or password".encode('utf-8'), res.data)

        # Successful Admin login
        res = self.login("admin", "admin123")
        self.assertEqual(res.status_code, 200)
        self.assertIn("ZONE SPORT CENTER".encode('utf-8'), res.data)
        self.assertIn("ADMIN".encode('utf-8'), res.data)

        # Logout
        res = self.logout()
        self.assertIn("signed out successfully".encode('utf-8'), res.data)

        # Successful Coach login
        res = self.login("coach_nam", "coach123")
        self.assertEqual(res.status_code, 200)
        self.assertIn("COACH".encode('utf-8'), res.data)
        print("-> Login & Logout: PASSED")

    def test_02_dashboard(self):
        print("Testing Dashboard...")
        self.login("admin", "admin123")
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn("TOTAL STUDENTS".encode('utf-8'), res.data)
        self.assertIn("TOTAL COACHES".encode('utf-8'), res.data)
        self.assertIn("TRAINING CLASSES".encode('utf-8'), res.data)
        print("-> Dashboard: PASSED")

    def test_03_student_crud(self):
        print("Testing Student CRUD...")
        self.login("admin", "admin123")

        # 1. List students
        res = self.client.get('/students')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Nguyễn Văn An".encode('utf-8'), res.data)

        # 2. Add student
        res = self.client.post('/students/new', data={
            'name': 'John Doe Student',
            'dob': '2011-04-10',
            'gender': 'Male',
            'phone': '0919998888',
            'address': 'High Tech Park, Thu Duc',
            'note': 'Potential point guard 1m80'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("John Doe Student".encode('utf-8'), res.data)

        # 3. Search student
        res = self.client.get('/students?q=0919998888')
        self.assertIn("John Doe Student".encode('utf-8'), res.data)

        # 4. Edit student
        st = next(s for s in db.get_all_students() if s['name'] == 'John Doe Student')
        res = self.client.post(f'/students/{st["id"]}/edit', data={
            'name': 'John Doe Updated',
            'dob': '2011-04-10',
            'gender': 'Male',
            'phone': '0919998888',
            'address': 'Updated Street Address',
            'status': 'Active',
            'note': 'Promoted to junior team'
        }, follow_redirects=True)
        self.assertIn("John Doe Updated".encode('utf-8'), res.data)

        # 5. Detail
        res = self.client.get(f'/students/{st["id"]}')
        self.assertEqual(res.status_code, 200)
        self.assertIn("STUDENT PROFILE".encode('utf-8'), res.data)

        # 6. Delete
        res = self.client.post(f'/students/{st["id"]}/delete', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("John Doe Updated".encode('utf-8'), res.data)
        print("-> Student CRUD: PASSED")

    def test_04_coach_crud(self):
        print("Testing Coach CRUD...")
        self.login("admin", "admin123")

        # 1. Add Coach
        res = self.client.post('/coaches/new', data={
            'name': 'Coach Alex Turner',
            'phone': '0938123456',
            'email': 'alex.turner@zonesport.vn',
            'experience': '7 years',
            'specialty': '3-Point Shooting & Perimeter Defense',
            'bio': 'FIBA Level 2 Certified Coach',
            'username': 'coach_alex',
            'password': 'coach123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Coach Alex Turner".encode('utf-8'), res.data)

        # 2. Detail
        coach = next(c for c in db.get_all_coaches() if c['name'] == 'Coach Alex Turner')
        res = self.client.get(f'/coaches/{coach["id"]}')
        self.assertEqual(res.status_code, 200)
        self.assertIn("3-Point Shooting", res.get_data(as_text=True))

        # 3. Coach login check with created account
        self.logout()
        res = self.login('coach_alex', 'coach123')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Coach Alex Turner", res.get_data(as_text=True))
        print("-> Coach CRUD: PASSED")

    def test_05_class_and_enrollment(self):
        print("Testing Class and Enrollment...")
        self.login("admin", "admin123")

        # 1. Add Class with max 2 students
        res = self.client.post('/classes/new', data={
            'name': 'Small Group Test Camp',
            'level': 'Intermediate',
            'coach_id': 'HLV001',
            'max_students': '2',
            'tuition_fee': '1500000',
            'status': 'Đang mở đăng ký',
            'schedule': 'Sat - Sun (15:00 - 16:30)',
            'location': 'Zone VIP Court',
            'description': 'Small camp with 2 trainees'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        cl = next(c for c in db.get_all_classes() if c['name'] == 'Small Group Test Camp')

        # 2. Enroll student 1
        res = self.client.post('/enrollments/register', data={
            'student_id': 'HV001',
            'class_id': cl['id'],
            'enroll_date': '2026-10-30',
            'auto_payment': 'yes'
        }, follow_redirects=True)
        self.assertIn("enrolled".encode('utf-8'), res.data)

        # 3. Duplicate enroll check
        res = self.client.post('/enrollments/register', data={
            'student_id': 'HV001',
            'class_id': cl['id'],
            'enroll_date': '2026-10-30'
        }, follow_redirects=True)
        self.assertIn("already enrolled".encode('utf-8'), res.data)

        # 4. Enroll student 2
        res = self.client.post('/enrollments/register', data={
            'student_id': 'HV002',
            'class_id': cl['id'],
            'enroll_date': '2026-10-30'
        }, follow_redirects=True)
        self.assertIn("enrolled".encode('utf-8'), res.data)

        # 5. Over capacity check (max is 2)
        res = self.client.post('/enrollments/register', data={
            'student_id': 'HV003',
            'class_id': cl['id'],
            'enroll_date': '2026-10-30'
        }, follow_redirects=True)
        self.assertIn("maximum capacity".encode('utf-8'), res.data)
        print("-> Class & Enrollment: PASSED")

    def test_06_payments_and_reports(self):
        print("Testing Payments and Reports...")
        self.login("admin", "admin123")

        # 1. View payments list
        res = self.client.get('/payments')
        self.assertEqual(res.status_code, 200)
        self.assertIn("TUITION & REVENUE MANAGEMENT".encode('utf-8'), res.data)

        # 2. Record new payment
        res = self.client.post('/payments/record', data={
            'student_id': 'HV002',
            'class_id': 'LH001',
            'amount': '1500000',
            'paid_amount': '1500000',
            'status': 'Đã thanh toán',
            'payment_date': '2026-10-30',
            'payment_method': 'Chuyển khoản QR',
            'note': 'Test payment deposit'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # 3. View Reports
        res = self.client.get('/reports')
        self.assertEqual(res.status_code, 200)
        self.assertIn("REPORTS & ANALYTICS".encode('utf-8'), res.data)
        self.assertIn("MONTHLY REVENUE TREND".encode('utf-8'), res.data)
        print("-> Payments & Reports: PASSED")

    def test_07_attendance(self):
        print("Testing Attendance...")
        self.login("coach_nam", "coach123")

        # Coach accesses attendance
        res = self.client.get('/attendance')
        self.assertEqual(res.status_code, 200)
        self.assertIn("ATTENDANCE".encode('utf-8'), res.data)

        # Post attendance
        res = self.client.post('/attendance', data={
            'class_id': 'LH001',
            'date': '2026-10-30',
            'status_HV001': 'Present',
            'status_HV003': 'Present',
            'status_HV005': 'Excused'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("saved successfully".encode('utf-8'), res.data)
        print("-> Attendance: PASSED")

if __name__ == '__main__':
    unittest.main()