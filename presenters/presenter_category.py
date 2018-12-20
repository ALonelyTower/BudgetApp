from models.model_category import Category


class CategoryPresenter:
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
        id_index = 0
        result = Category.find_by_name(name)
        return result[id_index]

    def find_name_by_id(self, category_id):
        if self._is_dirty:
            self._refresh_categories()

        name_result = None
        for category in self._categories:
            if category_id == category.id:
                name_result = category.name
        return name_result

    def _refresh_categories(self):
        self._categories = Category.find_all()
        self._is_dirty = False

