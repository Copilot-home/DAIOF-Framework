"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.MementoKeyValueStorage = void 0;
class MementoKeyValueStorage {
    constructor(mementoGlobalStorage) {
        this.mementoGlobalStorage = mementoGlobalStorage;
    }
    async getValue(key, defaultValue) {
        const value = await this.mementoGlobalStorage.get(key);
        return value || defaultValue;
    }
    setValue(key, value) {
        this.mementoGlobalStorage.update(key, value);
    }
}
exports.MementoKeyValueStorage = MementoKeyValueStorage;
//# sourceMappingURL=MementoKeyValueStorage.js.map