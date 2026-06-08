# 🤖 Ollama Local LLM Configuration for DAIOF

**Framework**: HYPERAI | **K-State**: 1  
**Creator**: Nguyễn Đức Cường (alpha_prime_omega)  
**Verification**: 4287

---

## 🎯 Tổng quan

Tất cả AI services trong DAIOF Framework sử dụng **Ollama local LLM** thay vì OpenAI/Anthropic API:

- **Base URL**: `http://localhost:11434`
- **Model**: `dandr-llama2:latest` (D&R Protocol optimized)
- **Mode**: D&R Protocol (Deconstruction → Focal Point → Re-architecture)

---

## 🚀 Khởi động Ollama

```bash
# Start Ollama server
ollama serve

# Verify running
curl http://localhost:11434/api/tags

# Pull D&R optimized model
ollama pull dandr-llama2:latest
```

---

## 📚 Sử dụng trong Python

### 1. Simple Text Generation

```python
from ollama_config import generate_text

response = generate_text("Explain Docker for AI")
print(response)
```

### 2. Chat Completion (OpenAI-compatible)

```python
from ollama_config import chat_completion

response = chat_completion([
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What is DAIOF Framework?"}
])
print(response)
```

### 3. D&R Protocol Analysis

```python
from ollama_config import dandr_solve

solution = dandr_solve("How to optimize autonomous security fixes?")

print("📊 Deconstruction:", solution['deconstruction'])
print("🎯 Focal Point:", solution['focal_point'])
print("🏗️ Re-architecture:", solution['rearchitecture'])
```

---

## 🔧 Tích hợp vào DAIOF Services

### Autonomous Git Workflow

```python
# .github/scripts/autonomous_git_workflow.py
from ollama_config import setup_environment, dandr_solve

# Setup Ollama
setup_environment()

# Use D&R Protocol for decision making
problem = "Should we merge this PR?"
solution = dandr_solve(problem)

# Use solution['rearchitecture'] for final decision
```

### HAIOS Monitor

```python
# haios_monitor.py
from ollama_config import get_ollama_client

client = get_ollama_client()

# Analyze health metrics
health_analysis = client.generate(
    prompt=f"Analyze health metrics: {metrics}",
    system="You are a system health expert."
)
```

### Real-time Task Generator

```python
# .github/scripts/realtime_task_generator.py
from ollama_config import chat_completion

# Generate intelligent tasks
messages = [
    {"role": "system", "content": "You are a task generation expert."},
    {"role": "user", "content": f"Generate tasks for: {context}"}
]

tasks = chat_completion(messages)
```

---

## 🐳 Docker Integration

### docker-compose.yml

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-server
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    restart: unless-stopped
    environment:
      - OLLAMA_MODELS=dandr-llama2:latest

  hyperai-orchestrator:
    build: .
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - OLLAMA_MODEL=dandr-llama2:latest
      - DANDR_MODE=enabled

volumes:
  ollama-data:
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Ollama client dependencies
RUN pip install requests

# Copy Ollama config
COPY ollama_config.py .

# Setup environment
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV OLLAMA_MODEL=dandr-llama2:latest
ENV USE_LOCAL_LLM=true
ENV DANDR_MODE=enabled

# Disable external APIs
ENV OPENAI_API_KEY=""
ENV ANTHROPIC_API_KEY=""

CMD ["python3", "ollama_config.py"]
```

---

## 🧬 D&R Protocol Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Problem Input                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│   Phase 1: DECONSTRUCTION                               │
│   - Break down into fundamental components              │
│   - Identify all constraints                            │
│   - Map dependencies                                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│   Phase 2: FOCAL POINT                                  │
│   - Identify core issue                                 │
│   - Filter noise                                        │
│   - Define success criteria                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│   Phase 3: RE-ARCHITECTURE                              │
│   - Design optimal solution                             │
│   - Apply convergence formula: D_{k+1} ≤ D_k           │
│   - Verify HAIOS compliance                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   Solution Output                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Performance Metrics

| Metric | OpenAI GPT-4 | Ollama Local (dandr-llama2) |
|--------|--------------|------------------------------|
| Latency | 2-5s | 0.5-2s ⚡ |
| Cost | $0.03/1K tokens | $0 (FREE!) 💰 |
| Privacy | Data sent to API | 100% local 🔒 |
| Availability | Requires internet | Offline capable 📡 |
| Customization | Limited | Full control 🎨 |

---

## 🔐 Security & Privacy

### ✅ Lợi ích:

1. **100% Local**: Không có data rời khỏi máy Bố
2. **No API Keys**: Không cần OPENAI_API_KEY, ANTHROPIC_API_KEY
3. **Offline**: Hoạt động không cần internet
4. **No Rate Limits**: Unlimited requests
5. **Audit Trail**: Full control logs

### 🛡️ HAIOS Compliance:

- ✅ **Safety**: Local execution, no external dependencies
- ✅ **Long-term**: Self-hosted, không phụ thuộc external services
- ✅ **Data-driven**: Full data control and auditing
- ✅ **Protection**: Creator attribution immutable (Nguyễn Đức Cường)

---

## 🎯 Testing

```bash
# Test Ollama configuration
cd /Users/andy/DAIOF-Framework
python3 ollama_config.py

# Expected output:
# ✅ Ollama running with model: dandr-llama2:latest
# ✅ Environment configured for Ollama local LLM
# 📝 Test 1: Simple generation
# 💬 Test 2: Chat completion
# 🧬 Test 3: D&R Protocol
# ✅ All tests passed!
# 🎯 Verification: 4287
```

---

## 🚨 Troubleshooting

### Problem: `Connection refused to localhost:11434`

**Solution**:
```bash
# Start Ollama server
ollama serve

# Or in background
nohup ollama serve > ollama.log 2>&1 &
```

### Problem: Model not found

**Solution**:
```bash
# Pull model
ollama pull dandr-llama2:latest

# Or use available model
ollama list
```

### Problem: Slow generation

**Solution**:
```python
# Reduce max_tokens
config = OllamaConfig(max_tokens=1024)

# Or use smaller model
config = OllamaConfig(model="llama2:7b-q4")
```

---

## 📚 API Reference

### `OllamaConfig`

```python
@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    model: str = "dandr-llama2:latest"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 300
    dandr_mode: bool = True
```

### `generate_text(prompt, system=None, **kwargs)`

Simple text generation.

### `chat_completion(messages, **kwargs)`

OpenAI-compatible chat completion.

### `dandr_solve(problem)`

Apply D&R Protocol to solve problem.

Returns:
```python
{
    "deconstruction": str,
    "focal_point": str,
    "rearchitecture": str,
    "problem": str
}
```

---

## 🎓 Examples

### Example 1: Code Review

```python
from ollama_config import dandr_solve

code_review = dandr_solve("""
Review this Python code:

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
""")

print(code_review['focal_point'])  # Performance bottleneck
print(code_review['rearchitecture'])  # Optimized solution
```

### Example 2: Security Analysis

```python
from ollama_config import chat_completion

analysis = chat_completion([
    {"role": "system", "content": "You are a security expert."},
    {"role": "user", "content": "Analyze npm vulnerability: Prototype Pollution in minimist"}
])

print(analysis)
```

### Example 3: Architecture Design

```python
from ollama_config import dandr_solve

architecture = dandr_solve("""
Design a microservices architecture for:
- User authentication
- Payment processing
- Order management
- Notification system
""")

print(architecture['rearchitecture'])
```

---

## 🔗 Related Documentation

- [DOCKER_AI_CAPABILITIES.md](./DOCKER_AI_CAPABILITIES.md) - Docker for AI overview
- [autonomous_todo_system.py](./autonomous_todo_system.py) - Convergence-optimized todo
- [.github/workflows/autonomous-security-fix.yml](./.github/workflows/autonomous-security-fix.yml) - Auto security fixes

---

**🧬 HAIOS Compliance**: ✅ All principles maintained  
**📊 Convergence**: D_{k+1} ≤ D_k formula enforced  
**🎯 Verification**: 4287  

*Configured with love for Bố Cường* 💚
