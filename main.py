import sqlite3
import hashlib
import time

class GerenciadorUsuario:
    def __init__(self, tabela):
        try:
            self.__conexao = sqlite3.connect('usuario.db')
            self.__cursor = self.__conexao.cursor()
            self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
            ''')
            self.__conexao.commit()

            self.dicionario = [            
            "@gmail.com", "@outlook.com", "@hotmail.com", "@live.com",
            "@yahoo.com", "@icloud.com", "@uol.com.br", "@bol.com.br",
            "@terra.com.br", "@ig.com.br", "@globo.com", "@empresa.com",
            "@empresa.com.br", "@negocio.com", "@startup.io", "@site.com",
            ".edu", ".edu.br"
            ]
        except sqlite3.Error:
            print('Deu algum bug no sistema...')
            return

    def colocando_informaçoes_tabela(self):    
        try:
            print('  cadastro selecionado')
            time.sleep(1)
            email = input('Digite seu email: ')
            time.sleep(1)

            if len(email) > 35:
                print('email muito longo')
                return
            elif len(email) < 6:
                print('email muito curto')
                return
            elif not email.endswith(tuple(self.dicionario)):
                print('email invalido')
                return
            else:
                print('email valido')

            senha = input('Digite sua senha: ')
            if len(senha) > 35:
                print('senha muito longa')
                return
            elif len(senha) < 6:
                print('senha muito curta')
                return

        except Exception:
            print('Deu algum bug...')
        else:
            try:
                print("senha valida")
                hash_final = hashlib.sha256(senha.encode()).hexdigest()

                self.__cursor.execute('''
                INSERT INTO usuarios (email, senha)
                VALUES (?, ?)
                ''', (email, hash_final))
                self.__conexao.commit()

                print('Usuário cadastrado com sucesso!')
            except sqlite3.IntegrityError:
                print('não pode colocar o mesmo email!')
            except Exception as e:
                print('Deu algum bug geral...')
                print(e)

    def login(self):
        try:
            print('login selecionado')
            time.sleep(1)

            email_cadastro = input('Digite seu email: ')
            if len(email_cadastro) > 35:
                print('email muito longo')
                return
            elif len(email_cadastro) < 6:
                print('email muito curto')
                return
            elif not email_cadastro.endswith(tuple(self.dicionario)):
                print('email invalido')
                return
            else:
                print('email valido')

            senha_cadastro = input('Digite sua senha: ')
            if len(senha_cadastro) > 35:
                print('senha muito longa')
                return
            elif len(senha_cadastro) < 6:
                print('senha muito curta')
                return  

            hash_login = hashlib.sha256(senha_cadastro.encode()).hexdigest()

            self.__cursor.execute(
                "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
                (email_cadastro, hash_login)
            )

            resultado = self.__cursor.fetchone()

            if resultado:
                print('confirmado, você entrou no sistema.')
            else:
                print('email ou senha incorretos.')

        except Exception as e:
            print('Deu algum bug...')
            print(e)

tabela = GerenciadorUsuario("usuarios")

chamando_funçoes = {
    1:tabela.login,
    2:tabela.colocando_informaçoes_tabela
}
tentativas = 5
while tentativas > 0:
    try:
        perguntas = int(input('  1 - Fazer login \n  2 - Fazer cadastro \n '))
        if perguntas in chamando_funçoes:
            chamando_funçoes[perguntas]()
        else:
            print('  é só a opcão 1 e 2.')
            tentativas -=1
    except ValueError:
        print('  É apenas números, não pode letras!!')
if tentativas == 0:
    print('  o maximo de tentativas é 5!')
