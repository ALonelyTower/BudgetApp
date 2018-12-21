from models.model_category import Category


class CategoryPresenter:
    # TODO: Feels like this presenter and its model's responsibilities have blurred a bit.
    def __init__(self):
        self._categories = Category.find_all()
        self._is_dirty = False

    def get_categories(self):
        if self._is_dirty:
            self._refresh_categories()

        return self._categories

    def add_new_categories(self, categories):
        for category in categories:
            Category.insert(category.name)
        self._is_dirty = True

    def find_id_by_name(self, name):
        # TODO: What happens when there are duplicates?  Will there be duplicates?
        if self._is_dirty:
            self._refresh_categories()

        id_result = None
        for category in self._categories:
            if category.name == name:
                id_result = category.id
        return id_result

    def find_name_by_id(self, category_id):
        if self._is_dirty:
            self._refresh_categories()

        name_result = None
        for category in self._categories:
            if category.id == category_id:
                name_result = category.name
        return name_result

    def _refresh_categories(self):
        self._categories = Category.find_all()
        self._is_dirty = False

