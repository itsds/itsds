<!-- Sky / Violet theme · generated to match DS_GitHub_Profile.html -->

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=230&color=0:38bdf8,50:a78bfa,100:f472b6&text=DURGA%20SHANKER&fontSize=54&fontColor=FFFFFF&fontAlignY=38&desc=Better%20Call%20DS&descAlignY=60&descSize=17&descColor=0B0F1A&animation=fadeIn" width="100%" alt="DURGA SHANKER · Better Call DS"/>
</p>

<p align="center">
  <a href="https://github.com/itsds">
    <img src="https://readme-typing-svg.demolab.com?font=IBM+Plex+Mono&weight=500&size=20&duration=2800&pause=1200&color=38BDF8&center=true&vCenter=true&width=620&lines=Staff+Data+Engineer+%7C+AI+Platform+Engineer;Batch+%26+Streaming+Pipelines+at+Scale;PySpark+%C2%B7+Kafka+%C2%B7+AWS+%C2%B7+Snowflake;LangGraph+Multi-Agent+Systems+%C2%B7+RAG" alt="Staff Data Engineer | AI Platform Engineer · Batch &amp; Streaming Pipelines at Scale · PySpark · Kafka · AWS · Snowflake · LangGraph Multi-Agent Systems · RAG"/>
  </a>
</p>

<p align="center">
  <b>11.5 years</b> building production systems — from backend services to large-scale data pipelines to autonomous AI agents.
</p>

<p align="center">
  <a href="https://linkedin.com/in/itsds"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://itsds.github.io"><img height="30" src="https://img.shields.io/badge/Portfolio-F472B6?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio"/></a>
  <a href="mailto:itisds.ai@gmail.com"><img height="30" src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
</p>

<p align="center">
  <img height="22" src="https://komarev.com/ghpvc/?username=itsds&style=for-the-badge&label=PROFILE+VIEWS&labelColor=0284C7&color=38BDF8" alt="Profile views"/>
  <a href="https://github.com/itsds?tab=followers"><img height="22" src="https://img.shields.io/github/followers/itsds?style=for-the-badge&logo=github&logoColor=white&label=FOLLOWERS&labelColor=7C3AED&color=A78BFA" alt="Followers"/></a>
  <a href="https://github.com/itsds?tab=repositories"><img height="22" src="https://img.shields.io/github/stars/itsds?style=for-the-badge&logo=github&logoColor=white&label=STARS&affiliations=OWNER&labelColor=DB2777&color=F472B6" alt="Stars"/></a>
</p>

## 🧭 About Me

Staff Data Engineer with **11.5 years** across three domains — currently at **Visa**, building enterprise-grade pipelines and autonomous AI agent platforms.

| Years | Domain | Focus |
|:---:|---|---|
| **4.5** | **Backend** | Java microservices, Spring Boot, distributed systems |
| **6.5+** | **Data Engineering** | Spark, Kafka, Iceberg, Snowflake — batch &amp; streaming at scale |
| **1+** | **AI Engineering** | LangGraph agents, RAG, LLM orchestration *(overlaps DE)* |

Drawn to the intersection where **data engineering meets AI** — building the infrastructure, retrieval layers, and production scaffolding that make AI agents reliable and observable.

## 🔥 What I'm Building

### 🏷️ [TTAG Pipeline](https://github.com/itsds/ttag-pipeline) &nbsp;`PRIVATE`

*End-to-end batch pipeline deriving cardholder travel signals to improve authorization accuracy and reduce false declines.*

- **Two-lane ingestion** — Booking files (HDFS) + Benefit stream (Kafka + Schema Registry)
- **Bronze → Silver → Gold** medallion on Iceberg with Hive Metastore
- Incremental loading via **Iceberg snapshot-based reads** with watermark control tables
- Idempotent **MERGE INTO** writes on natural keys at every layer
- **4-gate Airflow DAG** — schema validation, row-count checks, cross-lane reconciliation
- Gold **star schema** on Snowflake — Type 2 SCD dimensions, temporal FK lookups

`PySpark` `Iceberg` `Kafka` `Snowflake` `Airflow` `HDFS` `Great Expectations`

### 👁️ [Argus — Diagnostic Agents](https://github.com/itsds/argus)

*Four AI agents watching different failure surfaces of TTAG — named after the hundred-eyed watchman.*

| Agent | What It Does |
|---|---|
| **Recon Diagnostics** | Traces row-count mismatches, duplicate keys, NULL FK joins, watermark gaps |
| **DLQ Triage** | Classifies DLQ records, auto-requeues transients, escalates with context |
| **Backfill Planning** | Queries watermarks + Iceberg snapshots → safe backfill plan with HITL approval |
| **Spark Debugger** | Analyzes SparkUI metrics, execution plans → surfaces skew, spills, GC issues |

- Each agent: **LangGraph StateGraph** with typed Pydantic state + structured output
- Multi-trigger: Airflow `on_failure_callback` · CLI · REST API
- P1 → PagerDuty · P2 → Slack · P3 → log only

`LangGraph` `LangChain` `Gemini` `FastAPI` `Python`

### 📈 [DSView — Real-Time Crypto](https://github.com/itsds/dsview)

*Real-time BTC-USD pipeline replicating TradingView premium — from exchange WebSocket ticks to a live candlestick dashboard.*

- **Binance WebSocket → Redpanda** for live ingestion
- **Spark Structured Streaming** → windowed aggregations → Iceberg tables
- **FastAPI** backend + **React** frontend with TradingView's `lightweight-charts`
- Redis pub/sub for real-time WebSocket push to clients

`Spark Streaming` `Redpanda` `Iceberg` `Redis` `FastAPI` `React`

### 🤖 Aura AI 2.0 — Autonomous SWE Platform &nbsp;`VISA · INTERNAL`

*Multi-agent platform that turns a Jira ticket into a reviewed pull request — autonomously.*

- **9 specialized agents** orchestrated via Spring Boot event router
- **Graph-RAG**: Neo4j code graph + PGVector semantic + BM25 — cross-encoder reranked
- **LangGraph** workflows with PostgreSQL-backed crash recovery checkpoints
- **Episodic + Procedural memory** — cross-repo learning from merged PRs
- **Deterministic Execution Engine** — SHA-256 fingerprinting + LLM cache + replay API

`LangGraph` `Spring Boot` `Java 17` `Neo4j` `PGVector` `Claude/GPT` `K8s`

## 🛠️ Tech Stack

**Languages**

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java"/>
  <img src="https://img.shields.io/badge/SQL-336791?style=flat-square" alt="SQL"/>
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="Bash"/>
</p>

**Data Engineering**

<p>
  <img src="https://img.shields.io/badge/Spark-E25A1C?style=flat-square&logo=apachespark&logoColor=white" alt="Spark"/>
  <img src="https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white" alt="Kafka"/>
  <img src="https://img.shields.io/badge/Iceberg-4E9BCD?style=flat-square" alt="Iceberg"/>
  <img src="https://img.shields.io/badge/Snowflake-29B5E8?style=flat-square&logo=snowflake&logoColor=white" alt="Snowflake"/>
  <img src="https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" alt="Airflow"/>
  <img src="https://img.shields.io/badge/Delta%20Lake-003366?style=flat-square" alt="Delta Lake"/>
  <img src="https://img.shields.io/badge/Redpanda-DC382D?style=flat-square" alt="Redpanda"/>
  <img src="https://img.shields.io/badge/dbt-FF694B?style=flat-square&logo=dbt&logoColor=white" alt="dbt"/>
  <img src="https://img.shields.io/badge/Hive-C9A800?style=flat-square&logo=apachehive&logoColor=white" alt="Hive"/>
  <img src="https://img.shields.io/badge/Great%20Expectations-FF6F00?style=flat-square" alt="Great Expectations"/>
</p>

**AI &amp; Agents**

<p>
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Claude-D4A574?style=flat-square&logo=anthropic&logoColor=white" alt="Claude"/>
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/RAG-FF4500?style=flat-square" alt="RAG"/>
  <img src="https://img.shields.io/badge/LangSmith-1C3C3C?style=flat-square" alt="LangSmith"/>
</p>

**Backend &amp; Databases**

<p>
  <img src="https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" alt="Spring Boot"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Neo4j-4581C3?style=flat-square&logo=neo4j&logoColor=white" alt="Neo4j"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic"/>
</p>

**DevOps &amp; Infra**

<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes"/>
  <img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" alt="Terraform"/>
  <img src="https://img.shields.io/badge/AWS-FF9900?style=flat-square" alt="AWS"/>
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions"/>
  <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana"/>
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus"/>
</p>

## 📊 Career Journey

| Company | Role | Years | Focus |
|---|---|:---:|---|
| **HCL Technologies** | Sr. Software Engineer | 2014 – 2017 | Backend |
| **Infosys** | Sr. Systems Engineer | 2017 – 2019 | Backend + DE |
| **SanDisk / WD** | Staff Data Engineer | 2019 – 2023 | Data Engineering |
| **Visa** | Staff Data Engineer | 2023 – Present | DE + AI |

## 📈 GitHub Analytics

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=itsds&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&bg_color=171d30&title_color=38bdf8&icon_color=a78bfa&text_color=e2e8f0"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api?username=itsds&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&bg_color=ffffff&title_color=0284c7&icon_color=7c3aed&text_color=1e293b"/>
    <img alt="GitHub statistics" src="https://github-readme-stats.vercel.app/api?username=itsds&show_icons=true&include_all_commits=true&count_private=true&hide_border=true&bg_color=171d30&title_color=38bdf8&icon_color=a78bfa&text_color=e2e8f0" height="170"/>
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=itsds&layout=compact&langs_count=8&hide_border=true&bg_color=171d30&title_color=38bdf8&text_color=e2e8f0"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=itsds&layout=compact&langs_count=8&hide_border=true&bg_color=ffffff&title_color=0284c7&text_color=1e293b"/>
    <img alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=itsds&layout=compact&langs_count=8&hide_border=true&bg_color=171d30&title_color=38bdf8&text_color=e2e8f0" height="170"/>
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=itsds&hide_border=true&background=171d30&stroke=2a3350&ring=a78bfa&fire=f472b6&currStreakLabel=38bdf8&sideLabels=38bdf8&currStreakNum=f1f5f9&sideNums=f1f5f9&dates=8892a8"/>
    <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com/?user=itsds&hide_border=true&background=ffffff&stroke=e2e8f0&ring=7c3aed&fire=db2777&currStreakLabel=0284c7&sideLabels=0284c7&currStreakNum=0f172a&sideNums=0f172a&dates=64748b"/>
    <img alt="GitHub streak" src="https://streak-stats.demolab.com/?user=itsds&hide_border=true&background=171d30&stroke=2a3350&ring=a78bfa&fire=f472b6&currStreakLabel=38bdf8&sideLabels=38bdf8&currStreakNum=f1f5f9&sideNums=f1f5f9&dates=8892a8"/>
  </picture>
</p>

## 🏆 GitHub Trophies

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-trophy.vercel.app/?username=itsds&no-frame=true&no-bg=true&margin-w=8&column=-1&theme=darkhub"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-profile-trophy.vercel.app/?username=itsds&no-frame=true&no-bg=true&margin-w=8&column=-1&theme=flat"/>
    <img alt="GitHub trophies" src="https://github-profile-trophy.vercel.app/?username=itsds&no-frame=true&no-bg=true&margin-w=8&column=-1&theme=darkhub"/>
  </picture>
</p>

## 📉 Contribution Activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=itsds&area=true&hide_border=true&custom_title=Contribution%20Activity&bg_color=171d30&color=e2e8f0&title_color=38bdf8&line=38bdf8&point=f472b6&area_color=a78bfa"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=itsds&area=true&hide_border=true&custom_title=Contribution%20Activity&bg_color=ffffff&color=1e293b&title_color=0284c7&line=0284c7&point=db2777&area_color=c4b5fd"/>
    <img alt="Contribution activity graph" src="https://github-readme-activity-graph.vercel.app/graph?username=itsds&area=true&hide_border=true&custom_title=Contribution%20Activity&bg_color=171d30&color=e2e8f0&title_color=38bdf8&line=38bdf8&point=f472b6&area_color=a78bfa" width="100%"/>
  </picture>
</p>

## 🐍 Contribution Snake

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/itsds/itsds/output/github-snake-dark.svg"/>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/itsds/itsds/output/github-snake.svg"/>
    <img alt="Contribution snake eating the commit grid" src="https://raw.githubusercontent.com/itsds/itsds/output/github-snake-dark.svg"/>
  </picture>
</p>

## 🤝 Let's Connect

Open to conversations about **data engineering architecture**, **AI agent systems**, and **production-grade pipelines**.

<p align="center">
  <code>Staff / Principal Engineering</code> · <code>AI Engineering</code> · <code>Agentic AI</code> · <code>Data Platforms</code> · <code>Backend &amp; Distributed Systems</code> · <code>Platform Engineering</code>
</p>

<p align="center">
  <a href="https://linkedin.com/in/itsds"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://itsds.github.io"><img height="30" src="https://img.shields.io/badge/Portfolio-F472B6?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Portfolio"/></a>
  <a href="mailto:itisds.ai@gmail.com"><img height="30" src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="https://github.com/itsds"><img height="30" src="https://img.shields.io/badge/GitHub-24292F?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
</p>

<p align="center"><i>⚡ Built with purpose — pipelines that move data, agents that fix themselves.</i></p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=130&section=footer&color=0:38bdf8,50:a78bfa,100:f472b6&animation=fadeIn" width="100%" alt=""/>
</p>
