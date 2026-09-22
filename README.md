# 💰 Grana — Assistente Virtual de Educação Financeira

> Projeto desenvolvido para o desafio da **DIO**: [Construa Seu Assistente Virtual Com Inteligência Artificial](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).

![Tema](https://img.shields.io/badge/tema-Educação%20Financeira-green)
![Stack](https://img.shields.io/badge/stack-Python%20%2B%20Streamlit%20%2B%20Gemini-blue)
![Status](https://img.shields.io/badge/status-protótipo%20funcional-success)

## Sobre o projeto

**Grana** é um assistente virtual que ajuda uma pessoa a entender melhor os próprios hábitos financeiros e a aprender conceitos de educação financeira do dia a dia — sem jargão, sem julgamento e sem inventar informação que não tem.

Ele responde com base em três fontes de dados fictícias: um histórico de transações, um perfil de usuário e um conjunto de metas financeiras. Quando a pergunta foge do que os dados cobrem — ou pede recomendação de investimento específico — ele diz isso com clareza, em vez de "chutar" uma resposta.

## Estrutura do repositório

```
assistente-virtual-educacao-financeira/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── transacoes.csv
│   ├── perfil_usuario.json
│   ├── metas_financeiras.json
│   └── glossario_financeiro.json
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
└── src/
    └── app.py
```

## As 6 entregas do desafio

| # | Entrega | Onde está |
|---|---------|-----------|
| 1 | Documentação do agente | [`docs/01-documentacao-agente.md`](docs/01-documentacao-agente.md) |
| 2 | Base de conhecimento | [`docs/02-base-conhecimento.md`](docs/02-base-conhecimento.md) + [`data/`](data/) |
| 3 | Prompts do agente | [`docs/03-prompts.md`](docs/03-prompts.md) |
| 4 | Aplicação funcional | [`src/app.py`](src/app.py) |
| 5 | Avaliação e métricas | [`docs/04-metricas.md`](docs/04-metricas.md) |
| 6 | Pitch | [`docs/05-pitch.md`](docs/05-pitch.md) |

## Como rodar localmente

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/SEU-USUARIO/assistente-virtual-educacao-financeira.git
   cd assistente-virtual-educacao-financeira
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # Mac/Linux
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e cole sua chave gratuita da [API do Google Gemini](https://aistudio.google.com/app/apikey):
   ```bash
   copy .env.example .env        # Windows
   # cp .env.example .env        # Mac/Linux
   ```

4. Rode a aplicação:
   ```bash
   streamlit run src/app.py
   ```

5. Acesse `http://localhost:8501` no navegador e converse com o Grana.

> ⚠️ Todos os dados em `data/` são **fictícios**, criados só para este protótipo. Nenhum dado financeiro real é usado.

## Ferramentas usadas

- **Python + Streamlit** — interface de chat
- **Google Gemini API** (`gemini-1.5-flash`) — modelo de linguagem, plano gratuito
- **python-dotenv** — gestão da chave de API fora do código

## Créditos

Desafio original: [DIO — Digital Innovation One](https://www.dio.me). Repositório base: [`digitalinnovationone/dio-lab-bia-do-futuro`](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).
