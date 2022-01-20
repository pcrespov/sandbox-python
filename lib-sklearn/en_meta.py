# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable


import math
import random
from copy import deepcopy
from typing import Callable, Sequence, Tuple, TypeVar

import numpy as np
import pytest
from scipy.stats import norm, uniform
from sklearn.linear_model import LinearRegression

T = TypeVar["T"]


def iter_sensitivity(
    paramrefs: Sequence[T],
    paramdiff: Sequence[T],
    diff_or_fact: bool,
):
    assert len(paramrefs) == len(paramdiff)

    n_dims = len(paramrefs)

    for i in range(n_dims):
        paramtestplus = deepcopy(paramrefs)
        paramtestminus = deepcopy(paramrefs)

        # inc/dec one dimension at a time
        if diff_or_fact:
            paramtestplus[i] += paramdiff[i]
        else:
            paramtestplus[i] *= paramdiff[i]

        if diff_or_fact:
            paramtestminus[i] -= paramdiff[i]
        else:
            paramtestminus[i] /= paramdiff[i]  # check that not zero

        yield (i, paramtestplus, paramtestminus)


def eval_regression(
    paramrefs,
    paramtestplus,
    paramtestminus,
    refval,
    testvalplus,
    testvalminus,
    *,
    i: int,
    lin_or_power: bool
) -> Tuple[T, T]:
    linear_regressor = LinearRegression()

    x = np.array([paramrefs[i], paramtestplus[i], paramtestminus[i]]).reshape((-1, 1))
    y = np.array([refval, testvalplus, testvalminus])

    if not lin_or_power:
        x = np.log(x / x[1])  # must be larger than zero
        y = np.log(y / y[1])

    model = linear_regressor.fit(x, y)

    sensitivity = model.coef_[0]
    linearity = model.score(x, y)
    return sensitivity, linearity



def main():

    paramrefs=[1,2,3]
    paramdiff=[0.1, 0.1, 0.5]
     
    # //
    refval = myfunc(paramrefs)

    for i,paramtestplus, paramtestminus in iter_sensitivity(paramrefs=paramrefs, paramdiff=paramdiff, diff_or_fact=True):
        
        # //
        testvalplus = myfunc(paramtestplus)
        testvalminus = myfunc(paramtestminus)

        eval_regression(paramrefs, paramtestplus, paramtestminus, refval, testvalplus, testvalminus, i=i)





def sensitivity(
    func: Callable[[Sequence[T]], T],
    paramrefs: Sequence[T],
    paramdiff: Sequence[T],
    diff_or_fact: bool,
    lin_or_power: bool,
):

    n_dims = len(paramrefs)

    sensitivities = []
    linearities = []

    # eval at a point
    refval: T = func(paramrefs)

    linear_regressor = LinearRegression()

    for i in range(n_dims):
        paramtestplus = deepcopy(paramrefs)
        paramtestminus = deepcopy(paramrefs)

        # inc/dec one dimension at a time
        if diff_or_fact:
            paramtestplus[i] += paramdiff[i]
        else:
            paramtestplus[i] *= paramdiff[i]

        if diff_or_fact:
            paramtestminus[i] -= paramdiff[i]
        else:
            paramtestminus[i] /= paramdiff[i]  # check that not zero

        # evaluate func on that inc/dec
        testvalplus: T = func(paramtestplus)
        testvalminus: T = func(paramtestminus)

        # compute sensitivity/linearity of func along i-th dimension
        x = np.array([paramrefs[i], paramtestplus[i], paramtestminus[i]]).reshape(
            (-1, 1)
        )
        y = np.array([refval, testvalplus, testvalminus])

        if not lin_or_power:
            x = np.log(x / x[1])  # must be larger than zero
            y = np.log(y / y[1])

        model = linear_regressor.fit(x, y)

        # colleting results
        sensitivities.append(model.coef_[0])
        linearities.append(model.score(x, y))

    return refval, sensitivities, linearities



def myfunc(x):
    prod = 1
    for i in x:
        prod *= i ** 2
    return prod


@pytest.fixture
def myparamrefs():
    return [1, 2, 3]


@pytest.fixture
def myparamuncerts():
    return [0.1, 0.1, 0.5]


@pytest.fixture
def myparamuncerttypes():
    return ["N", "R", "N"]


@pytest.mark.parametrize("lin_or_power", [True, False])
def test_1(myparamrefs, myparamuncerts, myparamuncerttypes, lin_or_power):
    diff_or_fact = True

    sensitivity(myfunc, myparamrefs, myparamuncerts, diff_or_fact, lin_or_power)
    u = uncertainty(
        myfunc,
        myparamrefs,
        myparamuncerts,
        myparamuncerttypes,
        diff_or_fact,
        lin_or_power,
    )

    print("val:", u[0], "+-", u[2], "(", u[3], "dB)")
    print("uncertainty contributions:", u[1])
    print("sensitivity factors:", u[4])
    print("linearity:", u[5])


@pytest.mark.parametrize("initcount", [20, 1000])
def test_metropolis_hastings_uncertainty(
    myparamrefs, myparamuncerts, myparamuncerttypes, initcount
):
    nrruns = 10
    estimates = np.zeros((nrruns, 2))

    for i in range(nrruns):
        estimates[i, :] = MetropolisHastingsUncertainty(
            myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, initcount, 1000
        )

    print(
        "(",
        estimates[:, 0].mean(),
        "+-",
        estimates[:, 0].std(),
        ")",
        "+-",
        "(",
        estimates[:, 1].mean(),
        "+-",
        estimates[:, 1].std(),
        ")",
    )

    e = MetropolisHastingsUncertainty(
        myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 100, 100000
    )
    assert e == [37.87169680284157, 15.063556290352436]

    e = MetropolisHastingsUncertainty(
        myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 100, 100000
    )
    assert e == [37.49986517853013, 14.750375035278662]
