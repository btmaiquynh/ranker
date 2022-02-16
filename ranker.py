import itertools
import csv


class ConfusionMatrix:
    def __init__(self, combination):
        self.combination = combination
        self.TP = 0
        self.FP = 0
        self.FN = 0
        self.TN = 0
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        # self.selectivity = 0
        # self.npv = 0
        # self.fnr = 0

    def __str__(self):
        result = ("="*(len(self.combination)*5)+"=========\n")
        result += ("--- " + str(self.combination)+"  ---\n")
        result += ("||| TN = " + str(self.TN) +
                   "\t | \tFN = " + str(self.FN) + " |||\n")
        result += ("-"*(len(self.combination)*5)+"---------\n")
        result += ("||| FP = " + str(self.FP) +
                   "\t | \tTP = " + str(self.TP) + " |||\n")
        result += ("="*(len(self.combination)*5)+"=========\n")
        return result

    def compAll(self):
        if (self.TP+self.TN+self.FP+self.FN) != 0:
            self.accuracy = (self.TP+self.TN)/(self.TP+self.TN+self.FP+self.FN)
        if (self.TP+self.FP) != 0:
            self.precision = (self.TP/(self.TP+self.FP))
        if (self.TP+self.FN) != 0:
            self.recall = (self.TP/(self.TP+self.FN))
        # self.selectivity = (self.TN/(self.TN+self.FP))
        # self.npv = (self.TN/(self.TN+self.FN))
        # self.fnr = (self.FN/(self.FN+self.TP))


class Rows:
    def __init__(self, allRows, allPossibilities):

        self.highestAccuracyCM = ConfusionMatrix(list())
        self.highestPrecisionCM = ConfusionMatrix(list())
        self.highestRecallCM = ConfusionMatrix(list())
        self.highestTP = ConfusionMatrix(list())

        self.allRows = allRows
        self.allPossibilities = allPossibilities
        self.confusionMatrix = [ConfusionMatrix(
            x) for x in self.allPossibilities]

        self.computeCMValues()
        self.computeCMEvaluator()
        self.findHighestEvaluator()

    def computeScore(self, row, combination):
        score = 0
        for j in range(len(combination)):
            score += (combination[j]*row.rowInfo[j+2])
        return round(score, 2)

    def computeCMValues(self):
        for i in range(len(self.allPossibilities)):
            curComb = self.allPossibilities[i]
            score = 0
            for row in self.allRows:
                score = self.computeScore(row, curComb)
                if score/5 < 0.6:
                    if (row.realScore == 0 or row.realScore == 1):  # TN
                        self.confusionMatrix[i].TN += 1
                    else:  # FN
                        self.confusionMatrix[i].FN += 1

                else:
                    if (row.realScore == 0 or row.realScore == 1):  # FP
                        self.confusionMatrix[i].FP += 1
                    else:  # TP
                        self.confusionMatrix[i].TP += 1

    def computeCMEvaluator(self):
        for cm in self.confusionMatrix:
            cm.compAll()

    def findHighestEvaluator(self):
        for cm in self.confusionMatrix:
            if cm.accuracy > self.highestAccuracyCM.accuracy:
                self.highestAccuracyCM = cm
            if cm.precision > self.highestPrecisionCM.precision:
                self.highestPrecisionCM = cm
            if cm.recall > self.highestRecallCM.recall:
                self.highestRecallCM = cm

            if cm.TP > self.highestTP.TP:
                self.highestTP = cm


class Row:
    def __init__(self, rowInfo):
        self.rowInfo = rowInfo
        self.id = rowInfo[0]
        self.realScore = rowInfo[1]
        # self.f1 = rowInfo[2]
        # self.f2 = rowInfo[3]
        # self.f3 = rowInfo[4]
        # self.f4 = rowInfo[5]
        # self.f5 = rowInfo[6]
        # self.f6 = rowInfo[7]
        # self.f7 = rowInfo[8]
        # self.f8 = rowInfo[9]
        # self.f9 = rowInfo[10]
        # self.f10 = rowInfo[11]


def permutate(weightList, fileName):
    allPermutations = [x for x in itertools.product(
        weightList, repeat=len(weightList)) if sum(x) == 1]

    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(allPermutations)

    return allPermutations


def main():
    # weights = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    weights = [0.1, 0.2, 0.3, 0.6, 0.7]
    allPossibilities = permutate(weights, 'allComb3.csv')

    # print(allPossibilities)

    example = [["id", 3, 1, 2, 3, 4, 5], ["id2", 2, 0, 3, 1, 2, 5]]
    rows = Rows([Row(x) for x in example], allPossibilities)

    print(rows.highestAccuracyCM)
    # print(rows.highestTP)

    # print(len(rows.confusionMatrix))

    # for cm in rows.confusionMatrix:
    #     print(cm)
    #     print("")


main()
