/*
* The MIT License (MIT)
*
* Copyright (c) Microsoft Corporation
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
* OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
* ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
* OTHER DEALINGS IN THE SOFTWARE.
*
*/

#ifndef PYJION_CODEMODEL_H
#define PYJION_CODEMODEL_H

#include <stdint.h>
#include <wchar.h>
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <float.h>
#include <cstdlib>

#include <utility>
#include <vector>
#include <unordered_map>

#include "crossplat.h"
#include <corjit.h>

#include <Python.h>

#include "exceptions.h"
#include "base.h"

#define METHOD_SLOT_SPACE 0x00100000

using namespace std;
typedef std::unordered_map<int32_t, const char*> SymbolTable;

class Method;
class BaseMethod;
class CorClass;

class Parameter : public PyjionBase {
public:
    CorInfoType m_type;
    explicit Parameter(CorInfoType type) {
        m_type = type;
    }
};

class BaseModule : public PyjionBase {
    unordered_map<void*, int> existingSlots;
    int slotCursor = 0;

public:
    unordered_map<int32_t, BaseMethod*> m_methods;
    SymbolTable symbolTable;
    BaseModule() = default;

    virtual BaseMethod* ResolveMethod(int32_t tokenId) {
        return m_methods[tokenId];
    }

    virtual int AddMethod(CorInfoType returnType, std::vector<Parameter> params, void* addr, const char* label = "typeslot");
    virtual void RegisterSymbol(int32_t tokenId, const char* label);
    virtual SymbolTable GetSymbolTable();
};

class UserModule : public BaseModule {
    BaseModule& m_parent;

public:
    explicit UserModule(BaseModule& parent) : m_parent(parent) {
    }

    BaseMethod* ResolveMethod(int32_t tokenId) override {
        auto res = m_methods.find(tokenId);
        if (res == m_methods.end()) {
            return m_parent.ResolveMethod(tokenId);
        }

        return res->second;
    }

    SymbolTable GetSymbolTable() override {
        return m_parent.GetSymbolTable();
    }
};

struct SequencePoint {
    uint32_t ilOffset;
    uint32_t nativeOffset;
    uint32_t pythonOpcodeIndex;
};

struct CallPoint {
    uint32_t ilOffset;
    uint32_t nativeOffset;
    int32_t tokenId;
};

class BaseMethod : public PyjionBase {
public:
    virtual void getCallInfo(CORINFO_CALL_INFO* pResult) = 0;
    virtual uint32_t getMethodAttrs() = 0;
    virtual void findSig(CORINFO_SIG_INFO* sig) = 0;
    virtual void* getAddr() = 0;
    virtual void getFunctionEntryPoint(CORINFO_CONST_LOOKUP* pResult) = 0;
    virtual unsigned int getSequencePointCount() = 0;
    virtual uint32_t* getSequencePointOffsets() = 0;
    virtual void recordSequencePointOffsetPosition(uint32_t ilOffset, uint32_t nativeOffset) = 0;
    virtual void recordCallPointOffsetPosition(uint32_t ilOffset, uint32_t nativeOffset) = 0;
    virtual vector<SequencePoint> getSequencePoints() = 0;
    virtual vector<CallPoint> getCallPoints() = 0;
    virtual bool isIntrinsic() = 0;
};

class JITMethod : public BaseMethod {
    BaseModule* m_module;

public:
    vector<Parameter> m_params;
    CorInfoType m_retType;
    void* m_addr;
    vector<SequencePoint> m_sequencePoints;
    vector<CallPoint> m_callPoints;
    bool m_hasIntrinsics;

    JITMethod(BaseModule* module, CorInfoType returnType, std::vector<Parameter> params, void* addr, bool intrinsics) {
        m_retType = returnType;
        m_params = std::move(params);
        m_module = module;
        m_addr = addr;
        m_hasIntrinsics = intrinsics;
    }

    JITMethod(BaseModule* module, CorInfoType returnType, vector<Parameter> params, void* addr,
              const vector<pair<size_t, uint32_t>>& sequencePoints,
              const vector<pair<size_t, int32_t>>& callPoints,
              bool hasIntrinsics) : JITMethod(module, returnType, std::move(params), addr, hasIntrinsics) {
        for (auto& point : sequencePoints) {
            m_sequencePoints.push_back({static_cast<uint32_t>(point.first),
                                        0,
                                        point.second});
        }

        for (auto& point : callPoints) {
            m_callPoints.push_back({static_cast<uint32_t>(point.first),
                                    0,
                                    point.second});
        }
    }

    void* getAddr() override {
        return m_addr;
    }

    uint32_t getMethodAttrs() override {
        if (m_hasIntrinsics) {
            return CORINFO_FLG_STATIC | CORINFO_FLG_NATIVE | CORINFO_FLG_INTRINSIC;
        } else {
            return CORINFO_FLG_STATIC | CORINFO_FLG_NATIVE;
        }
    }

    void getCallInfo(CORINFO_CALL_INFO* pResult) override {
        pResult->codePointerLookup.lookupKind.needsRuntimeLookup = false;
        pResult->codePointerLookup.constLookup.accessType = IAT_PVALUE;
        pResult->codePointerLookup.constLookup.addr = &m_addr;
        if (m_hasIntrinsics) {
            pResult->verMethodFlags = pResult->methodFlags = CORINFO_FLG_STATIC | CORINFO_FLG_INTRINSIC;
        } else {
            pResult->verMethodFlags = pResult->methodFlags = CORINFO_FLG_STATIC;
        }
        pResult->kind = CORINFO_CALL;
        pResult->sig.args = (CORINFO_ARG_LIST_HANDLE) (m_params.empty() ? nullptr : &m_params[0]);
        pResult->sig.retType = m_retType;
        pResult->sig.numArgs = m_params.size();
    }
    void findSig(CORINFO_SIG_INFO* sig) override {
        sig->retType = m_retType;
        sig->callConv = CORINFO_CALLCONV_DEFAULT;
        sig->retTypeClass = nullptr;
        sig->retTypeSigClass = nullptr;
        sig->args = (CORINFO_ARG_LIST_HANDLE) (!m_params.empty() ? &m_params[0] : nullptr);
        sig->numArgs = m_params.size();
        sig->sigInst.classInstCount = 0;
        sig->sigInst.classInst = nullptr;
        sig->sigInst.methInstCount = 0;
        sig->sigInst.methInst = nullptr;
    }
    void getFunctionEntryPoint(CORINFO_CONST_LOOKUP* pResult) override {
        pResult->accessType = IAT_PVALUE;
        pResult->addr = &m_addr;
    }

    unsigned int getSequencePointCount() override {
        return static_cast<unsigned int>(m_sequencePoints.size());
    }

    uint32_t* getSequencePointOffsets() override {
        auto* pts = static_cast<uint32_t*>(PyMem_RawMalloc(sizeof(uint32_t) * m_sequencePoints.size()));
        if (pts == nullptr) {
            throw OutOfMemoryException();
        }
        size_t i = 0;
        for (auto& p : m_sequencePoints) {
            pts[i] = p.ilOffset;
            i++;
        }
        return pts;
    }

    void recordSequencePointOffsetPosition(uint32_t ilOffset, uint32_t nativeOffset) override {
        for (auto& pt : m_sequencePoints) {
            if (pt.ilOffset == ilOffset) {
                pt.nativeOffset = nativeOffset;
            }
        }
    }

    void recordCallPointOffsetPosition(uint32_t ilOffset, uint32_t nativeOffset) override {
        for (auto& pt : m_callPoints) {
            if (pt.ilOffset == ilOffset) {
                pt.nativeOffset = nativeOffset;
            }
        }
    }

    vector<SequencePoint> getSequencePoints() override {
        return m_sequencePoints;
    }

    vector<CallPoint> getCallPoints() override {
        return m_callPoints;
    }

    bool isIntrinsic() override {
        return m_hasIntrinsics;
    }
};


#endif