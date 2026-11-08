# Agente de briefing

Lê a mensagem que um possível cliente enviou pelo formulário do site e devolve um JSON com o tipo de negócio, a urgência, as perguntas que ainda faltam para o briefing e um rascunho de resposta.

Parte do projeto [MKLA Pixel](https://mklapixel.com.br), estúdio de sites para pequenos negócios que atendem clientes.

## O problema

Antes de contratar, o cliente costuma mandar uma mensagem curta e incompleta. Quem atende precisa ler, entender o negócio, avaliar a pressa e voltar com perguntas. O agente adianta essa primeira triagem.

## Como funciona

```
mensagem.txt  →  agente.py  →  JSON (tipo, urgência, perguntas, rascunho)
```

1. **Tipo de negócio:** procura palavras características (clínica, restaurante, salão, loja) em um dicionário.
2. **Urgência:** `alta` se aparece alguma expressão de pressa ("urgente", "o quanto antes"); caso contrário, `média`.
3. **Perguntas que faltam:** investimento, site ou rede social que a pessoa já tem e forma de contato. Só pergunta o que a mensagem ainda não respondeu.
4. **Rascunho de resposta:** montado a partir das perguntas, para uma pessoa revisar antes de enviar.

## Modo simulado

A função `claude_simulado` faz o papel de uma IA: devolve a resposta no mesmo formato que uma API de linguagem devolveria, mas usando as regras acima. O campo `origem` do JSON mostra `"simulado"`.

Foi uma escolha consciente: permite desenvolver e testar sem internet, sem chave de API e sem custo. A função `analisar` é a única porta de entrada do agente e tem uma chave `usar_api_real`. Para ligar um modelo de verdade, basta escrever uma função `claude_real` com o mesmo formato de retorno e chamá-la ali. O restante do programa não muda.

## Como rodar

Requer Python 3.9 ou mais novo. Não há dependências para instalar.

```bash
python agente.py mensagem.txt
```

Exemplo, com a mensagem "Tenho uma loja e quero um site urgente.":

```json
{
  "resumo": "Tenho uma loja e quero um site urgente.",
  "tipo_negocio": "loja",
  "urgencia": "alta",
  "perguntas_faltantes": [
    "Qual faixa de investimento você tem em mente?",
    "Você já tem site ou perfil em rede social?",
    "Como o cliente deve entrar em contato: WhatsApp, formulário ou agenda?"
  ],
  "rascunho_resposta": "Olá, obrigada pela mensagem. Para montar uma proposta que faça sentido, preciso entender alguns pontos: Qual faixa de investimento você tem em mente? Você já tem site ou perfil em rede social? Como o cliente deve entrar em contato: WhatsApp, formulário ou agenda? MKLA Pixel.",
  "origem": "simulado"
}
```

## Decisões de projeto

- **O agente sugere, não envia.** O rascunho passa por uma pessoa antes de chegar ao cliente.
- **Saída em JSON.** O formato permite ligar o agente à automação de novo contato (projeto `01-automacao-contato`), de modo que o cartão no Trello já nasça com resumo e urgência.
- **Serviço de IA separado do resto.** Trocar o simulado por um modelo real mexe em um ponto só.
- **Chaves fora do código.** Quando houver API real, a chave será lida de uma variável de ambiente, nunca escrita no repositório.

## Limites conhecidos

- A detecção por palavras-chave erra em mensagens fora do padrão. "Vendo bolo de pote" não bate em nenhuma palavra e cai em "não informado".
- Expressões como "tenho um site antigo" só são reconhecidas se estiverem na lista `JA_TEM_SITE`.
- Cada novo tipo de negócio exige editar o dicionário `TIPOS` à mão.

São justamente os pontos que um modelo de linguagem resolve, e por isso o próximo passo do projeto é a chamada real.

## O que aprendi construindo

Leitura de arquivos, funções, dicionários e listas, condicionais, saída em JSON e a ideia de simular um serviço externo para testar sem custo.

## Próximos passos

- Escrever `claude_real` e ativá-la quando houver chave de API.
- Receber a mensagem direto do formulário, sem arquivo de texto.
- Testes automatizados para as regras de tipo, urgência e perguntas.
