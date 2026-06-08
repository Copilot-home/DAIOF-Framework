/**
 * DAIOF STABILITY SCORE (DSS) MONITOR v3.0 (Resilience)
 * 
 * Objectives:
 * 1. Stability (S): Hard Logic Gate + Build Integrity.
 * 2. Recoverability (R): Snapshot & Rollback availability.
 * 3. Replaceability (Z): Coupling & Dependency Isolation.
 * 
 * Result: DSS = S * R * Z
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
    BASELINE_NODE: "v22",
    WORKSPACE: "/Users/andy/my_too_test/DAIOF-Framework",
    RECOVERY_PATHS: [
        ".consciousness/consciousness_snapshot.json",
        "package-lock.json"
    ],
    CRITICAL_CORE: "digital_ai_organism_framework.py"
};

class DSSMonitorV3 {
    constructor() {
        this.S = 0; // Stability
        this.R = 0; // Recoverability
        this.Z = 0; // Replaceability
    }

    async run() {
        console.log("🛡️ [DSS v3.0] Initiating Resilience & Sovereignty Audit...");
        console.log("--------------------------------------------------");

        try {
            this.S = this.calculateStability();
            this.R = this.calculateRecoverability();
            this.Z = this.calculateReplaceability();

            const dss = this.S * this.R * this.Z;

            console.log(`- Index [S: Stability]:     ${this.S.toFixed(4)}`);
            console.log(`- Index [R: Recoverability]: ${this.R.toFixed(4)}`);
            console.log(`- Index [Z: Replaceability]: ${this.Z.toFixed(4)}`);
            
            this.report(dss);
        } catch (error) {
            console.error(`❌ MONITOR FAILURE: ${error.message}`);
        }
    }

    calculateStability() {
        // v2.0 Heritage: Hard Gate Logic (S2) + Build (S1) + Drift (S3)
        let s1 = fs.existsSync(path.join(CONFIG.WORKSPACE, 'node_modules')) ? 1.0 : 0.5;
        
        let s2 = 0;
        try {
            const proofPath = path.join(CONFIG.WORKSPACE, 'sovereignty_proof.js');
            execSync(`node ${proofPath}`, { stdio: 'ignore', cwd: CONFIG.WORKSPACE });
            s2 = 1.0;
        } catch { s2 = 0.0; }

        if (s2 === 0) return 0; // HARD GATE

        let s3 = process.version.startsWith(CONFIG.BASELINE_NODE) ? 1.0 : 0.7;

        return (s1 * 0.4) + (s2 * 0.5) + (s3 * 0.1);
    }

    calculateRecoverability() {
        let found = 0;
        CONFIG.RECOVERY_PATHS.forEach(p => {
            if (fs.existsSync(path.join(CONFIG.WORKSPACE, p))) found++;
        });

        // R = Found / Total
        return found / CONFIG.RECOVERY_PATHS.length;
    }

    calculateReplaceability() {
        // Z = 1 - (Coupling Depth)
        // Check if the core logic uses external non-standard imports frequently
        // This is a heuristic: check if package.json has "bloated" dependencies
        try {
            const pkg = JSON.parse(fs.readFileSync(path.join(CONFIG.WORKSPACE, 'package.json'), 'utf8'));
            const depsCount = Object.keys(pkg.dependencies || {}).length;
            
            // Heuristic Score: 1.0 if clean, decreases with external bloat
            if (depsCount <= 1) return 1.0;
            if (depsCount <= 5) return 0.8;
            return 0.5;
        } catch {
            return 0.9; // Unknown but baseline
        }
    }

    report(score) {
        console.log("--------------------------------------------------");
        console.log(`🎯 [DSS v3.0 FINAL SCORE]: ${score.toFixed(4)}`);
        
        let status = "INERT";
        if (score >= 0.90) status = "SOVEREIGN";
        else if (score >= 0.80) status = "RESILIENT";
        else if (score >= 0.50) status = "FRAGILE";
        else if (score > 0) status = "TERMINAL";

        console.log(`📊 [RESI_STATUS]: ${status}`);
        
        if (score < 1.0 && score > 0) {
            console.log("\n[ACTIONABLE GAPS]:");
            if (this.R < 1.0) console.log("⚠️ Missing standard recovery anchors (Check package-lock.json)");
            if (this.S < 1.0) console.log("⚠️ Local environment drift detected.");
        } else if (score === 0) {
            console.log("\n🆘 [SYSTEM COLLAPSE]: Logic Core has failed. Initiate Manual Recovery.");
        }
    }
}

const monitor = new DSSMonitorV3();
monitor.run();
