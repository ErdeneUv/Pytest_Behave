import logging
from csv import excel

from tests.utilities.final_url import extract_https

logger = logging.getLogger()


def url_assertion(expected, actual):
    print(f"URL_ASSERTION EXPECTED: {expected}\nACTUAL: {actual}\n\n")
    if expected is None or actual is None:
        raise AssertionError(
            f'either actual or expected is empty:\n actual: {actual}\nexpected: {expected}\n\n\n'
        )
    if ' ' in actual:
        try:
            actual = actual.split(' ')[0]
            print(f'SPACE ACTUAL after split: {actual}\n\n\n')
            assert expected in actual, f'Assert for links with space failed. actual: {actual}\nexpected: {expected}\n\n'
        except AssertionError as e:
            print(f'Assertion failed: {str(e)}\n extracting domain...\n\n')
            extracted_expected = extract_https(expected)
            extracted_actual = extract_https(actual)
            print(f'SPACE actual AFTER extracting domain: {extracted_actual}\n expected: {extracted_expected}\n\n')
            assert extracted_expected in extracted_actual, f"extracted domains. Assertion failed: Extracted_expected {extracted_expected} is NOT in Extracted_actual {extracted_actual}\n"
            print(f'Assertion after extraction succeeded! {extracted_expected} is in {extracted_actual}\n\n')
    else:
        try:
            assert expected in actual, f"Assertion failed: Excepted: {expected} is NOT in Actual: {actual},\n trying extraction of domain urls...\n\n"
        except AssertionError as e:
            #might want to use requests.get to get the url and assert if that fails, use finally block to use extract_https()
            print(f'Assertion failed: {str(e)}\n extracting domain...\n\n')
            extracted_expected = extract_https(expected)
            extracted_actual = extract_https(actual)

            assert extracted_expected in extracted_actual, f"extracted domains. Assertion failed: Extracted_expected {extracted_expected} is NOT in Extracted_actual {extracted_actual}\n\n\n"
            print(f'Assertion after extraction succeeded! {extracted_expected} is in {extracted_actual}\n\n\n')
