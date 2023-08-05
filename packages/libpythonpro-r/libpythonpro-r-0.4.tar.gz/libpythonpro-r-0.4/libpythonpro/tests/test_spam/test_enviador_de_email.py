import pytest as pytest

from libpythonpro.spam.enviador_de_email import Enviador, EmailInvalido


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


@pytest.mark.parametrize(
    'destinatario',
    ['ricardo.vezetiv@mail.ru', 'foo@bar.com.br']
)
def test_remetente(destinatario):
    enviador = Enviador()
    resultado = enviador.enviar(
        destinatario,
        'ricardo.vezetiv@outlook.com',
        'Cursos Python Pro',
        'Aula Pytools no Módulo Framework Pytest.'
    )
    assert destinatario in resultado


@pytest.mark.parametrize(
    'destinatario',
    ['', 'foo']
)
def test_remetente_invalido(destinatario):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            destinatario,
            'ricardo.vezetiv@outlook.com',
            'Cursos Python Pro',
            'Aula Pytools no Módulo Framework Pytest.'
        )
