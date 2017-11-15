from app.controllers import create_chatbot


def test_create_chatbot(capfd):

    name = 'Testy McTesterson'

    chatbot = create_chatbot(name)

    out, err = capfd.readouterr()

    assert out.splitlines()[-1].split()[-1] == '100%'
    assert chatbot.name == name
