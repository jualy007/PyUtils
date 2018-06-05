#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

from lib.db.mysql import Mysql


class GuessPlate():
    '''
    Guess Game Plate Calcuator.
    '''

    UPPLATE = 0  # 主队是否是让球方，0 为让球方，即盘口小于0. 被让球方值为1

    BONUS = 0  # 上盘口奖金，下盘口奖金

    UPPLATERATE = 2

    DOWNPLATERATE = 2

    def __init__(self, plate=-0.25, rate=[2, 2]):
        self.setPlate(plate)
        self.setRate(rate)

    def setPlate(self, plate):

        if isinstance(plate, list):
            if plate[1] <= 0:
                self.UPPLATE = 0
            else:
                self.UPPLATE = 1

            self._plate = [plate[0].__abs__(), plate[1].__abs__()]
        elif (not plate == 0) and (not plate % 0.5 == 0):
            if plate <= 0.0:
                self.UPPLATE = 0
            else:
                self.UPPLATE = 1

            self._plate = [plate.__abs__() - 0.25, plate.__abs__() + 0.25]
        else:
            if plate <= 0.0:
                self.UPPLATE = 0
                self._plate = plate.__abs__()
            else:
                self.UPPLATE = 1
                self._plate = plate

    def setRate(self, rate):
        self.rate = rate

        if self.UPPLATE == 0:
            self.UPPLATERATE = rate[0]
            self.DOWNPLATERATE = rate[1]
        else:
            self.UPPLATERATE = rate[1]
            self.DOWNPLATERATE = rate[0]

    def setScore(self, result):
        '''
        Calculate Win Score.
        '''
        self.result = result.strip()

        if self.UPPLATE == 0:
            self._winscore = int(self.result[0]) - int(self.result[2])
        else:
            self._winscore = int(self.result[2]) - int(self.result[0])

    def calcBonus(self, value, option=0):
        '''
        Calculate Bonus.
        '''

        if isinstance(self._plate, list):
            if self._winscore > self._plate[1]:
                self.BONUS = self.win(
                    value,
                    self.UPPLATERATE) if ((self.UPPLATE ^ option) == 0) else 0
            elif self._winscore <= self._plate[1] and self._winscore > self._plate[0]:
                self.BONUS = self.halfWin(value, self.UPPLATERATE) if ((
                    self.UPPLATE ^ option) == 0) else self.halfLose(value)
            elif self._winscore == self._plate[0]:
                self.BONUS = self.halfLose(value) if ((
                    self.UPPLATE ^ option) == 0) else self.halfWin(
                        value, self.DOWNPLATERATE)
            else:
                self.BONUS = 0 if ((self.UPPLATE ^ option) == 0) else self.win(
                    value, self.DOWNPLATERATE)
        else:
            if self._winscore > self._plate:
                self.BONUS = self.win(
                    value,
                    self.UPPLATERATE) if ((self.UPPLATE ^ option) == 0) else 0
            elif self._winscore == self._plate:
                self.BONUS = value
            else:
                self.BONUS = 0 if ((self.UPPLATE ^ option) == 0) else self.win(
                    value, self.DOWNPLATERATE)

        return self.BONUS

    def win(self, value, rate):
        return rate * value

    def lose(self):
        return 0

    def push(self, value):
        return value

    def halfLose(self, value):
        return value / 2

    def halfWin(self, value, rate):
        return value / 2 * rate + value / 2


class GuessPlateDB(GuessPlate):
    TITLE = "index   Charge Address" + " " * 32 + \
        "Rate    " + "Bottom Amount " + " " * 6 + "Bonus"

    def __init__(self, *args, **kwargs):
        self.mysql = Mysql('172.17.1.128', 'sp_test', 'sp_test', 'sp_demo')
        self.mysql.conect()

    def getContract(self, name):
        query = 'SELECT A.id, B.score, B.handicap from blk_fortune_contract as A RIGHT JOIN fortune_forecast_event as B on A.address = B.address WHERE A.contract_name = "{0}"'.format(
            name)
        self.mainId, self.score, plate = self.mysql.query(query)[0]

        if plate.__contains__(','):
            super().setPlate([
                float(plate.split(',')[0].strip()),
                float(plate.split(',')[1].strip())
            ])
        else:
            super().setPlate(float(plate))

    def getRate(self):
        query = 'SELECT B.odds from blk_fortune_contract as A LEFT JOIN fortune_forecast_option as B on A.address = B.address where A.parent_contract_id = {0} ORDER BY A.option_index'.format(
            self.mainId)
        rates = self.mysql.query(query)

        super().setRate([rates[0][0], rates[1][0]])

    def setScore(self, score=None):
        if not score and (not self.score and not self.score == ""):
            raise RuntimeError('Make Sure Guess Game Score haa been set!!!')
        else:
            if score:
                super().setScore(score)
            else:
                super().setScore(self.score)

    def calcBonus(self):
        query = 'SELECT A.option_index, B.option_address, B.odds, B.amount from blk_fortune_contract as A RIGHT JOIN fortune_betting_record as B on B.option_id = A.forecast_game_or_option_id where  A.parent_contract_id = {0}'.format(
            self.mainId)
        records = self.mysql.query(query)

        for record in records:
            if record:
                if record[0] == 0:
                    super().setRate([record[2], self.rate[1]])
                else:
                    super().setRate([self.rate[0], record[2]])

                bonus = super().calcBonus(record[3], record[0])
                print(self.TITLE)
                print("{0}{1}    {2}{3}{4}".format(
                    '%-8d' % record[0], record[1], '%-8.3f' % record[2],
                    '%-20.15f' % record[3], '%-20.15f' % bonus))
            else:
                break

        self.mysql.close()


if __name__ == '__main__':
    guess = GuessPlate(plate=-0.75, rate=[1.775, 1.975])
    guess.setScore('1:2')

    print(guess.calcBonus(1.99999999, 0))
    print(guess.calcBonus(0.99999999, 1))

    # guessplatedb = GuessPlateDB()
    # guessplatedb.getContract('B_7队 VS C_7队')
    # guessplatedb.getRate()
    # guessplatedb.setScore()
    # guessplatedb.calcBonus()
