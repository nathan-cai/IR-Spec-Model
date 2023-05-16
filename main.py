import jcamp
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt


def row_to_write(name, val):
    result = [name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result.extend(val)
    return result


if __name__ == "__main__":
    d = jcamp.jcamp_readfile("JCampFiles/592-43-8-IR.jdx")
    print(len(d["x"]))
    print(len(d["y"]))
    print(d["x"])
    print(d["y"])
    FILE = open('data.csv', 'a')

    writer = csv.writer(FILE)
    row = row_to_write('2-hexene', d["y"])

    writer.writerow(row)

    FILE.close()
