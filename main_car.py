import csv
import scarper
import time


def main():

    sc = scarper.Scraper()
    pageNum = 45
    data = []

    with open('emlak_verisi.csv', 'w', encoding='utf-8-sig') as f:

        thewriter = csv.writer(f)

        thewriter.writerow(sc.columns)
        print(sc.columns)

        for i in range(8, pageNum):
            if i <= 10:
                sc.set_url(sc.get_url()[:len(sc.get_url()) - 1] + str(i))
            elif i ==24:
                continue
            else:
                sc.set_url(sc.get_url()[:len(sc.get_url()) - 2] + str(i))

            sc.load_url()
            sc.read_data()

            for h in sc.get_hrefs():

                data.append(sc.get_info("https://www.arabam.com/" + h))
                print(sc.get_info("https://www.arabam.com/" + h))


            sc.dump_hrefs()
            print(str(i) + ". SAYFADAN BİLGİLER ALINDI ---------------------------")

        # write the data
        thewriter.writerows(data)


if __name__ == '__main__':
    main()