# AI-RA (Intelligent Life Copilot)

> **AI-RA** é um copiloto inteligente e adaptativo de vida pessoal, acadêmica e financeira, projetado para orientar o usuário em direção a objetivos ambiciosos de longo prazo (como a compra do primeiro imóvel e a aceleração profissional) ajustando a rotina em tempo real aos níveis de energia, tempo e orçamento disponíveis.

---

##  Visão do Produto

Ao contrário de gerenciadores de hábitos rígidos ou chatbots genéricos, a **AI-RA** opera como uma **máquina de estados adaptativa**. Se o usuário passa por um imprevisto financeiro ou uma semana de estafa, o sistema não gera cobrança desnecessária: ele transiciona para o modo de recuperação, protege os hábitos biológicos essenciais e recalibra os prazos e orçamentos automaticamente.

### Pilares Centrais
1. **Engenharia de Prompt Dinâmica:** O comportamento do modelo varia de acordo com o momento do usuário através de roteamento por modos (`RECUPERAÇÃO`, `MANUTENÇÃO`, `FOCO_TOTAL`, `ACELERAÇÃO`).
2. **Memória de Estado Estruturada (State-Driven Context):** Armazenamento em JSON/banco de dados das metas ativas, saldo acumulado, gargalos de tempo e restrições.
3. **Foco em Resultados Concretos:** Engenharia reversa de metas (ex.: cálculo de aporte mensal necessário para entrada de apartamento e planejamento de portfólio profissional).

---

##  Identidade Visual e UI/UX

A interface foi concebida com estética limpa, moderna e acolhedora, combinando tons suaves de rosa com microinterações fluidas e ícones elegantes.

* **Paleta Principal:**
  * **Primary (Rosa Principal):** `#EC4899` (Pink 500) / `#F43F5E` (Rose 500)
  * **Primary Soft (Fundo e Destaques Suaves):** `#FDF2F8` (Pink 50) / `#FCE7F3` (Pink 100)
  * **Accent / Glow:** `#FB7185` (Rose 400)
  * **Dark Mode Base:** `#1E1523` (Dark Plum) com acentos em `#F472B6`
* **Estilo Visual:** Bordas arredondadas (`rounded-2xl`), glassmorphism sutil, tipografia moderna (Inter ou Outfit) e indicadores de progresso visuais.
* **Ícone / Mascote:** Símbolo estilizado integrando uma centelha de inteligência artificial (`sparkle`) e pétalas florais/aura geométrica rosa minimalista.

---

##  Arquitetura do Sistema

```
┌────────────────────────────────┐
│      Frontend (Angular 17+)    │
│  - Dashboard de Métricas       │
│  - Chat Interativo em Tempo Real│
│  - Indicadores de Modo e Metas │
└───────────────▲────────────────┘
                │ HTTP / REST / WebSocket
┌───────────────▼────────────────┐
│      Backend (Python / FastAPI)│
│  - Gestão de Estados e Memória │
│  - Pipeline de Prompt Dinâmico │
│  - Integração com Groq Cloud   │
└───────────────▲────────────────┘
                │
     ┌──────────┴──────────┐
     ▼                     ▼
┌───────────────┐   ┌───────────────────────────┐
│ Banco de Dados│   │  Groq API (Llama 3 / Mixtral)│
│ (PostgreSQL/  │   │  - Respostas ultra-rápidas│
│ SQLite Local) │   │  - Processamento do prompt│
└───────────────┘   └───────────────────────────┘
```

---

##  Engenharia de Prompt e Gestão de Memória

### 1. O Estado do Usuário (`user_state`)
A cada interação com a API Groq, o backend concatena o histórico recente ao estado atual serializado em JSON:

```json
{
  "profile": {
    "name": "Usuário",
    "anchors": ["Treino regular", "Sono 7h+", "Reunião de metas"]
  },
  "current_state": {
    "energy_level": "baixa | media | alta",
    "financial_status": "apertado | estavel | superavit",
    "operational_mode": "RECUPERACAO | MANUTENCAO | FOCO_TOTAL | ACELERACAO"
  },
  "primary_goals": {
    "financial": {
      "target": "Entrada do apartamento",
      "target_value": 70000,
      "current_saved": 8500,
      "monthly_target_savings": 1500
    },
    "career": {
      "target": "Aumento de renda / Destaque técnico",
      "current_bottleneck": "Tempo para entregas de alto impacto"
    }
  }
}
```

### 2. Modos de Operação da IA
* **Recuperação:** Reduz tarefas complementares a zero; foca em descanso e proteção orçamentária contra imprevistos.
* **Manutenção:** Exige apenas o mínimo diário essencial sem novas iniciativas pesadas.
* **Foco Total:** Ritmo padrão de alto rendimento, verificação de gastos e cumprimento de blocos de estudo/trabalho.
* **Aceleração:** Sprints intencionais de produtividade técnica e aportes extras.

---

##  Stack Tecnológica

* **Frontend:**
  * **Framework:** [Angular](https://angular.io/) (Standalone Components, Signals para reatividade)
  * **Estilização:** Tailwind CSS (tema customizado rosa/rose) + Lucide Icons / Heroicons
  * **Componentes:** Angular CDK / Radix-style primitives
* **Backend:**
  * **Linguagem:** Python 3.11+
  * **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (alta performance e geração automática de OpenAPI Docs)
  * **Validação:** Pydantic V2
  * **ORM / Banco:** SQLAlchemy ou SQLModel com SQLite (desenvolvimento) / PostgreSQL (produção)
* **Motor de IA:**
  * **Provedor:** [Groq Cloud SDK](https://console.groq.com/)
  * **Modelos recomendados:** `llama-3.3-70b-versatile` ou `mixtral-8x7b-32768` (latência extremamente baixa para experiência fluida)

---

## Como Executar o Projeto Localmente

### Pré-requisitos
* Node.js 18+ e Angular CLI (`npm install -g @angular/cli`)
* Python 3.11+
* Chave de API da [Groq Cloud](https://console.groq.com/keys)

---

### 1. Configurando o Backend (Python / FastAPI)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ai-ra.git
cd ai-ra/backend

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install fastapi uvicorn groq pydantic python-dotenv sqlalchemy

# Configure as variáveis de ambiente
cp .env.example .env
# Adicione sua GROQ_API_KEY no arquivo .env

# Inicie o servidor FastAPI
uvicorn main:app --reload --port 8000
```

---

### 2. Configurando o Frontend (Angular)

```bash
cd ../frontend

# Instale os pacotes npm
npm install

# Inicie o servidor de desenvolvimento
ng serve --open
```

O frontend estará disponível em `http://localhost:4200` e a documentação interativa da API (Swagger) em `http://localhost:8000/docs`.

---

## 🗺️ Roadmap do MVP

- [x] Definição de identidade visual e modelo de persona da AI-RA.
- [x] Especificação da arquitetura de estados e prompt dinâmico.
- [ ] Implementação da API FastAPI com endpoint de chat com streaming via Groq.
- [ ] Modelagem do banco de dados para histórico e perfil de metas do usuário.
- [ ] Interface Angular com chat responsivo, tema em tons de rosa e cards de métricas.
- [ ] Módulo financeiro de acompanhamento da entrada do apartamento com gráficos de progresso.

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte `LICENSE` para obter mais informações.
