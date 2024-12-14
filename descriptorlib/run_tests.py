# Descriptorlib/run_coverage.py
import pytest
from coverage import Coverage

def run_tests_with_coverage():
    cov = Coverage()
    cov.start()

    pytest.main(args=['-v', 'Descriptorlib/tests'])

    cov.stop()
    cov.save()

    cov.report()
    cov.html_report(directory='htmlcov')
    print("覆盖率报告已保存到 htmlcov/index.html")

if __name__ == '__main__':
    run_tests_with_coverage()