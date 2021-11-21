class NineSquareRecognizer:
    def __init__(self, x_array: list, y_array: list):
        if len(x_array) != len(y_array):
            raise IndexError('len(x_array) != len(y_array)')

        self.templates = dict()
        self.generate_templates()

        self.candidate = ["0" for _ in range(9)]
        self.define_candidate(x_array, y_array)
        self.template_answer = self.find_template_answer()

    def find_template_answer(self):
        for template_key in self.templates.keys():
            for tem_area_i, tem_area in enumerate(self.templates[template_key]):
                if tem_area == "0" or tem_area == "1":
                    if self.candidate[tem_area_i] != tem_area:
                        # continue to next template
                        break
                if tem_area_i == len(self.templates[template_key]) - 1:
                    return template_key
        return None

    def get_template_answer(self):
        return self.template_answer

    def define_candidate(self, x_array, y_array):
        min_x = min(x_array)
        min_y = min(y_array)
        max_x = max(x_array)
        max_y = max(y_array)

        x_range = max_x - min_x
        y_range = max_y - min_y

        x_0 = min_x
        x_1 = min_x + x_range / 3
        x_2 = min_x + x_range / 3 * 2
        x_3 = max_x

        y_0 = min_y
        y_1 = min_y + y_range / 3
        y_2 = min_y + y_range / 3 * 2
        y_3 = max_y

        for i in range(len(x_array)):
            if self.candidate[0] == "0" and x_0 <= x_array[i] <= x_1 \
                    and y_0 <= y_array[i] <= y_1:
                self.candidate[0] = "1"
            elif self.candidate[1] == "0" and x_1 <= x_array[i] <= x_2 \
                    and y_0 <= y_array[i] <= y_1:
                self.candidate[1] = "1"
            elif self.candidate[2] == "0" and x_2 <= x_array[i] <= x_3 \
                    and y_0 <= y_array[i] <= y_1:
                self.candidate[2] = "1"

            elif self.candidate[3] == "0" and x_0 <= x_array[i] <= x_1 \
                    and y_1 <= y_array[i] <= y_2:
                self.candidate[3] = "1"
            elif self.candidate[4] == "0" and x_1 <= x_array[i] <= x_2 \
                    and y_1 <= y_array[i] <= y_2:
                self.candidate[4] = "1"
            elif self.candidate[5] == "0" and x_2 <= x_array[i] <= x_3 \
                    and y_1 <= y_array[i] <= y_2:
                self.candidate[5] = "1"

            elif self.candidate[6] == "0" and x_0 <= x_array[i] <= x_1 \
                    and y_2 <= y_array[i] <= y_3:
                self.candidate[6] = "1"
            elif self.candidate[7] == "0" and x_1 <= x_array[i] <= x_2 \
                    and y_2 <= y_array[i] <= y_3:
                self.candidate[7] = "1"
            elif self.candidate[8] == "0" and x_2 <= x_array[i] <= x_3 \
                    and y_2 <= y_array[i] <= y_3:
                self.candidate[8] = "1"

    def generate_templates(self):
        self.templates[">"] = ["1", "X", "X",
                               "0", "X", "1",
                               "1", "X", "X"]
        self.templates["<"] = ["X", "X", "1",
                               "1", "X", "0",
                               "X", "X", "1"]
        self.templates["^"] = ["X", "1", "X",
                               "X", "X", "X",
                               "1", "0", "1"]
        # Letter 'O', not a zero '0'
        self.templates["O"] = ["1", "1", "1",
                               "1", "0", "1",
                               "1", "1", "1"]
        self.templates["/"] = ["0", "X", "1",
                               "X", "X", "X",
                               "1", "X", "0"]
