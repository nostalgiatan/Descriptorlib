import pytest
from coverage import Coverage

def run_tests_with_coverage():
    cov = Coverage()
    cov.start()

    pytest.main(args=['-v', 'descriptorlib/tests'])

    cov.stop()
    cov.save()

    cov.report()
    cov.xml_report(outfile='coverage.xml')  # 生成 XML 报告
    print("覆盖率报告已保存到 coverage.xml")

if __name__ == '__main__':
    run_tests_with_coverage()