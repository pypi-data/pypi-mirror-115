from libpythonpro.spam.modelos import Usuario


def test_salvar_usuario(sessao):
    usuario = Usuario(nome='Ricardo', email='ricardo.vezetiv@mail.ru')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)


def test_listar_usuario(sessao):
    usuarios = [
        Usuario(nome='Ricardo', email='ricardo.vezetiv@mail.ru'),
        Usuario(nome='Theodoro', email='theodoro.vezetiv@mail.ru')
    ]
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
