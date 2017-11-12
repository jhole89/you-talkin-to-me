from main.app import run


def test_run(capfd):

    run(train=False)

    out, err = capfd.readouterr()

    assert out.splitlines()[-1] == 'I am sorry, I don\'t understand right now'
