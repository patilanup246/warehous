from multiprocessing import Process
import uhaul
import u_store_baltimore
import extraspace
import publicstorage


def uhaul_scrap_process(zip_code_lst):
    uhaul_unique_url_lst = []
    uhaul.uhaul_scrap(zip_code_lst, uhaul_unique_url_lst)


def uStoreBaltimore_scrap_process(zip_code_lst):
    uStoreBaltimore_unique_url_lst = []
    u_store_baltimore.uStoreBaltimore_scrap(zip_code_lst, uStoreBaltimore_unique_url_lst)


def publicstorage_scrap_process(zip_code_lst):
    publicstorage_unique_url_lst = []
    publicstorage.publicstorage_scrap(zip_code_lst, publicstorage_unique_url_lst)


def extraspace_scrap_process(zip_code_lst):
    extraspace_unique_url_lst = []
    extraspace.extraspace_scrap(zip_code_lst, extraspace_unique_url_lst)


if __name__ == '__main__':
    try:
        zip_code_lst = []
        with open("zip_code.txt", "r") as f:
            file = f.read()
            zip_codes = file.split(",")
            for code in zip_codes:
                if len(code.strip()) > 0:
                    zip_code_lst.append(code.strip())

        p1 = Process(target=uhaul_scrap_process, args=(zip_code_lst,))
        p2 = Process(target=uStoreBaltimore_scrap_process, args=(zip_code_lst,))
        p3 = Process(target=publicstorage_scrap_process, args=(zip_code_lst,))
        p4 = Process(target=extraspace_scrap_process, args=(zip_code_lst,))

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()

    except:
        pass
