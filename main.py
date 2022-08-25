import pandas
import pandas as pd

df = pandas.read_csv("../Assets/webInq.csv")

outDf = pandas.DataFrame()

firstNames = []
lastNames = []
emails = []

for item in df.Body:
    allWords = item.split(' ')
    name = []
    for word in allWords:
        if "has" in word:
            if "\u2009" in word:
                name.append(word.split("\u2009")[0])
            break
        name.append(word)

    email = ""
    for i in range(0, len(allWords)):
        if "Email:" in allWords[i]:
            email = allWords[i+1][:-7]

    firstNames.append(name[0])

    name.reverse()
    for i in name:
        if i != "" and i != "III" and i != "Jr" and i != "II" and i != "I":
            lastNames.append(i)
            break

    emails.append(email)

outDf["first names"] = firstNames
outDf["last names"] = lastNames
outDf["emails"] = emails

outDf.to_csv("../Assets/nameEmail.csv", index=False)