"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
class TelemetryDisabledExperimentationService {
    constructor() {
        this.initializePromise = Promise.resolve();
        this.initialFetch = Promise.resolve();
    }
    isFlightEnabled(flight) {
        return false;
    }
    isCachedFlightEnabled(flight) {
        return Promise.resolve(false);
    }
    isFlightEnabledAsync(flight) {
        return Promise.resolve(false);
    }
    getTreatmentVariable(configId, name) {
        return undefined;
    }
    getTreatmentVariableAsync(configId, name) {
        return Promise.resolve(undefined);
    }
}
exports.default = TelemetryDisabledExperimentationService;
//# sourceMappingURL=TelemetryDisabledExperimentationService.js.map