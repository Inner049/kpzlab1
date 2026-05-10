# src/before_refactoring/expense_service_bad.py
class OldExpenseService:
    def add(self, a, c_id, d, d_date): # Погані назви параметрів
        if a > 1000000: # Magic Number + вбудована валідація
            return False
        
        if len(d) < 3: 
            return False
            
        print(f"saved amount {a}") # Використання f-рядків у логах/прінтах
        return True
