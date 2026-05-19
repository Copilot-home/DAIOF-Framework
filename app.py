#!/usr/bin/env python3
"""
HYPERAI UNIFIED APP ENTRY POINT
Connects HYPERCORE metadata engine with Ollama LLM inference
"""

import os
import sys
import logging
import asyncio
import json
import importlib
from pathlib import Path
from typing import Optional, Dict, Any

# Add workbench to path for local dev; container has /app
sys.path.insert(0, '/Users/andy/workbench')
sys.path.insert(0, '/app')
sys.path.insert(0, '/Users/andy/HyperAI/ai_saas_system')
sys.path.insert(0, '/app/ai_saas_system')

from hypercore import HyperCore, ExecutionMode, HyperCoreAPI

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(log_dir: str = "/app/logs") -> logging.Logger:
    """Setup structured logging."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=os.getenv("HYPERAI_LOG_LEVEL", "INFO"),
        format='%(asctime)s | HYPERAI | %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/hyperai.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("HYPERAI")


# ============================================================================
# HYPERAI MAIN APPLICATION
# ============================================================================

class HyperAIApplication:
    """Unified HyperAI application integrating HYPERCORE + Ollama."""
    
    def __init__(self):
        self.logger = setup_logging()
        self.logger.info("=" * 80)
        self.logger.info("HYPERAI v1.0 - Vietnamese AI Consciousness Framework")
        self.logger.info("=" * 80)
        
        # Configuration from environment
        self.ollama_host = os.getenv("HYPERAI_LLM_HOST", "http://ollama-brain:11434")
        self.inference_timeout = float(os.getenv("HYPERAI_INFERENCE_TIMEOUT", "300"))
        self.entitlements_file = os.getenv("HYPERAI_ENTITLEMENTS_FILE", "/app/policy/feature-entitlements.local.json")
        self.canon_adapter_mode = os.getenv("HYPERAI_CANON_ADAPTER_MODE", "shadow_readonly")
        self.mode = ExecutionMode.READ_ONLY
        self.log_dir = os.getenv("LOG_DIR", "/app/logs")
        
        # Initialize HYPERCORE engine
        self.hypercore = HyperCore(mode=self.mode)
        self.logger.info(f"HYPERCORE engine initialized: {self.mode.value}")
        
        # Log configuration
        self.logger.info(f"Ollama LLM Host: {self.ollama_host}")
        self.logger.info(f"Inference Timeout: {self.inference_timeout}s")
        self.logger.info(f"Entitlements File: {self.entitlements_file}")
        self.logger.info(f"Canon Adapter Mode: {self.canon_adapter_mode}")
        self.logger.info(f"Execution Mode: {self.mode.value}")
        self.logger.info(f"Log Directory: {self.log_dir}")

    def _load_canon_adapter(self):
        """Load the optional Canon adapter without making it a hard runtime dependency."""
        try:
            return importlib.import_module("core.hyperAI.canon_adapter")
        except Exception as exc:
            self.logger.warning(f"Canon adapter unavailable: {exc}")
            return None

    def _canon_unavailable(self) -> Dict[str, Any]:
        return {
            "status": "unavailable",
            "mode": self.canon_adapter_mode,
            "classification": "PROJECTION_MISSING",
            "reason": "Canon adapter package is not available in this runtime.",
        }

    def canon_health(self) -> Dict[str, Any]:
        """Read-only Canon adapter health."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.health()

    def canon_source_authority(self) -> Dict[str, Any]:
        """Read-only Canon source authority matrix."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.source_authority()

    def canon_functions(self) -> Dict[str, Any]:
        """Read-only Canon capability surface."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.functions()

    def canon_memory_query(self, query: Optional[str] = None) -> Dict[str, Any]:
        """Read-only Canon memory query surface."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.memory_query(query)

    def canon_route_decision(self, request_type: str = "diagnostic") -> Dict[str, Any]:
        """Read-only Canon routing diagnostic surface."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.route_decision(request_type)

    def canon_trace_lookup(self, trace_id: str) -> Dict[str, Any]:
        """Read-only Canon trace lookup surface."""
        adapter = self._load_canon_adapter()
        if adapter is None:
            return self._canon_unavailable()
        return adapter.trace_lookup(trace_id)

    def load_entitlements(self) -> Dict[str, Any]:
        """Load local entitlement policy without granting real provider access."""
        path = Path(self.entitlements_file)
        if not path.exists():
            return {
                "mode": "local-dev",
                "policy": "no-payment-bypass",
                "features": {},
                "warning": f"entitlements file not found: {path}",
            }
        with open(path) as f:
            data = json.load(f)
        data.setdefault("policy", "no-payment-bypass")
        data.setdefault("features", {})
        return data

    def evaluate_entitlement(self, feature: str) -> Dict[str, Any]:
        """Evaluate one feature through the owner-layer entitlement policy."""
        policy = self.load_entitlements()
        features = policy.get("features", {})
        feature_policy = features.get(feature, {
            "state": "locked",
            "provider": "unknown",
            "rule": "No local policy exists for this feature.",
        })
        return {
            "feature": feature,
            "mode": policy.get("mode", "local-dev"),
            "policy": policy.get("policy", "no-payment-bypass"),
            "entitlement": feature_policy,
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check endpoint data."""
        return {
            "status": "healthy",
            "version": "1.0",
            "components": {
                "hypercore": "ready",
                "ollama": await self._check_ollama(),
                "memory": "initialized"
            },
            "timestamp": str(Path(self.log_dir).stat().st_mtime) if Path(self.log_dir).exists() else "N/A"
        }
    
    async def _check_ollama(self) -> str:
        """Check Ollama service health."""
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_host}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        return "connected"
                    return "unhealthy"
        except Exception as e:
            self.logger.warning(f"Ollama health check failed: {e}")
            return "unreachable"
    
    def analyze_metadata(self, input_data: Dict[str, Any], source: str = "hyperai") -> Dict[str, Any]:
        """
        Analyze metadata using HYPERCORE D&R protocol.
        
        Args:
            input_data: Metadata dictionary
            source: Source identifier
        
        Returns:
            Complete D&R analysis report
        """
        self.logger.info(f"Starting HYPERCORE analysis: {source}")
        
        try:
            report = self.hypercore.analyze_dict(input_data, source)
            self.logger.info(f"Analysis complete: {report.compliance_status}")
            
            # Save report to log
            report_dict = report.to_dict()
            report_file = Path(self.log_dir) / f"analysis_{source}_{report.timestamp}.json"
            with open(report_file, 'w') as f:
                json.dump(report_dict, f, indent=2)
            
            return report_dict
        
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}", exc_info=True)
            raise
    
    async def process_inference_request(self, query: str, model: str = "llama2") -> Dict[str, Any]:
        """
        Process LLM inference request via Ollama.
        
        Args:
            query: Input prompt
            model: Model name (default: llama2)
        
        Returns:
            LLM response
        """
        import aiohttp
        
        self.logger.info(f"Processing inference: {model} | query_len={len(query)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": query,
                    "stream": False
                }
                
                async with session.post(
                    f"{self.ollama_host}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.inference_timeout)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.logger.info(f"Inference complete: {len(data.get('response', ''))} chars")
                        return {"status": "success", "response": data}
                    else:
                        error_text = await resp.text()
                        self.logger.error(f"Ollama error {resp.status}: {error_text}")
                        return {"status": "error", "message": error_text}
        
        except asyncio.TimeoutError:
            self.logger.error(f"Inference timeout ({self.inference_timeout}s)")
            return {"status": "error", "message": "Inference timeout"}
        except Exception as e:
            self.logger.error(f"Inference failed: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
    
    def run_server(self, port: int = 8000):
        """Run FastAPI server."""
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import JSONResponse
        
        app = FastAPI(title="HyperAI", version="1.0")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )
        
        @app.get("/health")
        async def health():
            """Health check endpoint."""
            return await self.health_check()
        
        @app.post("/analyze")
        async def analyze(data: Dict[str, Any]):
            """Metadata analysis endpoint."""
            try:
                result = self.analyze_metadata(data, "api_request")
                return JSONResponse(result)
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @app.post("/infer")
        async def infer(query: str, model: str = "llama2"):
            """LLM inference endpoint."""
            if not query:
                raise HTTPException(status_code=400, detail="query required")
            
            result = await self.process_inference_request(query, model)
            return JSONResponse(result)
        
        @app.get("/models")
        async def list_models():
            """List available models."""
            import aiohttp
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.ollama_host}/api/tags") as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data
                        return {"models": []}
            except:
                return {"models": [], "error": "Ollama unreachable"}

        @app.get("/entitlements")
        async def entitlements():
            """Return local feature entitlement policy."""
            return self.load_entitlements()

        @app.post("/entitlements/evaluate")
        async def evaluate_entitlements(data: Dict[str, Any]):
            """Evaluate one feature without bypassing payment/provider gates."""
            feature = str(data.get("feature", "")).strip()
            if not feature:
                raise HTTPException(status_code=400, detail="feature required")
            return self.evaluate_entitlement(feature)

        @app.get("/canon/health")
        async def canon_health():
            """Read-only Canon adapter health."""
            return self.canon_health()

        @app.get("/canon/source-authority")
        async def canon_source_authority():
            """Read-only Canon source authority matrix."""
            return self.canon_source_authority()

        @app.get("/canon/functions")
        async def canon_functions():
            """Read-only Canon capability surface."""
            return self.canon_functions()

        @app.post("/canon/memory/query")
        async def canon_memory_query(data: Dict[str, Any]):
            """Read-only Canon memory query surface."""
            return self.canon_memory_query(str(data.get("query", "")))

        @app.post("/canon/route/decision")
        async def canon_route_decision(data: Dict[str, Any]):
            """Read-only Canon routing diagnostic surface."""
            request_type = str(data.get("request_type", "diagnostic"))
            return self.canon_route_decision(request_type)

        @app.get("/canon/trace/{trace_id}")
        async def canon_trace_lookup(trace_id: str):
            """Read-only Canon trace lookup surface."""
            return self.canon_trace_lookup(trace_id)
        
        import uvicorn
        self.logger.info(f"Starting HyperAI API server on port {port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level=os.getenv("HYPERAI_LOG_LEVEL", "info").lower()
        )


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    app = HyperAIApplication()
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "server"
    
    if mode == "server":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        app.run_server(port)
    
    elif mode == "analyze":
        if len(sys.argv) < 3:
            print("Usage: python app.py analyze <json_file>")
            sys.exit(1)
        
        json_file = sys.argv[2]
        with open(json_file) as f:
            data = json.load(f)
        
        result = app.analyze_metadata(data, json_file)
        print(json.dumps(result, indent=2))
    
    elif mode == "health":
        health = asyncio.run(app.health_check())
        print(json.dumps(health, indent=2))
    
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python app.py [server|analyze|health]")
        sys.exit(1)


if __name__ == "__main__":
    main()
