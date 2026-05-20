"""
Unit-тести для ExpenseValidator
Перевіряють валідацію даних витрат
"""
import pytest
from datetime import date, timedelta
from src.validators.expense_validator import ExpenseValidator
from src.exceptions import ValidationError


class TestExpenseValidator:
    """Клас для групування тестів ExpenseValidator"""

    # ═══════════════════════════════════════════════════════════
    # HAPPY PATH — коректні дані проходять валідацію
    # ═══════════════════════════════════════════════════════════

    @pytest.mark.unit
    def test_valid_expense_passes(self):
        """Коректні дані проходять валідацію без помилок"""
        # Arrange
        amount = 150.50
        category_id = 1
        description = "Кава в кафе"
        expense_date = date.today()

        # Act & Assert (не кидає виключення)
        ExpenseValidator.validate(amount, category_id, description, expense_date)

    @pytest.mark.unit
    def test_minimal_valid_amount(self):
        """Мінімальна допустима сума (0.01) проходить валідацію"""
        ExpenseValidator.validate(0.01, 1, "Тест", date.today())

    @pytest.mark.unit
    def test_all_categories_valid(self):
        """Всі 5 допустимих категорій проходять валідацію"""
        for category_id in [1, 2, 3, 4, 5]:
            ExpenseValidator.validate(100, category_id, "Тест", date.today())

    @pytest.mark.unit
    def test_description_gets_stripped(self):
        """Опис з пробілами на початку/кінці обробляється коректно"""
        # Валідатор має приймати опис з пробілами (вони обрізаються)
        ExpenseValidator.validate(100, 1, "   Опис з пробілами   ", date.today())

    @pytest.mark.unit
    def test_today_date_is_valid(self):
        """Сьогоднішня дата є допустимою"""
        ExpenseValidator.validate(100, 1, "Сьогодні", date.today())

    @pytest.mark.unit
    def test_past_date_is_valid(self):
        """Дата в минулому є допустимою"""
        past_date = date.today() - timedelta(days=10)
        ExpenseValidator.validate(100, 1, "Минуле", past_date)

    # ═══════════════════════════════════════════════════════════
    # ERROR CASES — некоректні дані кидають ValidationError
    # ═══════════════════════════════════════════════════════════

    @pytest.mark.unit
    def test_zero_amount_raises_error(self):
        """Сума 0 кидає ValidationError з полем 'amount'"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(0, 1, "Тест", date.today())
        assert exc_info.value.field == "amount"
        assert "більшою за нуль" in exc_info.value.message

    @pytest.mark.unit
    def test_negative_amount_raises_error(self):
        """Від'ємна сума кидає ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(-10.50, 1, "Тест", date.today())
        assert exc_info.value.field == "amount"

    @pytest.mark.unit
    def test_amount_exceeds_limit_raises_error(self):
        """Сума що перевищує ліміт (1_000_000) кидає ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(1_000_001, 1, "Тест", date.today())
        assert exc_info.value.field == "amount"
        assert "перевищує ліміт" in exc_info.value.message

    @pytest.mark.unit
    def test_invalid_category_raises_error(self):
        """Неприпустима категорія (99) кидає ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(100, 99, "Тест", date.today())
        assert exc_info.value.field == "category_id"
        assert "недопустима" in exc_info.value.message

    @pytest.mark.unit
    def test_empty_description_raises_error(self):
        """Порожній опис кидає ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(100, 1, "", date.today())
        assert exc_info.value.field == "description"

    @pytest.mark.unit
    def test_short_description_raises_error(self):
        """Опис менше 3 символів кидає ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(100, 1, "AB", date.today())
        assert exc_info.value.field == "description"
        assert "3 символи" in exc_info.value.message

    @pytest.mark.unit
    def test_future_date_raises_error(self):
        """Дата в майбутньому кидає ValidationError"""
        future_date = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError) as exc_info:
            ExpenseValidator.validate(100, 1, "Майбутнє", future_date)
        assert exc_info.value.field == "expense_date"
        assert "майбутньому" in exc_info.value.message


# ═══════════════════════════════════════════════════════════
# ПАРАМЕТРИЗОВАНІ ТЕСТИ — об'єднання схожих тестів
# ═══════════════════════════════════════════════════════════

class TestExpenseValidatorParametrized:
    """Параметризовані тести для зменшення дублювання коду"""

    @pytest.mark.unit
    @pytest.mark.parametrize("invalid_amount,expected_field", [
        (0, "amount"),              # нуль
        (-10, "amount"),            # від'ємне
        (-0.01, "amount"),          # від'ємне дробове
        (1_000_001, "amount"),      # перевищує ліміт
        (1_500_000, "amount"),      # значно перевищує ліміт
    ])
    def test_invalid_amounts_raise_validation_error(self, invalid_amount, expected_field):
        """Некоректні суми кидають ValidationError з полем 'amount'"""
        with pytest.raises(ValidationError) as exc:
            ExpenseValidator.validate(invalid_amount, 1, "Тест", date.today())
        assert exc.value.field == expected_field

    @pytest.mark.unit
    @pytest.mark.parametrize("invalid_category", [0, 6, 10, 99, -1])
    def test_invalid_categories_raise_error(self, invalid_category):
        """Неприпустимі категорії кидають ValidationError"""
        with pytest.raises(ValidationError) as exc:
            ExpenseValidator.validate(100, invalid_category, "Тест", date.today())
        assert exc.value.field == "category_id"

    @pytest.mark.unit
    @pytest.mark.parametrize("invalid_description", [
        "",           # порожній
        "  ",         # лише пробіли
        "AB",         # 2 символи
        "A",          # 1 символ
    ])
    def test_invalid_descriptions_raise_error(self, invalid_description):
        """Некоректні описи кидають ValidationError"""
        with pytest.raises(ValidationError) as exc:
            ExpenseValidator.validate(100, 1, invalid_description, date.today())
        assert exc.value.field == "description"
