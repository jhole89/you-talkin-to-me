from app.controllers import create_chatbot, process_quotes


def test_create_chatbot(capfd):
    """
    Test case for app.controllers.create_chatbot
    :param capfd: pytest fixture for capturing stdout/stderr
    :return: None
    """

    name = 'Testy McTesterson'

    chatbot = create_chatbot(name)

    out, err = capfd.readouterr()

    assert out.splitlines()[-1].split()[-1] == '100%'
    assert chatbot.name == name


def test_process_quotes():
    """
    Test case for app.controllers.process_quotes
    :return: None
    """

    conversations = process_quotes(
        static_file='moviequotes.scripts.txt.gz',
        delimiter='+++$+++'
    )

    assert type(conversations) == list
    assert len(conversations) == 393758
