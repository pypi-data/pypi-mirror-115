import re
import logging

class Validations:
    def __init__(self) -> None:
        self.regex_list = [
            r'ADHOC-10.\d*.\d*.\d*',
            r'ADHOC-\d{1,2}.\d{1,2}.\d{1,3}.\d{1,4}'
        ]
        self.match = []

    def check_artifact_string(self, arg: str) -> str:
        logging.info("Validations/check_artifact_string()")
        for i in self.regex_list:
            self.match.append(bool(re.compile(i).match(str(arg))))
        if True in self.match:
            logging.info("Validation Cleared: Artifact name in standrds")
            return True
        else:
            logging.info("Validation Cleared: Artifact name in standrds")
            return False

    def get_correct_artifact_name(self, arg):
        logging.info("Validations/get_correct_artifact_name")
        if '.tar.gz' in arg:
            logging.info("Validation cleared .tar.gz removed")
            return arg.strip('.tar.gz')
        elif '.tar' in arg:
            logging.info("Validation cleared .tar removed")
            return arg.strip('.tar')
        elif '.tgz' in arg:
            logging.info("Validation cleared .tgz removed")
            return arg.strip('.tgz')
        else:
            logging.info(f"Validation supress: {arg}")
            return arg

    def return_artifact_name(self, arg):
        logging.info("Validations/return_artifact_name")
        return '.'.join([self.get_correct_artifact_name(arg), 'tar.gz'])

    def get_version_name(self, arg) -> str:
        logging.info("Validations/get_version_name")
        return re.findall(r'\d+.\d+.\d+.\d+', arg)[0]
