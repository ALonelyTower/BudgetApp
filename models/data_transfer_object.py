

class TransactionDTO:
    def __init__(self, transaction_id, date, category, payment_method, total_expense, description):
        self.id = transaction_id
        self.date = date

        if isinstance(category, int):
            self.category = CategoryDTO(category_id=category, name="")
        else:
            self.category = category

        self.payment_method = payment_method
        self.total_expense = total_expense
        self.description = description

    @classmethod
    def new(cls, date, category, payment_method, total_expense, description):
        return TransactionDTO(transaction_id=-1, date=date, category=category, payment_method=payment_method,
                              total_expense=total_expense, description=description)

    def prepare_values_for_insert(self):
        return self.date, self.category.id, self.payment_method, self.total_expense, self.description

    def prepare_values_for_update(self):
        return self.date, self.category.id, self.payment_method, self.total_expense, self.description, self.id

    def prepare_values_for_form(self):
        return self.id, self.date, self.category.id, self.payment_method, self.total_expense, self.description

    def __eq__(self, other):
        return self.prepare_values_for_update() == other.prepare_values_for_update()

    def __repr__(self):
        return f"TransactionDTO({self.id}, '{self.date}', {self.category}, '{self.payment_method}', " \
                f"{self.total_expense}, '{self.description}')"


class CategoryDTO:
    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name

    @classmethod
    def new(cls, name):
        return CategoryDTO(category_id=-1, name=name)

    def __repr__(self):
        return f"CategoryDTO({self.id}, '{self.name}')"
