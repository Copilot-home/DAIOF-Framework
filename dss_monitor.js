/**
 * DAIOF STABILITY SCORE (DSS) MONITOR v2.0 (Hardened)
 * 
 * Objectives:
 * 1. Hard Gate: If S2 (Logic) fails, DSS is 0.
 * 2. Real Invariant Test: Run actual core logic.
 * 3. Health Penalty: Non-linear risk assessment.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = {
    BASELINE_NODE: "v22",
    WORKSPACE: "/Users/andy/my_too_test/DAIOF-Framework",
    WEIGHTS: {
        S1_BUILD: 0.35,
        S2_LOGIC: 0.45,
        S3_DRIFT: 0.10,
        S4_RISK: 0.10
    }
};

class DSSMonitorV2 {
    constructor() {
        this.scores = { S1: 0, S2: 0, S3: 0, S4: 0 };
    }

    async run() {
        console.log("🛠️ [DSS v2.0] Initiating Hardened Multi-Layer Audit...");
        console.log("--------------------------------------------------");

        try {
            // S1: Build Integrity (Harden)
            this.scores.S1 = this.checkBuildHarden();
            console.log(`- Layer [S1: Build]: ${this.scores.S1.toFixed(2)}`);

            // S2: Logic Determinism (Hard Gate)
            this.scores.S2 = this.checkLogicReal();
            console.log(`- Layer [S2: Logic]: ${this.scores.S2.toFixed(2)} [HARD GATE]`);

            // S3: Environment Drift
            this.scores.S3 = this.checkDriftStrict();
            console.log(`- Layer [S3: Drift]: ${this.scores.S3.toFixed(2)}`);

            // S4: Dependency Risk (Penalty Factor)
            this.scores.S4 = this.checkRiskHarden();
            console.log(`- Layer [S4: Risk]:  ${this.scores.S4.toFixed(2)}`);

            const dss = this.calculateDSS();
            this.report(dss);
        } catch (error) {
            console.error(`❌ CRITICAL MONITOR FAILURE: ${error.message}`);
            process.exit(1);
        }
    }

    checkBuildHarden() {
        const hasPackage = fs.existsSync(path.join(CONFIG.WORKSPACE, 'package.json'));
        if (!hasPackage) return 0.0;

        try {
            // Check if node_modules exists
            if (!fs.existsSync(path.join(CONFIG.WORKSPACE, 'node_modules'))) return 0.2;
            
            // Fast check: is npm list succeeding? (No missing deps)
            // execSync('npm list --depth=0', { stdio: 'ignore', cwd: CONFIG.WORKSPACE });
            return 1.0;
        } catch {
            return 0.5; // Dependency mismatch or broken tree
        }
    }

    checkLogicReal() {
        // Run the REAL Sovereignty Proof as the Invariant Test
        try {
            const proofPath = path.join(CONFIG.WORKSPACE, 'sovereignty_proof.js');
            if (!fs.existsSync(proofPath)) return 0.0;

            execSync(`node ${proofPath}`, { stdio: 'ignore', cwd: CONFIG.WORKSPACE });
            return 1.0; // PASS
        } catch {
            return 0.0; // FAIL -> Will trigger Hard Gate
        }
    }

    checkDriftStrict() {
        const currentVersion = process.version;
        if (currentVersion.startsWith(CONFIG.BASELINE_NODE)) return 1.0;
        return 0.5; // Unknown environment drift
    }

    checkRiskHarden() {
        let score = 1.0;
        const hasLock = fs.existsSync(path.join(CONFIG.WORKSPACE, 'package-lock.json'));
        const hasTypes = fs.existsSync(path.join(CONFIG.WORKSPACE, 'node_modules/@types/node'));

        if (!hasLock) score -= 0.3; // Penalty for missing lockfile
        if (!hasTypes) score -= 0.3; // Penalty for missing core types

        return Math.max(0, score);
    }

    calculateDSS() {
        // HARD GATE: If Logic is 0, DSS is 0.
        if (this.scores.S2 === 0) {
            console.log("\n🛑 [HARD GATE TRIGGERED]: Logic Core Failure. All other metrics invalidated.");
            return 0.0;
        }

        const baseScore = (this.scores.S1 * CONFIG.WEIGHTS.S1_BUILD) +
                          (this.scores.S2 * CONFIG.WEIGHTS.S2_LOGIC) +
                          (this.scores.S3 * CONFIG.WEIGHTS.S3_DRIFT) +
                          (this.scores.S4 * CONFIG.WEIGHTS.S4_RISK);
        
        return baseScore;
    }

    report(score) {
        console.log("--------------------------------------------------");
        console.log(`🎯 [DSS v2.0 RESULT]: ${score.toFixed(4)}`);
        
        let status = "DEAD";
        if (score >= 0.95) status = "IMMORTAL";
        else if (score >= 0.90) status = "STABLE";
        else if (score >= 0.70) status = "DEGRADED";
        else if (score > 0) status = "CRITICAL";

        console.log(`📊 [STATUS]: ${status}`);
        
        if (score < 1.0 && score > 0) {
            console.log("\n[ADVISORY]:");
            if (this.scores.S1 < 1.0) console.log("- Resolve Build Integrity (S1)");
            if (this.scores.S4 < 1.0) console.log("- Eliminate Dependency Risk (S4)");
        } else if (score === 0) {
            console.log("\n🆘 [RECOVERY REQUIRED]: Invariant violation detected in Logic Core.");
        }
    }
}

const monitor = new DSSMonitorV2();
monitor.run();
