import ciel.score_template_matching as stm


class ScoreRecognizer:
    NUM_SCORE_DIGITS = 8

    def __init__(self, path: str):
        self.model = stm.load(path)

    def predict(self, image):
        predicted = ['', '']
        for i in range(2):
            for j in range(self.NUM_SCORE_DIGITS):
                predicted[i] += stm.predict(image[i, j], self.model)
        return predicted
