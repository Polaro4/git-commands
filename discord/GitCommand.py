import subprocess, os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="-",intents=discord.Intents.all(),application_id=int(os.getenv("BOT_ID")))

dir_paths = {'yagner': r'C:\Users\migue\codiguinhos\peiton\yagner'}

@bot.command(name='list_dirs', help='lista os diretórios disponíveis')
async def list_dirs(ctx):
    message = "Lista de diretórios:\n"
    for idx, name in enumerate(dir_paths.keys(), start=1):
        message += f"{idx}. {name}\n"
    await ctx.send(message)

@bot.command(name='git', help='executa comandos do git', aliases=['g', 'github'])
async def git_command(ctx, commando: str = None, dir_id: int = None):
    try:
        if commando is None:
            await ctx.send('Forneça um comando. Para mais informações, use o comando **-lgit**.')
            return

        if dir_id is None:
            await ctx.send('Por favor, forneça o ID do diretório. Para listar os diretórios disponíveis, use **-list_dirs**.')
            return

        dir_keys = list(dir_paths.keys())
        if 1 <= dir_id <= len(dir_keys):
            dir_path = dir_paths[dir_keys[dir_id - 1]]
            await ctx.send(f"Executando o comando '{commando}' no diretório '{dir_path}'")
        else:
            await ctx.send(f"ID '{dir_id}' não encontrado nos diretórios configurados.")
            return

        if not os.path.isdir(dir_path):
            await ctx.send(f"O diretório '{dir_path}' não é válido.")
            return

        commando = commando.split()
        result = subprocess.run(
            ['git'] + commando, 
            capture_output=True, 
            text=True, 
            check=True, 
            cwd=dir_path
        )
        await ctx.send(f'**Comando executado com sucesso:** \n {result.stdout}')
    except subprocess.CalledProcessError as e:
        await ctx.send(f'Erro ao executar o comando git: {e.stderr}')
    except Exception as e:
        await ctx.send(f'Ocorreu um erro: {e}')

        
@bot.command(name='lgit', help='lista alguns commandos do git', aliases=['listagit', 'githelp', 'hgit'])
async def lgit(ctx):
    await ctx.send('''\n
                   **Lista de Comandos Git**

1. **`git clone <URL>`**
   - Clona um repositório remoto para o diretório local.
   - Exemplo: `git clone https://github.com/usuario/repositorio.git`

2. **`git pull`**
   - Atualiza o repositório local com as alterações do repositório remoto. Combina `git fetch` e `git merge`.
   - Exemplo: `git pull origin main`

3. **`git fetch`**
   - Baixa as alterações do repositório remoto, mas não as mescla automaticamente.
   - Exemplo: `git fetch origin`

4. **`git status`**
   - Mostra o estado atual do diretório de trabalho e da área de stage.
   - Exemplo: `git status`

5. **`git add <arquivo>`**
   - Adiciona arquivos ao próximo commit.
   - Exemplo: `git add arquivo.txt` ou `git add .` para adicionar todas as alterações.

6. **`git commit -m "<mensagem>"`**
   - Cria um commit com uma mensagem descritiva.
   - Exemplo: `git commit -m "Adicionar novo recurso"`''')
    await ctx.send('''

7. **`git push`**
   - Envia os commits do repositório local para o repositório remoto.
   - Exemplo: `git push origin main`

8. **`git log`**
   - Exibe o histórico de commits.
   - Exemplo: `git log`

9. **`git branch`**
   - Lista as branches locais. Com opções adicionais, pode criar ou deletar branches.
   - Exemplo: `git branch` para listar, `git branch nome-da-branch` para criar, `git branch -d nome-da-branch` para deletar.

10. **`git checkout <branch>`**
    - Troca para outra branch.
    - Exemplo: `git checkout main` ou `git checkout -b nova-branch` para criar e trocar para uma nova branch.

11. **`git merge <branch>`**
    - Mescla a branch especificada na branch atual.
    - Exemplo: `git merge feature-branch`

12. **`git reset --hard <commit>`**
    - Reseta o diretório de trabalho para o estado do commit especificado, descartando todas as alterações.
    - Exemplo: `git reset --hard HEAD~1` para resetar ao commit anterior.

### Exemplos de Uso

- **Atualizar o repositório local com as alterações remotas:**
  ```sh
  git pull origin main
# Exemplo de uso: git status
output = git_command(['status'])
print(output)''')

bot.run(os.getenv('DISCORD_TOKEN'))