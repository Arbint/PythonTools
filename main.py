import pandas
import pandas as pd

df = pandas.read_csv("../Assets/webInq.csv")

outDf = pandas.DataFrame()

names = []
emails = []

for item in df.Body:
    allWords = item.split(' ')
    name = ""
    for word in allWords:
        if "has" in word:
            if "\u2009" in word:
                name += word.split("\u2009")[0]
            break
        name += word + " "

    email = ""
    for i in range(0, len(allWords)):
        if "Email:" in allWords[i]:
            email = allWords[i+1][:-7]

    names.append(name)
    emails.append(email)

outDf["names"] = names
outDf["emails"] = emails

outDf.to_csv("../Assets/nameEmail.csv", index=False)