def pytest_addoption(parser):
    parser.addoption(
        "--functional",
        default=False,
        action="store_true",
        help="test against real server",
    )


def pytest_generate_tests(metafunc):
    if "functional" in metafunc.fixturenames:
        metafunc.parametrize("functional", [metafunc.config.getoption("functional")])
