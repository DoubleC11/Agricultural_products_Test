import os
import  shutil
import pytest

if __name__ == '__main__':
    pytest.main()
    shutil.copy("./environment.xml", "./reports/allure-results")
    os.system('allure serve ./reports/allure-results')