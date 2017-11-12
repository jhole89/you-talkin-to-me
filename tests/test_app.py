from main.app import run


def test_run(capfd):

    run()

    out, err = capfd.readouterr()

    assert out.splitlines()[-1] == "Me too"
