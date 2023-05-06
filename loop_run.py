from kijijiauto import KijijiAutoScraper
from time import sleep
import datetime


if __name__ == "__main__":
    kijiji = KijijiAutoScraper()
    while True:
        try:
            kijiji.main()
            print("Wait 10 min!")
            print(datetime.datetime.now())
            print("To stop script press Ctrl+C")
            sleep(60*10)
        except Exception as err:
            print(err)
            print('Catching all exceptions')
            pass
print("Exiting loop_run")