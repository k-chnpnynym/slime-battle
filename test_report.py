import unittest
import sys
import os
import datetime
import traceback
from typing import Optional, List, Dict, Any, Tuple, Type, Union
from types import TracebackType
from unittest.runner import TextTestRunner
from unittest.result import TestResult
from test_slime_battle import *

# OptExcInfoのカスタム型定義
ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]
OptExcInfo = Union[Tuple[None, None, None], ExcInfo]

class DetailedTestResult(TestResult):
    def __init__(self):
        super().__init__()
        self.test_details: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime.datetime] = None
        self.current_test = None

    def startTest(self, test):
        self.start_time = datetime.datetime.now()
        self.current_test = test
        super().startTest(test)

    def _calculate_elapsed_time(self) -> float:
        if self.start_time is None:
            return 0.0
        return (datetime.datetime.now() - self.start_time).total_seconds()

    def _format_error(self, err: OptExcInfo, test: unittest.TestCase) -> str:
        """エラー情報を文字列に変換"""
        if err[0] is None or err[1] is None:
            return "Unknown error"
        # スタックトレースを除外してエラーメッセージのみを取得
        return ''.join(traceback.format_exception_only(err[0], err[1]))

    def addSuccess(self, test):
        self.test_details.append({
            'name': test.id(),
            'result': 'OK',
            'time': self._calculate_elapsed_time(),
            'doc': test._testMethodDoc or "No description available"
        })
        super().addSuccess(test)

    def addError(self, test, err):
        self.test_details.append({
            'name': test.id(),
            'result': 'ERROR',
            'error': self._format_error(err, test),
            'time': self._calculate_elapsed_time(),
            'doc': test._testMethodDoc or "No description available"
        })
        super().addError(test, err)

    def addFailure(self, test, err):
        self.test_details.append({
            'name': test.id(),
            'result': 'FAIL',
            'error': self._format_error(err, test),
            'time': self._calculate_elapsed_time(),
            'doc': test._testMethodDoc or "No description available"
        })
        super().addFailure(test, err)

def generate_markdown_report(result):
    now = datetime.datetime.now()
    report = f"""# スライムバトルゲーム テスト実行レポート

## 実行概要
- 実行日時: {now.strftime('%Y-%m-%d %H:%M:%S')}
- テスト数: {result.testsRun}
- 成功: {len([t for t in result.test_details if t['result'] == 'OK'])}
- 失敗: {len([t for t in result.test_details if t['result'] == 'FAIL'])}
- エラー: {len([t for t in result.test_details if t['result'] == 'ERROR'])}

## テスト詳細

"""
    
    # テストクラスごとにグループ化
    test_classes = {}
    for detail in result.test_details:
        class_name = detail['name'].split('.')[1]
        if class_name not in test_classes:
            test_classes[class_name] = []
        test_classes[class_name].append(detail)

    for class_name, tests in test_classes.items():
        report += f"### {class_name}\n\n"
        for test in tests:
            test_name = test['name'].split('.')[-1]
            status_emoji = "✅" if test['result'] == 'OK' else "❌"
            report += f"#### {status_emoji} {test_name}\n"
            report += f"- 説明: {test['doc']}\n"
            report += f"- 結果: {test['result']}\n"
            report += f"- 実行時間: {test['time']:.3f}秒\n"
            if test['result'] != 'OK':
                report += f"- エラー詳細:\n```\n{test['error']}\n```\n"
            report += "\n"

    return report

def generate_html_report(result):
    now = datetime.datetime.now()
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>スライムバトルゲーム テスト実行レポート</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .success {{ color: green; }}
        .failure {{ color: red; }}
        .test-case {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
        .test-details {{ margin-left: 20px; }}
        pre {{ background-color: #f5f5f5; padding: 10px; }}
    </style>
</head>
<body>
    <h1>スライムバトルゲーム テスト実行レポート</h1>
    <h2>実行概要</h2>
    <ul>
        <li>実行日時: {now.strftime('%Y-%m-%d %H:%M:%S')}</li>
        <li>テスト数: {result.testsRun}</li>
        <li>成功: {len([t for t in result.test_details if t['result'] == 'OK'])}</li>
        <li>失敗: {len([t for t in result.test_details if t['result'] == 'FAIL'])}</li>
        <li>エラー: {len([t for t in result.test_details if t['result'] == 'ERROR'])}</li>
    </ul>
"""

    # テストクラスごとにグループ化
    test_classes = {}
    for detail in result.test_details:
        class_name = detail['name'].split('.')[1]
        if class_name not in test_classes:
            test_classes[class_name] = []
        test_classes[class_name].append(detail)

    for class_name, tests in test_classes.items():
        html += f"<h2>{class_name}</h2>"
        for test in tests:
            test_name = test['name'].split('.')[-1]
            status_class = "success" if test['result'] == 'OK' else "failure"
            html += f"""
    <div class="test-case">
        <h3 class="{status_class}">{test_name}</h3>
        <div class="test-details">
            <p><strong>説明:</strong> {test['doc']}</p>
            <p><strong>結果:</strong> {test['result']}</p>
            <p><strong>実行時間:</strong> {test['time']:.3f}秒</p>
"""
            if test['result'] != 'OK':
                html += f"""
            <p><strong>エラー詳細:</strong></p>
            <pre>{test['error']}</pre>
"""
            html += """
        </div>
    </div>
"""

    html += """
</body>
</html>
"""
    return html

def run_tests_with_report():
    # テストスイートの作成
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])

    # テストの実行
    result = DetailedTestResult()
    runner = TextTestRunner(verbosity=2)
    suite.run(result)

    # レポートの生成
    markdown_report = generate_markdown_report(result)
    html_report = generate_html_report(result)

    # レポートの保存
    reports_dir = "test_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(f"{reports_dir}/test_report_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(markdown_report)
    
    with open(f"{reports_dir}/test_report_{timestamp}.html", "w", encoding="utf-8") as f:
        f.write(html_report)

    print(f"\nテストレポートが生成されました:")
    print(f"- Markdown: {reports_dir}/test_report_{timestamp}.md")
    print(f"- HTML: {reports_dir}/test_report_{timestamp}.html")

if __name__ == '__main__':
    run_tests_with_report() 