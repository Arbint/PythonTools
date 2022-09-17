RawData = "curve -d 1 -p -2 0 2 -p -4 0 0 -p -4 0 -4 -p -3 0 -4 -p -3 0 -2 -p -3 0 -6 -p -2 0 -6 -p -2 0 -3 -p -2 0 -7 -p -1 0 -7 -p -1 0 -3 -p -1 0 -6 -p 0 0 -6 -p 0 0 -3 -p 0 0 -5 -p 1 0 -5 -p 1 0 0 -p 0 0 2 -p -2 0 2 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 ;"

while " " in RawData:
    RawData = RawData.replace(" ", "")

points = "["

for i in range(0, len(RawData)):
    c = RawData[i]
    if c == "p":
        point = "("
        next = RawData[i + 1]
        while next != "p" and next !="k":
            point += next
            if next != '-':
                point += ','
            i+=1
            if i >= len(RawData)-1:
                break
            next = RawData[i+1]
        point = point[:-2]
        point+="),"
        points += point

points = points[:-1] + "]"

print(points)