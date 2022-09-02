import csv
import scarper
import time


def main():

    sc = scarper.Scraper()
    pageNum = 48

    data = []

    with open('emlak_verisi.csv', 'w', encoding = 'utf-8-sig') as f:

        thewriter = csv.writer(f)

        # for i in range(1, pageNum):
        #     # sayfaların her birine gidecek, yalnızca sütunları alacak
        #
        #     if i <= 10:
        #         sc.set_url(sc.get_url()[:len(sc.get_url()) - 1] + str(i))
        #     else:
        #         sc.set_url(sc.get_url()[:len(sc.get_url()) - 2] + str(i))
        #
        #     sc.load_url()
        #     sc.read_data()
        #
        #     for h in sc.get_hrefs():
        #
        #         sc.get_columns("http://www.emlakjet.com/" + h)
        #
        #     sc.dump_hrefs()
        #     print(str(i) + ". SAYFADAN SÜTUNLAR ALINDI ---------------------------")


        thewriter.writerow(sc.columns)
        print(sc.columns)

        for i in range(1, pageNum):
            if i <= 10:
                sc.set_url(sc.get_url()[:len(sc.get_url()) - 1] + str(i))
            else:
                sc.set_url(sc.get_url()[:len(sc.get_url()) - 2] + str(i))

            sc.load_url()
            sc.read_data()

            for h in sc.get_hrefs():

                data.append(sc.get_info("http://www.emlakjet.com/" + h))
                print(sc.get_info("http://www.emlakjet.com/" + h))

            sc.dump_hrefs()
            print(str(i) + ". SAYFADAN BİLGİLER ALINDI ---------------------------")

        # write the data
        thewriter.writerows(data)


if __name__ == '__main__':
    main()