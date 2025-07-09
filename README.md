# 🛡️ SnapshotIM — Captura de Tela Antifraude

Aplicativo de captura de tela com marca d'água e proteção antifraude para uso corporativo. Criado para registrar **simulações diárias de taxas** e evitar edições ou manipulações não autorizadas.

---

## 🎯 Objetivo

O SnapshotIM foi desenvolvido para ambientes onde a **transparência em simulações de taxas e negociações** é essencial. A ferramenta garante que:

- A tela seja registrada **com integridade**.
- O conteúdo da **barra de tarefas** esteja sempre visível.
- A captura esteja associada ao **usuário do sistema** e **data/hora atual**.
- Nenhuma aplicação esteja em modo **tela cheia (F11)** durante a captura.

---

## ⚙️ Recursos

✅ Captura de todos os monitores conectados  
✅ Bloqueio automático se houver janela em tela cheia  
✅ Marca d’água vertical repetida com data, hora e usuário  
✅ Interface com botão único para facilitar o uso  
✅ Compatível com Windows 10+  
✅ Compilado em `.exe` (não requer Python instalado)

---

## 🖼️ Exemplo de marca d’água

A marca d’água é aplicada de forma vertical, com repetição, passando inclusive sobre a barra de tarefas, com o seguinte formato:

09-07-2025 15:32:10 | Usuário: fulano

---

## 🚀 Como usar

1. **Clique duas vezes** no executável `snapshotim.exe`.
2. Clique no botão `📸 Capturar Tela`.
3. Se nenhuma aplicação estiver em F11, a imagem será salva com marca d’água.

A captura será salva no mesmo diretório do executável, com nome como:

captura_fulano_09-07-2025 15-32-10.png

---

## 🔐 Segurança

- **Impossibilita capturas enquanto houver janelas fullscreen.**
- **Evita fraudes em prints manipulados** por esconder a janela da aplicação antes da captura.
- A marca d'água cobre **toda a imagem**, dificultando remoção por edição.

---

## 🛠️ Compilação do executável

### 1. Criar o ambiente virtual
```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual no Windows
```bash
venv\Scripts\activate
```

### 3. Instalar os pacotes listados no requirements.txt
```bash
pip install -r requirements.txt
```

### 4. Gerar o executável
```bash
pyinstaller --noconfirm --onefile --windowed --strip snapshotim.py
```

### 5. Resultado
O executável será gerado em:
dist/snapshotim.exe
