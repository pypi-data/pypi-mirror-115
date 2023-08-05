from unittest.mock import Mock

import pytest

from libpythonpro.spam.main import EnviadorDeSpam
from libpythonpro.spam.modelos import Usuario


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Ricardo', email='ricardo.vezetiv@mail.ru'),
            Usuario(nome='Theodoro', email='theodoro.vezetiv@mail.ru')
        ],
        [
            Usuario(nome='Ricardo', email='ricardo.vezetiv@mail.ru')
        ]
    ]
)
def test_qde_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'ricardo.vezetiv@mail.ru',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    assert len(usuarios) == enviador.enviar.call_count


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Ricardo', email='ricardo.vezetiv@mail.ru')
    sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'theodoro.vezetiv@mail.ru',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    enviador.enviar.assert_called_once_with(
        'theodoro.vezetiv@mail.ru',
        'ricardo.vezetiv@mail.ru',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
