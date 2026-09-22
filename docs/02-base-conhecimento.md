# 📚 Base de Conhecimento

Todos os dados abaixo são **fictícios**, criados especificamente para este protótipo — nenhum dado financeiro real é usado em nenhuma etapa.

## Arquivos

| Arquivo | Formato | O que contém |
|---|---|---|
| `data/transacoes.csv` | CSV | Histórico de transações fictícias (data, categoria, descrição, valor, tipo) cobrindo dois meses |
| `data/perfil_usuario.json` | JSON | Perfil resumido: profissão, renda mensal estimada, nível de conhecimento financeiro, objetivo principal |
| `data/metas_financeiras.json` | JSON | Metas de economia em andamento, com valor alvo, valor atual e prazo |
| `data/glossario_financeiro.json` | JSON | Pequeno glossário de termos financeiros, usado para grounding nas explicações de conceito |

## Por que essa estrutura

- **CSV para transações:** é o formato mais natural para dado tabular e repetitivo, e fica fácil de filtrar por categoria ou período.
- **JSON para perfil e metas:** são poucos registros, com estrutura aninhada (ex: cada meta tem valor alvo *e* valor atual *e* prazo), então JSON é mais legível que forçar isso em colunas de CSV.
- **Glossário separado:** em vez de deixar o modelo "lembrar" definições de conceitos financeiros por conta própria (risco de alucinação), o glossário garante que toda explicação de termo citada pelo agente vem de uma fonte fixa e auditável.

## Como o app usa esses dados

O `src/app.py` carrega os quatro arquivos uma vez (com cache do Streamlit) e, a cada pergunta, decide por palavra-chave qual subconjunto de dado é relevante:

- Pergunta menciona "gastei", "compra", "categoria" → inclui as transações recentes no contexto
- Pergunta menciona "meta", "economizar", "reserva" → inclui as metas financeiras
- Pergunta contém algum termo do glossário → inclui a definição correspondente
- Em qualquer caso, o perfil do usuário sempre entra no contexto (é pequeno e dá personalização básica)

Essa é uma retrieval simples baseada em regra, não uma busca vetorial — suficiente para o escopo do protótipo, e listada como possível evolução na seção de próximos passos do pitch.

## Como expandir

Para ir além do MVP, os próximos candidatos naturais a entrar em `data/` seriam um histórico de conversas anteriores (para dar continuidade entre sessões) e um conjunto maior de perguntas frequentes de educação financeira, já formatado como pares pergunta/resposta para few-shot.
