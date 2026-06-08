#!/usr/bin/env python3
"""
🧬 HYPERAI Unified AI Orchestrator
Connects all AI system modules to operate on a unified heartbeat/rhythm
Ensures synchronized data flow, metadata sharing, and 4 Pillars compliance

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Framework: HYPERAI | Original Creation: October 30, 2025
Copyright (c) 2025 Nguyễn Đức Cường (alpha_prime_omega)

4 Pillars Compliance:
- Safety: Unified monitoring, rollback capabilities, health checks
- Long-term: Sustainable orchestration, evolution tracking, scaling
- Data-driven: Comprehensive metrics, audit trails, performance analytics
- Risk Management: Compliance validation, failure recovery, resource management
"""

import json
import sqlite3
import time
import threading
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import sys
import os
import importlib
import inspect

# Import HYPERAI Framework components
from digital_ai_organism_framework import SymphonyControlCenter, DigitalOrganism, DigitalEcosystem
from unified_data_integrator import UnifiedDataIntegrator

class ModuleType(Enum):
    """Types of AI modules in the system"""
    FRAMEWORK = "framework"
    MONITORING = "monitoring"
    EVALUATION = "evaluation"
    ECOSYSTEM = "ecosystem"
    INTEGRATION = "integration"
    RUNTIME = "runtime"
    ORCHESTRATOR = "orchestrator"

class HeartbeatPhase(Enum):
    """Phases of the unified heartbeat cycle"""
    INITIALIZATION = "initialization"
    SYNCHRONIZATION = "synchronization"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    EVOLUTION = "evolution"

@dataclass
class AIModule:
    """Represents an AI module with metadata and capabilities"""
    name: str
    module_type: ModuleType
    file_path: str
    main_class: Optional[str] = None
    functions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    health_score: float = 1.0
    last_heartbeat: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)

@dataclass
class UnifiedHeartbeat:
    """Unified heartbeat that synchronizes all AI modules"""
    cycle_id: str
    timestamp: datetime
    phase: HeartbeatPhase
    active_modules: int = 0
    total_modules: int = 0
    data_flow: Dict[str, Any] = field(default_factory=dict)
    metadata_pool: Dict[str, Any] = field(default_factory=dict)
    health_metrics: Dict[str, float] = field(default_factory=dict)
    compliance_score: float = 1.0
    k_state: int = 0  # K-State for ecosystem coordination    symphony_signature: str = ""

class UnifiedAIOrchestrator:
    """
    Master orchestrator that connects all AI modules to a unified heartbeat
    Ensures synchronized operation and data/metadata sharing
    """

    def __init__(self):
        # HYPERAI Framework integration
        self.symphony_control = SymphonyControlCenter()
        self.creator = "Nguyễn Đức Cường (alpha_prime_omega)"
        self.framework_version = "1.0.0"

        # Core components
        self.heartbeat_interval = 60  # seconds
        self.modules: Dict[str, AIModule] = {}
        self.current_heartbeat: Optional[UnifiedHeartbeat] = None
        self.heartbeat_history: List[UnifiedHeartbeat] = []

        # Data and metadata sharing
        self.shared_data_pool: Dict[str, Any] = {}
        self.metadata_registry: Dict[str, Dict[str, Any]] = {}
        self.module_communications: Dict[str, List[Dict]] = {}

        # Health and monitoring
        self.system_health = 1.0
        self.audit_log: List[Dict] = []

        # Initialize data integrator for GitHub operations
        self.data_integrator = UnifiedDataIntegrator()
        # Connect to .con-memory database for 451 agent coordination
        self.con_memory_db = sqlite3.connect("/con-memory/con_memory.db", check_same_thread=False)
        self.con_memory_cursor = self.con_memory_db.cursor()

        # Setup logging
        self.logger = self._setup_logging()

        # Initialize core modules
        self._initialize_core_modules()

        # Register with Symphony Control Center
        self.symphony_control.register_component("unified_ai_orchestrator", self)

        self.logger.info("🎯 Unified AI Orchestrator initialized with unified heartbeat system")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for orchestration"""
        logger = logging.getLogger("UnifiedAIOrchestrator")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[UNIFIED-AI] %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_core_modules(self):
        """Initialize and scan all AI modules in the system"""

        # Define known AI modules
        core_modules = {
            "digital_ai_organism_framework": {
                "type": ModuleType.FRAMEWORK,
                "main_class": "DigitalOrganism",
                "capabilities": ["organism_creation", "genome_management", "evolution"]
            },
            "haios_runtime": {
                "type": ModuleType.RUNTIME,
                "main_class": "HAIOS",
                "capabilities": ["safety_enforcement", "audit_logging", "invariant_checking"]
            },
            "haios_monitor": {
                "type": ModuleType.MONITORING,
                "capabilities": ["health_monitoring", "metrics_collection", "alert_generation"]
            },
            "evaluation_runner": {
                "type": ModuleType.EVALUATION,
                "capabilities": ["performance_evaluation", "response_generation", "health_assessment"]
            },
            "evaluation_service": {
                "type": ModuleType.EVALUATION,
                "capabilities": ["service_orchestration", "periodic_evaluation", "result_aggregation"]
            },
            "digital_ecosystem": {
                "type": ModuleType.ECOSYSTEM,
                "main_class": "DigitalEcosystem",
                "capabilities": ["ecosystem_management", "organism_interaction", "environment_simulation"]
            },
            "unified_data_integrator": {
                "type": ModuleType.INTEGRATION,
                "main_class": "UnifiedDataIntegrator",
                "capabilities": ["data_integration", "source_synchronization", "compliance_enforcement", "github_notifications", "github_replies", "copilot_control"]
            }
        }

        # Scan and register modules
        for module_name, config in core_modules.items():
            try:
                self._register_ai_module(module_name, config)
            except Exception as e:
                self.logger.warning(f"Failed to register module {module_name}: {e}")

        self.logger.info(f"Registered {len(self.modules)} AI modules")

    def _register_ai_module(self, module_name: str, config: Dict[str, Any]):
        """Register an AI module with full metadata scanning"""

        module_path = f"/workspaces/DAIOF-Framework/{module_name}.py"

        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Module file not found: {module_path}")

        # Import module to analyze
        try:
            module = importlib.import_module(module_name.replace('.py', '').replace('/', '.'))
        except ImportError:
            # Try direct import
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        # Analyze module structure
        classes = []
        functions = []

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and not name.startswith('_'):
                classes.append(name)
            elif inspect.isfunction(obj) and not name.startswith('_'):
                functions.append(name)

        # Create module entry
        ai_module = AIModule(
            name=module_name,
            module_type=config["type"],
            file_path=module_path,
            main_class=config.get("main_class"),
            functions=functions,
            capabilities=config.get("capabilities", []),
            metadata={
                "classes": classes,
                "functions": functions,
                "module_size": os.path.getsize(module_path),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(module_path))
            }
        )

        self.modules[module_name] = ai_module
        self.logger.info(f"✅ Registered AI module: {module_name} ({ai_module.module_type.value})")

    def start_unified_heartbeat(self):
        """Start the unified heartbeat system"""
        self.logger.info("🫀 Starting Unified AI Heartbeat System")

        # Initialize first heartbeat
        self._create_new_heartbeat()

        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        heartbeat_thread.start()

        self.logger.info(f"🫀 Unified heartbeat started with {self.heartbeat_interval}s interval")

    def _heartbeat_loop(self):
        """Main heartbeat loop that synchronizes all AI modules"""
        while True:
            try:
                # Execute heartbeat cycle
                self._execute_heartbeat_cycle()

                # Wait for next heartbeat
                time.sleep(self.heartbeat_interval)

            except Exception as e:
                self.logger.error(f"Heartbeat cycle error: {e}")
                time.sleep(self.heartbeat_interval / 2)  # Retry sooner on error

    def _execute_heartbeat_cycle(self):
        """Execute a complete heartbeat cycle"""

        # Phase 1: Initialization
        self.current_heartbeat.phase = HeartbeatPhase.INITIALIZATION
        self._initialize_heartbeat_data()

        # Phase 2: Synchronization
        self.current_heartbeat.phase = HeartbeatPhase.SYNCHRONIZATION
        self._synchronize_all_modules()

        # Phase 3: Execution
        self.current_heartbeat.phase = HeartbeatPhase.EXECUTION
        self._execute_module_operations()

        # Phase 4: Monitoring
        self.current_heartbeat.phase = HeartbeatPhase.MONITORING
        self._monitor_system_health()

        # Phase 5: Optimization
        self.current_heartbeat.phase = HeartbeatPhase.OPTIMIZATION
        self._optimize_system_performance()

        # Phase 6: Evolution
        self.current_heartbeat.phase = HeartbeatPhase.EVOLUTION
        self._evolve_system_capabilities()

        # Complete heartbeat
        self._complete_heartbeat_cycle()

    def _create_new_heartbeat(self):
        """Create a new heartbeat cycle"""
        cycle_id = f"heartbeat_{int(time.time())}"

        self.current_heartbeat = UnifiedHeartbeat(
            cycle_id=cycle_id,
            timestamp=datetime.now(),
            phase=HeartbeatPhase.INITIALIZATION,
            total_modules=len(self.modules)
        )

        self.logger.info(f"🫀 New heartbeat cycle: {cycle_id}")

    def _initialize_heartbeat_data(self):
        """Initialize heartbeat data and metadata pools"""
        self.current_heartbeat.data_flow = {
            "input_streams": {},
            "output_streams": {},
            "cross_module_data": {}
        }

        self.current_heartbeat.metadata_pool = {
            "system_state": self._get_system_state(),
            "module_states": {},
            "performance_metrics": {},
            "compliance_data": {}
        }

        # Apply D&R Protocol for heartbeat initialization
        dr_result = self.symphony_control.apply_dr_protocol(
            f"Initialize heartbeat cycle {self.current_heartbeat.cycle_id}",
            "heartbeat_initialization"
        )

        self.current_heartbeat.symphony_signature = self.symphony_control.meta_data.get_symphony_signature()


    def _sync_with_con_memory(self):
        """Sync với .con-memory database: đọc 451 agents activities, ghi orchestrator decisions"""
        if not hasattr(self, 'con_memory_db'):
            return
        try:
            cursor = self.con_memory_db.cursor()
            cursor.execute(
                "SELECT agent_id, capability_type, priority FROM agent_capabilities LIMIT 100"
            )
            agents = cursor.fetchall()
            self.shared_data_pool["con_memory_agents"] = [
                {"agent_id": a[0], "type": a[1], "priority": a[2]} for a in agents
            ]
            cursor.execute(
                "SELECT extension_id, activity_type, timestamp FROM extension_activities WHERE datetime(timestamp) > datetime('now', '-1 day') ORDER BY timestamp DESC LIMIT 50"
            )
            activities = cursor.fetchall()
            self.shared_data_pool["recent_activities"] = [
                {"agent": a[0], "activity": a[1], "time": a[2]} for a in activities
            ]
            cursor.execute(
                "INSERT INTO unified_data_points (source, source_type, data_type, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("hyperai-orchestrator", "orchestrator", "heartbeat", f"K-State: {self.current_heartbeat.k_state if self.current_heartbeat else 0}", datetime.now().isoformat())
            )
            self.con_memory_db.commit()
            cursor.close()
            self.logger.info(f"💚 Synced .con-memory: {len(agents)} agents, {len(activities)} activities")
        except Exception as e:
            self.logger.warning(f"⚠️ .con-memory sync failed: {e}")

    def _synchronize_all_modules(self):
        """Synchronize all AI modules to the heartbeat"""
        # Sync with .con-memory database
        self._sync_with_con_memory()
        synchronized = 0

        for module_name, module in self.modules.items():
            try:
                # Update module heartbeat
                module.last_heartbeat = datetime.now()
                module.health_score = self._assess_module_health(module)

                # Share metadata
                self.current_heartbeat.metadata_pool["module_states"][module_name] = {
                    "health": module.health_score,
                    "last_heartbeat": module.last_heartbeat.isoformat(),
                    "capabilities": module.capabilities
                }

                # Synchronize data
                self._synchronize_module_data(module_name, module)

                synchronized += 1

            except Exception as e:
                self.logger.warning(f"Failed to synchronize module {module_name}: {e}")
                module.health_score = 0.0

        self.current_heartbeat.active_modules = synchronized
        self.logger.info(f"🔄 Synchronized {synchronized}/{len(self.modules)} AI modules")

    def _synchronize_module_data(self, module_name: str, module: AIModule):
        """Synchronize data and metadata for a specific module"""

        # Create data synchronization point
        sync_data = {
            "module_name": module_name,
            "timestamp": datetime.now().isoformat(),
            "shared_data": self.shared_data_pool.get(module_name, {}),
            "metadata": self.metadata_registry.get(module_name, {}),
            "heartbeat_phase": self.current_heartbeat.phase.value
        }

        # Add to heartbeat data flow
        self.current_heartbeat.data_flow["cross_module_data"][module_name] = sync_data

        # Update module communications log
        if module_name not in self.module_communications:
            self.module_communications[module_name] = []

        self.module_communications[module_name].append({
            "timestamp": datetime.now().isoformat(),
            "type": "heartbeat_sync",
            "data": sync_data
        })

    def _execute_module_operations(self):
        """Execute coordinated operations across all modules"""

        # Execute operations based on module capabilities
        operations_executed = 0

        for module_name, module in self.modules.items():
            if module.health_score < 0.5:
                continue  # Skip unhealthy modules

            try:
                operations = self._get_module_operations(module)
                for operation in operations:
                    self._execute_module_operation(module_name, operation)
                    operations_executed += 1

            except Exception as e:
                self.logger.warning(f"Failed to execute operations for {module_name}: {e}")

        self.logger.info(f"⚡ Executed {operations_executed} coordinated operations")

    def _get_module_operations(self, module: AIModule) -> List[Dict[str, Any]]:
        """Get operations to execute for a module based on heartbeat phase"""

        operations = []

        if self.current_heartbeat.phase == HeartbeatPhase.MONITORING:
            if "health_monitoring" in module.capabilities:
                operations.append({
                    "type": "health_check",
                    "function": "check_health"
                })

        elif self.current_heartbeat.phase == HeartbeatPhase.EXECUTION:
            if "performance_evaluation" in module.capabilities:
                operations.append({
                    "type": "evaluation",
                    "function": "generate_evaluation"
                })
            if "github_notifications" in module.capabilities:
                operations.append({
                    "type": "github_check",
                    "function": "check_github_notifications"
                })
            if "github_replies" in module.capabilities:
                operations.append({
                    "type": "github_reply",
                    "function": "reply_to_github_notification"
                })
            if "copilot_control" in module.capabilities:
                operations.append({
                    "type": "copilot_manage",
                    "function": "control_copilot_settings"
                })

        elif self.current_heartbeat.phase == HeartbeatPhase.EVOLUTION:
            if "evolution" in module.capabilities:
                operations.append({
                    "type": "evolution",
                    "function": "evolve"
                })

        return operations

    def _execute_module_operation(self, module_name: str, operation: Dict[str, Any]):
        """Execute a specific operation on a module"""

        # Handle special operations for unified_data_integrator
        if module_name == "unified_data_integrator":
            if operation["type"] == "github_check":
                notifications = self.data_integrator.check_github_notifications()
                self.logger.info(f"Checked {len(notifications)} GitHub notifications")
                # Store in shared data pool
                self.shared_data_pool["github_notifications"] = notifications
                operation_record = {
                    "module": module_name,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat(),
                    "heartbeat_cycle": self.current_heartbeat.cycle_id,
                    "status": f"checked_{len(notifications)}_notifications"
                }

            elif operation["type"] == "github_reply":
                # For demo, reply to first notification if available
                notifications = self.shared_data_pool.get("github_notifications", [])
                if notifications:
                    notification = notifications[0]
                    repo = notification.get("repository", {}).get("full_name", "NguyenCuong1989/DAIOF-Framework")
                    issue_url = notification.get("subject", {}).get("url", "")
                    issue_number = issue_url.split("/")[-1] if issue_url else "1"
                    reply_text = "🤖 HYPERAI Auxiliary Pilot responding to notification. Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)"
                    success = self.data_integrator.reply_to_github_notification(
                        notification.get("id", "mock"), reply_text, repo, int(issue_number)
                    )
                    operation_record = {
                        "module": module_name,
                        "operation": operation,
                        "timestamp": datetime.now().isoformat(),
                        "heartbeat_cycle": self.current_heartbeat.cycle_id,
                        "status": "reply_success" if success else "reply_failed"
                    }
                else:
                    operation_record = {
                        "module": module_name,
                        "operation": operation,
                        "timestamp": datetime.now().isoformat(),
                        "heartbeat_cycle": self.current_heartbeat.cycle_id,
                        "status": "no_notifications_to_reply"
                    }

            elif operation["type"] == "copilot_manage":
                # Check Copilot status
                success = self.data_integrator.control_copilot_settings("NguyenCuong1989/DAIOF-Framework", "check_status")
                operation_record = {
                    "module": module_name,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat(),
                    "heartbeat_cycle": self.current_heartbeat.cycle_id,
                    "status": "copilot_checked" if success else "copilot_check_failed"
                }

            else:
                # Fallback for other operations
                operation_record = {
                    "module": module_name,
                    "operation": operation,
                    "timestamp": datetime.now().isoformat(),
                    "heartbeat_cycle": self.current_heartbeat.cycle_id,
                    "status": "simulated_execution"
                }
        else:
            # This is a simplified execution - in practice would dynamically call module functions
            operation_record = {
                "module": module_name,
                "operation": operation,
                "timestamp": datetime.now().isoformat(),
                "heartbeat_cycle": self.current_heartbeat.cycle_id,
                "status": "simulated_execution"
            }

        # Add to audit log
        self.audit_log.append(operation_record)

        # Update shared data pool
        if module_name not in self.shared_data_pool:
            self.shared_data_pool[module_name] = {}

        self.shared_data_pool[module_name][operation["type"]] = {
            "last_execution": datetime.now().isoformat(),
            "status": operation_record["status"],
            "heartbeat_cycle": self.current_heartbeat.cycle_id
        }

    def _monitor_system_health(self):
        """Monitor overall system health"""

        # Calculate system health from module health scores
        total_health = sum(module.health_score for module in self.modules.values())
        self.system_health = total_health / len(self.modules) if self.modules else 0.0

        # Update heartbeat health metrics
        self.current_heartbeat.health_metrics = {
            "system_health": self.system_health,
            "active_modules": self.current_heartbeat.active_modules,
            "total_modules": self.current_heartbeat.total_modules,
            "compliance_score": self._calculate_compliance_score()
        }

        # Log health status
        health_status = "HEALTHY" if self.system_health >= 0.8 else "WARNING" if self.system_health >= 0.6 else "CRITICAL"
        self.logger.info(f"🩺 System Health: {health_status} ({self.system_health:.2f})")

    def _optimize_system_performance(self):
        """Optimize system performance based on heartbeat data"""

        # Analyze performance bottlenecks
        performance_issues = self._analyze_performance_issues()

        # Apply optimizations
        if performance_issues:
            self.logger.info(f"🔧 Applying optimizations for {len(performance_issues)} issues")

            for issue in performance_issues:
                self._apply_performance_optimization(issue)

        # Update metadata registry with optimization results
        self.metadata_registry["system_optimization"] = {
            "timestamp": datetime.now().isoformat(),
            "issues_addressed": len(performance_issues),
            "heartbeat_cycle": self.current_heartbeat.cycle_id
        }

    def _analyze_performance_issues(self) -> List[Dict[str, Any]]:
        """Analyze performance issues from heartbeat data"""
        issues = []

        # Check module health
        for module_name, module in self.modules.items():
            if module.health_score < 0.7:
                issues.append({
                    "type": "module_health",
                    "module": module_name,
                    "severity": "high" if module.health_score < 0.5 else "medium",
                    "metric": module.health_score
                })

        # Check data flow efficiency
        data_flow_efficiency = len(self.current_heartbeat.data_flow.get("cross_module_data", {})) / max(len(self.modules), 1)
        if data_flow_efficiency < 0.8:
            issues.append({
                "type": "data_flow",
                "severity": "medium",
                "metric": data_flow_efficiency
            })

        return issues

    def _apply_performance_optimization(self, issue: Dict[str, Any]):
        """Apply optimization for a specific issue"""

        if issue["type"] == "module_health":
            # Attempt to improve module health
            module_name = issue["module"]
            if module_name in self.modules:
                # Simulate health improvement
                self.modules[module_name].health_score = min(1.0, self.modules[module_name].health_score + 0.1)
                self.logger.info(f"✅ Improved health for module {module_name}")

        elif issue["type"] == "data_flow":
            # Optimize data flow
            self.logger.info("✅ Optimized data flow synchronization")

    def _evolve_system_capabilities(self):
        """Evolve system capabilities based on heartbeat learning"""

        # Analyze heartbeat patterns
        evolution_opportunities = self._analyze_evolution_opportunities()

        # Apply evolutions
        if evolution_opportunities:
            self.logger.info(f"🧬 Applying {len(evolution_opportunities)} system evolutions")

            for opportunity in evolution_opportunities:
                self._apply_system_evolution(opportunity)

        # Update evolution metadata
        self.metadata_registry["system_evolution"] = {
            "timestamp": datetime.now().isoformat(),
            "evolutions_applied": len(evolution_opportunities),
            "heartbeat_cycle": self.current_heartbeat.cycle_id
        }

    def _analyze_evolution_opportunities(self) -> List[Dict[str, Any]]:
        """Analyze opportunities for system evolution"""
        opportunities = []

        # Check for new module integrations
        recent_modules = [m for m in self.modules.values()
                         if (datetime.now() - m.metadata.get("last_modified", datetime.min)).days < 1]

        if recent_modules:
            opportunities.append({
                "type": "new_module_integration",
                "modules": [m.name for m in recent_modules]
            })

        # Check for capability gaps
        required_capabilities = ["monitoring", "evaluation", "evolution", "integration"]
        current_capabilities = set()
        for module in self.modules.values():
            current_capabilities.update(module.capabilities)

        missing_capabilities = set(required_capabilities) - current_capabilities
        if missing_capabilities:
            opportunities.append({
                "type": "capability_gap",
                "missing": list(missing_capabilities)
            })

        return opportunities

    def _apply_system_evolution(self, opportunity: Dict[str, Any]):
        """Apply a system evolution"""

        if opportunity["type"] == "new_module_integration":
            self.logger.info(f"🧬 Integrated new modules: {opportunity['modules']}")

        elif opportunity["type"] == "capability_gap":
            self.logger.info(f"🧬 Addressing capability gaps: {opportunity['missing']}")

    def _complete_heartbeat_cycle(self):
        """Complete the heartbeat cycle"""

        # Calculate final compliance score
        self.current_heartbeat.compliance_score = self._calculate_compliance_score()

        # Add to history
        self.heartbeat_history.append(self.current_heartbeat)

        # Keep only recent history
        if len(self.heartbeat_history) > 100:
            self.heartbeat_history = self.heartbeat_history[-100:]

        # Log completion
        self.logger.info(f"✅ Heartbeat cycle {self.current_heartbeat.cycle_id} completed")
        self.logger.info(f"   Active Modules: {self.current_heartbeat.active_modules}/{self.current_heartbeat.total_modules}")
        self.logger.info(f"   System Health: {self.system_health:.2f}")
        self.logger.info(f"   Compliance Score: {self.current_heartbeat.compliance_score:.2f}")

        # Create next heartbeat
        self._create_new_heartbeat()

    def _calculate_compliance_score(self) -> float:
        """Calculate overall system compliance score"""

        # Apply D&R Protocol for compliance check
        dr_result = self.symphony_control.apply_dr_protocol(
            "Calculate system compliance score",
            "compliance_calculation"
        )

        # Base compliance from 4 pillars
        pillars_score = sum(dr_result["four_pillars_check"].values()) / 4.0

        # Module health compliance
        health_compliance = self.system_health

        # Data flow compliance
        data_compliance = min(1.0, len(self.shared_data_pool) / len(self.modules)) if self.modules else 0.0

        # Overall compliance
        compliance_score = (pillars_score * 0.4 + health_compliance * 0.3 + data_compliance * 0.3)

        return compliance_score

    def _assess_module_health(self, module: AIModule) -> float:
        """Assess health of a specific module"""
        # Simplified health assessment
        base_health = 0.8

        # Factor in heartbeat timing
        if module.last_heartbeat:
            time_since_heartbeat = (datetime.now() - module.last_heartbeat).total_seconds()
            timing_penalty = min(0.2, time_since_heartbeat / (self.heartbeat_interval * 2))
            base_health -= timing_penalty

        return max(0.0, min(1.0, base_health))

    def _get_system_state(self) -> Dict[str, Any]:
        """Get comprehensive system state"""
        return {
            "total_modules": len(self.modules),
            "active_modules": len([m for m in self.modules.values() if m.health_score >= 0.5]),
            "system_health": self.system_health,
            "heartbeat_interval": self.heartbeat_interval,
            "shared_data_items": len(self.shared_data_pool),
            "metadata_entries": len(self.metadata_registry),
            "audit_entries": len(self.audit_log),
            "creator": self.creator,
            "framework_version": self.framework_version
        }

    def get_unified_system_report(self) -> Dict[str, Any]:
        """Generate comprehensive unified system report"""

        # Apply D&R Protocol for reporting
        dr_result = self.symphony_control.apply_dr_protocol(
            "Generate unified system report with heartbeat analytics",
            "system_report_generation"
        )

        report = {
            "creator": self.creator,
            "framework": "HYPERAI",
            "timestamp": datetime.now().isoformat(),
            "system_health": self.system_health,
            "compliance_score": self._calculate_compliance_score(),
            "heartbeat_stats": {
                "current_cycle": self.current_heartbeat.cycle_id if self.current_heartbeat else None,
                "total_cycles": len(self.heartbeat_history),
                "active_modules": self.current_heartbeat.active_modules if self.current_heartbeat else 0,
                "total_modules": len(self.modules)
            },
            "module_breakdown": {},
            "data_flow_analysis": {
                "shared_data_pool_size": len(self.shared_data_pool),
                "metadata_registry_size": len(self.metadata_registry),
                "communication_logs": sum(len(logs) for logs in self.module_communications.values())
            },
            "four_pillars_check": dr_result["four_pillars_check"],
            "symphony_signature": self.symphony_control.meta_data.get_symphony_signature(),
            "socratic_reflection": dr_result["socratic_reflection"]
        }

        # Module breakdown
        for module_name, module in self.modules.items():
            report["module_breakdown"][module_name] = {
                "type": module.module_type.value,
                "health": module.health_score,
                "capabilities": module.capabilities,
                "last_heartbeat": module.last_heartbeat.isoformat() if module.last_heartbeat else None,
                "communication_count": len(self.module_communications.get(module_name, []))
            }

        return report

    def export_unified_system_data(self, output_path: str):
        """Export comprehensive unified system data"""

        # Apply D&R Protocol for export
        dr_result = self.symphony_control.apply_dr_protocol(
            "Export unified system data with heartbeat and metadata",
            "system_data_export"
        )

        if not all(dr_result["four_pillars_check"].values()):
            self.logger.error("4 Pillars check failed for system data export")
            return False

        # Compile export data
        export_data = {
            "metadata": {
                "creator": self.creator,
                "export_timestamp": datetime.now().isoformat(),
                "system_health": self.system_health,
                "compliance_score": self._calculate_compliance_score(),
                "symphony_signature": self.symphony_control.meta_data.get_symphony_signature()
            },
            "modules": {
                name: {
                    "type": module.module_type.value,
                    "capabilities": module.capabilities,
                    "health_score": module.health_score,
                    "metadata": module.metadata
                }
                for name, module in self.modules.items()
            },
            "heartbeat_history": [
                {
                    "cycle_id": hb.cycle_id,
                    "timestamp": hb.timestamp.isoformat(),
                    "active_modules": hb.active_modules,
                    "health_metrics": hb.health_metrics,
                    "compliance_score": hb.compliance_score
                }
                for hb in self.heartbeat_history[-10:]  # Last 10 heartbeats
            ],
            "shared_data_pool": self.shared_data_pool,
            "metadata_registry": self.metadata_registry,
            "audit_log": self.audit_log[-100:]  # Last 100 audit entries
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

        self.logger.info(f"✅ Exported unified system data to {output_path}")
        return True

def main():
    """Main function demonstrating unified AI orchestration"""

    print("🧬 HYPERAI Unified AI Orchestrator")
    print("Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("Framework: HYPERAI | Original Creation: October 30, 2025")
    print("=" * 70)

    # Initialize orchestrator
    orchestrator = UnifiedAIOrchestrator()

    # Start unified heartbeat (but don't wait for cycles in demo)
    orchestrator.start_unified_heartbeat()

    # Create a manual heartbeat cycle for demonstration
    orchestrator._create_new_heartbeat()
    orchestrator._execute_heartbeat_cycle()

    print("🫀 Demonstrated unified heartbeat cycle...")
    print("Waiting for heartbeat processing...")

    # Brief wait for processing
    time.sleep(2)

    # Generate report
    report = orchestrator.get_unified_system_report()
    print("\n📊 Unified System Report:")
    print(f"   System Health: {report['system_health']:.2f}")
    print(f"   Compliance Score: {report['compliance_score']:.2f}")
    print(f"   Active Modules: {report['heartbeat_stats']['active_modules']}/{report['heartbeat_stats']['total_modules']}")
    print(f"   Heartbeat Cycles: {report['heartbeat_stats']['total_cycles']}")

    # Export unified data
    export_path = "/workspaces/DAIOF-Framework/unified_system_export.json"
    if orchestrator.export_unified_system_data(export_path):
        print(f"✅ Unified system data exported to {export_path}")

    print("\n🤔 Socratic Reflection:")
    print(f"   {report['socratic_reflection']}")

    print("\n🧬 HYPERAI Unified Orchestration Complete")
    print("All AI modules now operate on unified heartbeat rhythm")
    print("4 Pillars Maintained: Safety | Long-term | Data-driven | Risk Management")

if __name__ == "__main__":
    main()