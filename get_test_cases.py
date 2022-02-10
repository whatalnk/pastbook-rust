import argparse
import urllib.request
from html.parser import HTMLParser


header = """use cli_test_dir::*;

const BIN: &'static str = "./hello";"""

test_case_template = """
#[test]
fn sample{test_case_number}() {{
    let testdir = TestDir::new(BIN, "");
    let output = testdir
        .cmd()
        .output_with_stdin(
            r#"{sample_input}
            "#,
        )
        .tee_output()
        .expect_success();
    assert_eq!(output.stdout_str(), "{sample_output}\\n");
    assert!(output.stderr_str().is_empty());
}}"""


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h3_flag = False
        self.input_flag = False
        self.output_flag = False
        self.pre_flag = False
        self.sample_inputs = []
        self.sample_outputs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            self.h3_flag = True

        if (self.input_flag or self.output_flag) and tag == 'pre':
            self.pre_flag = True

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.h3_flag and '入力例' in data:
            self.input_flag = True
            self.h3_flag = False
        elif self.h3_flag and '出力例' in data:
            self.output_flag = True
            self.h3_flag = False

        if self.pre_flag:
            if self.input_flag:
                self.sample_inputs.append(data.rstrip())
            elif self.output_flag:
                self.sample_outputs.append(data.rstrip())
            self.pre_flag = False
            self.input_flag = False
            self.output_flag = False

    def handle_startendtag(self, tag, attrs):
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    with urllib.request.urlopen(args.url) as f:
        resp = f.read().decode('utf-8')
        html_parser = MyHTMLParser()
        html_parser.feed(resp)
        print(header)
        for n, (i, o) in enumerate(zip(html_parser.sample_inputs, html_parser.sample_outputs)):
            params = dict(test_case_number=n + 1,
                          sample_input=i, sample_output=o)
            print(test_case_template.format(**params))
