def validate_email(email: str) -> bool:
    """Єдиний рядок валідації — без дублювань (DRY)"""
    return '@' in email

def validate_password(password: str) -> bool:
    return len(password) >= 8

class UserRepository:
    """Відповідає ТІЛЬКИ за зберігання даних (SRP)"""
    def __init__(self, db_connection):
        # Залежність передається ззовні (DIP)
        self.conn = db_connection

    def save(self, email, password, name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users VALUES (?,?,?)", (email, password, name))
        self.conn.commit()

    def update(self, user_id, email, name):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET email=?, name=? WHERE id=?", (email, name, user_id))
        self.conn.commit()

    def delete(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def get_all(self) -> list:
        cursor = self.conn.cursor()
        return cursor.execute("SELECT * FROM users").fetchall()

class EmailService:
    """Відповідає ТІЛЬКИ за відправку email (SRP)"""
    def send_welcome(self, email, name):
        # Логіка відправки через smtplib
        print(f"Відправлено email на {email}: Welcome {name}!")

class ReportService:
    """Відповідає ТІЛЬКИ за звіти (SRP)"""
    def generate_new_user_report(self, email):
        with open('report.txt', 'w') as f:
            f.write(f'New user: {email}')
            
    def send_mass_report(self, users):
        print(f"Звіт згенеровано для {len(users)} користувачів")

class UserService:
    """Бізнес-логіка — координує інші сервіси"""
    def __init__(self, repo: UserRepository, email_svc: EmailService, report_svc: ReportService):
        # Усі залежності впроваджуються через конструктор (DIP)
        self.repo = repo
        self.email_svc = email_svc
        self.report_svc = report_svc

    def register(self, email, password, name):
        if not validate_email(email) or not validate_password(password):
            return False
        
        self.repo.save(email, password, name)
        self.email_svc.send_welcome(email, name)
        self.report_svc.generate_new_user_report(email)
        return True

    def update(self, user_id, email, name):
        if not validate_email(email):
            return False
            
        self.repo.update(user_id, email, name)
        return True