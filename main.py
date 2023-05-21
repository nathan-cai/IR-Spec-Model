import jcamp
import csv
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt


def row_to_write(name, val):
    result = [name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    result.extend(val)
    return result


def valid_spec(jcamp_content):
    if len(jcamp_content["x"]) == 0:
        return False
    elif jcamp_content["x"][0] % 1 != 0.0:
        return False
    elif 550.0 not in jcamp_content["x"] or 3846.0 not in jcamp_content["x"]:
        return False
    else:
        return True


def get_indices(arr):
    start = -1
    end = -1
    for index in range(len(arr)):
        if arr[index] == 550.0:
            start = index
        if arr[index] == 3846.0:
            end = index
    return start, end


if __name__ == "__main__":

    # Data will be written into data.csv
    with open('data.csv', 'a', newline='') as FILE:
        writer = csv.writer(FILE)

        # cas_num.txt includes cas numbers to be used to generate urls to IR Specs
        cas = open('cas_num.txt', 'r')

        for i in range(44388):
            # Wrap in try and except due to occurence of uni code errors
            try:
                # reads a new entry for cas line
                curr = cas.readline().strip()
                currSplit = curr.split(",,")
                num = currSplit[2].replace('-', '')

                # generate url for cas number
                url = f'https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C{num}&Index=0&Type=IR'
                response = requests.get(url)
                content = response.content.splitlines()
                content = [line.decode("utf-8") for line in content]
                d = jcamp.jcamp_read(content)

                # write to data.csv if the spec is valid
                if valid_spec(d):
                    a, b = get_indices(d["x"])
                    row = row_to_write(currSplit[0], d["y"][a:b + 1])
                    writer.writerow(row)

            except:
                print(f'error at {i}')

            print(i)

        cas.close()
