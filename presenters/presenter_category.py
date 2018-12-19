from models.model_category import Category


class CategoryPresenter:
    def __init__(self):
        self._categories = Category.find_all()

    def get_categories(self):
        return Category.find_all()

    def add_new_categories(self, categories):
        for category in categories:
            Category.insert(category[1])
            # if category not in self._categories:
            #     self._categories.append(category)

    def find_category_id_by_name(self, name):
        id_index = 0
        result = Category.find_by_name(name)
        return result[id_index]
