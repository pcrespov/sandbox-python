#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import random

import numpy as np
from scipy.stats import norm, uniform
from sklearn.linear_model import LinearRegression

# does it make sense to keep both diff_or_fact and lin_or_power? we could instead have a single dB option. code would be cleaner and there would not be asymmetry issues


# In[2]:


def sensitivity(func, paramrefs, paramdiff, diff_or_fact, lin_or_power):
    sensitivities = []
    linearities = []

    refval = func(paramrefs)

    if len(paramrefs) != len(paramdiff):
        return [refval, sensitivities, linearities]

    linear_regressor = LinearRegression()

    for i in range(len(paramrefs)):
        paramtestplus = paramrefs.copy()
        paramtestminus = paramrefs.copy()
        if diff_or_fact:
            paramtestplus[i] += paramdiff[i]
        else:
            paramtestplus[i] *= paramdiff[i]
        if diff_or_fact:
            paramtestminus[i] -= paramdiff[i]
        else:
            paramtestminus[i] /= paramdiff[i]  # check that not zero

        testvalplus = func(paramtestplus)

        testvalminus = func(paramtestminus)

        x = np.array([paramrefs[i], paramtestplus[i], paramtestminus[i]]).reshape(
            (-1, 1)
        )
        y = np.array([refval, testvalplus, testvalminus])
        if not lin_or_power:
            x = np.log(x / x[1])  # must be larger than zero
            y = np.log(y / y[1])
        model = linear_regressor.fit(x, y)
        sensitivities.append(model.coef_[0])
        linearities.append(model.score(x, y))

    return refval, sensitivities, linearities


# In[3]:


def uncertainty(
    func, paramrefs, paramuncerts, paramuncerttypes, diff_or_fact, lin_or_power
):
    refval, sensitivities, linearities = sensitivity(
        func, paramrefs, paramuncerts, diff_or_fact, lin_or_power
    )
    uncerts = []
    totaluncert = 0.0
    totaluncertdB = 0.0
    if (len(paramrefs) != len(paramuncerts)) or (
        len(paramrefs) != len(paramuncerttypes)
    ):
        return [refval, uncerts, totaluncert, totaluncertdB, sensitivities, linearities]

    for i in range(len(paramrefs)):
        if lin_or_power:
            if diff_or_fact:
                uncerts.append(sensitivities[i] * paramuncerts[i])
            else:
                uncerts.append(
                    sensitivities[i] * paramrefs[i] * (paramuncerts[i] - 1)
                )  # not symmetric
        else:
            if diff_or_fact:
                uncerts.append(
                    sensitivities[i] * np.log(paramuncerts[i] / paramrefs[i] + 1)
                )  # not symmetric
            else:
                uncerts.append(sensitivities[i] * np.log(paramuncerts[i]))

        if paramuncerttypes[i] == "R":
            uncerts[i] /= math.sqrt(3)

        totaluncert += uncerts[i] ** 2
    totaluncert = math.sqrt(totaluncert)
    totaluncertdB = totaluncert
    if lin_or_power:
        totaluncertdB = np.log(totaluncert / refval + 1)  # not symmetric
    else:
        totaluncert = (np.exp(totaluncertdB) - 1) * refval  # not symmetric
    return refval, uncerts, totaluncert, totaluncertdB, sensitivities, linearities


# k=2


# In[15]:


def myfunc(x):
    prod = 1
    for i in x:
        prod *= i**2
    return prod


myparamrefs = [1, 2, 3]
myparamuncerts = [0.1, 0.1, 0.5]
myparamuncerttypes = ["N", "R", "N"]
diff_or_fact = True
lin_or_power = True

sensitivity(myfunc, myparamrefs, myparamuncerts, diff_or_fact, lin_or_power)


u = uncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, diff_or_fact, lin_or_power
)

print("val:", u[0], "+-", u[2], "(", u[3], "dB)")
print("uncertainty contributions:", u[1])
print("sensitivity factors:", u[4])
print("linearity:", u[5])


# In[5]:


lin_or_power = False

sensitivity(myfunc, myparamrefs, myparamuncerts, diff_or_fact, lin_or_power)
u = uncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, diff_or_fact, lin_or_power
)

print("val:", u[0], "+-", u[2], "(", u[3], "dB)")
print("uncertainty contributions:", u[1])
print("sensitivity factors:", u[4])
print("linearity:", u[5])


# In[6]:


myparamuncerts = [1.1, 1.05, 1.16]
diff_or_fact = False
lin_or_power = True

sensitivity(myfunc, myparamrefs, myparamuncerts, diff_or_fact, lin_or_power)
u = uncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, diff_or_fact, lin_or_power
)

print("val:", u[0], "+-", u[2], "(", u[3], "dB)")
print("uncertainty contributions:", u[1])
print("sensitivity factors:", u[4])
print("linearity:", u[5])


# In[7]:


lin_or_power = False

sensitivity(myfunc, myparamrefs, myparamuncerts, diff_or_fact, lin_or_power)
u = uncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, diff_or_fact, lin_or_power
)

print("val:", u[0], "+-", u[2], "(", u[3], "dB)")
print("uncertainty contributions:", u[1])
print("sensitivity factors:", u[4])
print("linearity:", u[5])


# In[8]:


# https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm


def MetropolisHastingsUncertainty(
    func, paramrefs, paramuncerts, paramuncerttypes, initcount, totalcount
):  # diff_or_fact
    n = len(paramrefs)
    jumpfactor = 0.5
    alpha = 0.0
    valsum = 0.0
    val2sum = 0.0

    currentparams = paramrefs.copy()

    counter = 0
    while counter < totalcount:
        i = random.randrange(n)
        candidate = norm.rvs(currentparams[i], paramuncerts[i] * jumpfactor)

        if paramuncerttypes[i] == "R":
            alpha = uniform.pdf(
                candidate, paramrefs[i] - paramuncerts[i], 2 * paramuncerts[i]
            ) / uniform.pdf(
                currentparams[i], paramrefs[i] - paramuncerts[i], 2 * paramuncerts[i]
            )
        else:
            alpha = norm.pdf(candidate, paramrefs[i], paramuncerts[i]) / norm.pdf(
                currentparams[i], paramrefs[i], paramuncerts[i]
            )

        if uniform.rvs() < alpha:
            currentparams[i] = candidate

        if counter > initcount:
            val = func(currentparams)
            valsum += val
            val2sum += val**2

        counter += 1

    valmean = valsum / (totalcount - initcount)
    val2mean = val2sum / (totalcount - initcount)
    valstddev = math.sqrt(val2mean - valmean**2)

    return [valmean, valstddev]


# In[16]:


nrruns = 10
estimates = np.zeros((nrruns, 2))

for i in range(nrruns):
    estimates[i, :] = MetropolisHastingsUncertainty(
        myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 20, 1000
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


# In[17]:


nrruns = 10
estimates = np.zeros((nrruns, 2))

for i in range(nrruns):
    estimates[i, :] = MetropolisHastingsUncertainty(
        myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 1000, 10000
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


# In[18]:


MetropolisHastingsUncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 100, 100000
)


# In[19]:


MetropolisHastingsUncertainty(
    myfunc, myparamrefs, myparamuncerts, myparamuncerttypes, 100, 100000
)


# In[ ]:
