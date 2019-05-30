import argparse
import csv
import requests
import os
import time


def mkdir(outfolder, row):
    year = row[0].split("/")[0]
    admin = row[1]
    admin_eng = admin_name_jtoe(admin)
    meeting = row[2].split()[0]
    path = os.path.join(outfolder, admin_eng, year, meeting)
    os.makedirs(path, exist_ok=True)
    return path


def save(pathname, r):
    with open(pathname, 'wb') as g:
        g.write(r.content)


def admin_name_jtoe(admin_name):
    name = dict()
    name["内閣府"] = "cao"
    name["国会"] = "diet"
    name["財務省"] = "mof"
    name["環境省"] = "env"
    name["国土交通省"] = "mlit"
    name["厚生労働省"] = "mhlw"
    name["経済産業省"] = "meti"
    name["水産庁"] = "suisan"
    name["首相官邸"] = "kantei"
    name["内閣官房"] = "cas"
    name["文部科学省"] = "mext"
    name["農林水産省"] = "maff"
    name["総務省"] = "soumu"
    name["林野庁"] = "rinya"
    name["外務省"] = "mofa"
    name["法務省"] = "moj"
    name["防衛省"] = "mod"
    name["日本学術会議"] = "scj"
    return name[admin_name]


def main(args):
    infile = args.file
    outfolder = args.outfolder
    notexist = []
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    with open(infile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            print("process {}".format(",".join(row)))
            path = mkdir(outfolder, row)
            url = row[4]
            name1, name2 = url.split("/")[-2:]
            pathname = path + "/" + name1 + "_" + name2
            if os.path.exists(pathname):
                print("this file exists")
                continue
            
            time.sleep(1)
            try:
                r = requests.get("http://" + url)
                if r.status_code != requests.codes.ok:
                    r = requests.get("https://" + url)
                    if r.status_code != requests.codes.ok:
                        notexist.append(",".join(row))
                        continue

            except:
                notexist.append(",".join(row))
                continue

            save(pathname, r)

    with open("notexist", 'w') as h:
        for ne in notexist:
            print(ne, file=h)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="designate input csv file")
    parser.add_argument("-o", "--outfolder",
                        help="designate output folder name")
    args = parser.parse_args()
    main(args)

