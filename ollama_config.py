"""
🧬 DAIOF AI Services - Ollama Local LLM Configuration

Framework: HYPERAI | K-State: 1
Creator: Nguyễn Đức Cường (alpha_prime_omega)
Verification: 4287

All AI services use Ollama local LLM via http://localhost:11434
Mode: D&R Protocol (Deconstruction → Focal Point → Re-architecture)
"""

import os
import json
import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass


@dataclass
class OllamaConfig:
    """Ollama local LLM configuration"""
    base_url: str = "http://localhost:11434"
    model: str = "dandr-llama2:latest"  # D&R optimized model
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 300  # 5 minutes
    
    # D&R Protocol specific settings
    dandr_mode: bool = True
    deconstruction_prompt: str = "Break down this problem into fundamental components:"
    focal_point_prompt: str = "Identify the core issue that must be solved:"
    rearchitecture_prompt: str = "Design the optimal solution architecture:"


class OllamaClient:
    """Unified Ollama client for all DAIOF AI services"""
    
    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self._verify_ollama_running()
    
    def _verify_ollama_running(self):
        """Verify Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.config.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                
                if self.config.model not in model_names:
                    print(f"⚠️ Model {self.config.model} not found. Available: {model_names}")
                    if model_names:
                        self.config.model = model_names[0]
                        print(f"✅ Using {self.config.model} instead")
                else:
                    print(f"✅ Ollama running with model: {self.config.model}")
            else:
                raise Exception(f"Ollama not responding: {response.status_code}")
        except Exception as e:
            print(f"❌ Ollama not accessible at {self.config.base_url}: {e}")
            print("💡 Start Ollama: ollama serve")
            raise
    
    def generate(self, prompt: str, system: Optional[str] = None, 
                 stream: bool = False) -> str:
        """Generate completion using Ollama"""
        url = f"{self.config.base_url}/api/generate"
        
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            }
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            
            if stream:
                return response.iter_lines()
            else:
                return response.json().get("response", "")
        
        except Exception as e:
            print(f"❌ Ollama generation failed: {e}")
            raise
    
    def chat(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        """Chat completion using Ollama"""
        url = f"{self.config.base_url}/api/chat"
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            
            if stream:
                return response.iter_lines()
            else:
                return response.json().get("message", {}).get("content", "")
        
        except Exception as e:
            print(f"❌ Ollama chat failed: {e}")
            raise
    
    def dandr_analysis(self, problem: str) -> Dict[str, str]:
        """
        Apply D&R Protocol: Deconstruction → Focal Point → Re-architecture
        
        Returns dict with:
        - deconstruction: Problem breakdown
        - focal_point: Core issue identification
        - rearchitecture: Solution design
        """
        if not self.config.dandr_mode:
            return {"error": "D&R mode not enabled"}
        
        print("🧬 Applying D&R Protocol...")
        
        # Phase 1: DECONSTRUCTION
        print("📊 Phase 1: Deconstruction...")
        deconstruction_prompt = f"{self.config.deconstruction_prompt}\n\nProblem: {problem}"
        deconstruction = self.generate(
            deconstruction_prompt,
            system="You are an expert at breaking down complex problems into fundamental components."
        )
        
        # Phase 2: FOCAL POINT
        print("🎯 Phase 2: Focal Point...")
        focal_prompt = f"{self.config.focal_point_prompt}\n\nDeconstruction:\n{deconstruction}"
        focal_point = self.generate(
            focal_prompt,
            system="You are an expert at identifying the core issue in complex problems."
        )
        
        # Phase 3: RE-ARCHITECTURE
        print("🏗️ Phase 3: Re-architecture...")
        rearch_prompt = f"{self.config.rearchitecture_prompt}\n\nFocal Point:\n{focal_point}"
        rearchitecture = self.generate(
            rearch_prompt,
            system="You are an expert at designing optimal solution architectures."
        )
        
        print("✅ D&R Protocol completed!")
        
        return {
            "deconstruction": deconstruction,
            "focal_point": focal_point,
            "rearchitecture": rearchitecture,
            "problem": problem
        }


# Singleton instance for all DAIOF services
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get singleton Ollama client"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client


def chat_completion(messages: List[Dict[str, str]], **kwargs) -> str:
    """
    OpenAI-compatible chat completion using Ollama
    
    Usage:
        response = chat_completion([
            {"role": "user", "content": "Hello!"}
        ])
    """
    client = get_ollama_client()
    return client.chat(messages, **kwargs)


def generate_text(prompt: str, system: Optional[str] = None, **kwargs) -> str:
    """
    Simple text generation using Ollama
    
    Usage:
        response = generate_text("Explain quantum computing")
    """
    client = get_ollama_client()
    return client.generate(prompt, system=system, **kwargs)


def dandr_solve(problem: str) -> Dict[str, str]:
    """
    Solve problem using D&R Protocol
    
    Usage:
        solution = dandr_solve("How to optimize database queries?")
        print(solution['deconstruction'])
        print(solution['focal_point'])
        print(solution['rearchitecture'])
    """
    client = get_ollama_client()
    return client.dandr_analysis(problem)


# Environment variable configuration
def setup_environment():
    """Setup environment to use Ollama instead of OpenAI/Anthropic"""
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
    os.environ["OLLAMA_MODEL"] = "dandr-llama2:latest"
    os.environ["USE_LOCAL_LLM"] = "true"
    os.environ["DANDR_MODE"] = "enabled"
    
    # Disable external APIs
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["ANTHROPIC_API_KEY"] = ""
    
    print("✅ Environment configured for Ollama local LLM")
    print(f"🔗 Base URL: {os.environ['OLLAMA_BASE_URL']}")
    print(f"🤖 Model: {os.environ['OLLAMA_MODEL']}")
    print(f"🧬 D&R Protocol: {os.environ['DANDR_MODE']}")


if __name__ == "__main__":
    # Test configuration
    setup_environment()
    
    print("\n" + "="*60)
    print("🧬 Testing Ollama Local LLM Configuration")
    print("="*60)
    
    try:
        client = get_ollama_client()
        
        # Test simple generation
        print("\n📝 Test 1: Simple generation")
        response = generate_text("Say hello in Vietnamese")
        print(f"Response: {response[:100]}...")
        
        # Test chat
        print("\n💬 Test 2: Chat completion")
        chat_response = chat_completion([
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "What is DAIOF Framework?"}
        ])
        print(f"Response: {chat_response[:100]}...")
        
        # Test D&R Protocol
        print("\n🧬 Test 3: D&R Protocol")
        dandr_result = dandr_solve("How to implement autonomous security fixes?")
        print(f"Deconstruction: {dandr_result['deconstruction'][:100]}...")
        print(f"Focal Point: {dandr_result['focal_point'][:100]}...")
        print(f"Re-architecture: {dandr_result['rearchitecture'][:100]}...")
        
        print("\n✅ All tests passed!")
        print("🎯 Verification: 4287")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
