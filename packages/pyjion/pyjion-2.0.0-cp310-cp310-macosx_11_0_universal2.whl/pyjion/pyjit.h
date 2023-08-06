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

#ifndef PYJION_PYJIT_H
#define PYJION_PYJIT_H

#include <cstdint>
#include <cwchar>
#include <cstdio>
#include <cstddef>
#include <cstdlib>
#include <climits>
#include <cstring>
#include <cfloat>

#include <vector>
#include <unordered_map>

#include <Python.h>
#include <frameobject.h>
#include "ipycomp.h"

#include "codemodel.h"
#include "absvalue.h"
#include "attrtable.h"

using namespace std;

enum OptimizationFlags {
    InlineIs = 1,          // OPT-1
    InlineDecref = 2,      // OPT-2
    InternRichCompare = 4, // OPT-3
    InlineFramePushPop = 8,// OPT-5
    KnownStoreSubscr = 16, // OPT-6
    KnownBinarySubscr = 32,// OPT-7
    InlineIterators = 64,  // OPTIMIZE_ITERATORS; // OPT-9
    HashedNames = 128,     // OPTIMIZE_HASHED_NAMES; // OPT-10
    BuiltinMethods = 256,  // OPTIMIZE_BUILTIN_METHODS; // OPT-12
    TypeSlotLookups = 512, //OPTIMIZE_TYPESLOT_LOOKUPS; // OPT-13
    FunctionCalls = 1024,  // OPTIMIZE_FUNCTION_CALLS; // OPT-14
    LoadAttr = 2048,       // OPTIMIZE_LOAD_ATTR; // OPT-15
    Unboxing = 4096,       // OPTIMIZE_UNBOXING; // OPT-16
    AttrTypeTable = 8192,         // OPTIMIZE_ISNONE; // OPT-17
    IntegerUnboxingMultiply = 16384,
    OptimisticIntegers = 32768
};

class PyjionCodeProfile : public PyjionBase {
    unordered_map<size_t, unordered_map<size_t, PyTypeObject*>> stackTypes;
    unordered_map<size_t, unordered_map<size_t, AbstractValueKind>> stackKinds;

public:
    void record(size_t opcodePosition, size_t stackPosition, PyObject* obj);
    PyTypeObject* getType(size_t opcodePosition, size_t stackPosition);
    AbstractValueKind getKind(size_t opcodePosition, size_t stackPosition);
    ~PyjionCodeProfile();
};

void capturePgcStackValue(PyjionCodeProfile* profile, PyObject* value, size_t opcodePosition, size_t stackPosition);
class PyjionJittedCode;

bool JitInit(const wchar_t* jitpath);
PyObject* PyJit_ExecuteAndCompileFrame(PyjionJittedCode* state, PyFrameObject* frame, PyThreadState* tstate, PyjionCodeProfile* profile);
static inline PyObject* PyJit_CheckFunctionResult(PyThreadState* tstate, PyObject* result, PyFrameObject* frame);
static inline PyObject* PyJit_ExecuteJittedFrame(void* state, PyFrameObject* frame, PyThreadState* tstate, PyjionJittedCode*);
PyObject* PyJit_EvalFrame(PyThreadState*, PyFrameObject*, int);
PyjionJittedCode* PyJit_EnsureExtra(PyObject* codeObject);

// This type isn't exported in the Python 3.10 API, so define it here.
typedef struct {
    PyCodeObject* code;       // The code object for the bounds. May be NULL.
    PyCodeAddressRange bounds;// Only valid if code != NULL.
    CFrame cframe;
} PyTraceInfo;

typedef PyObject* (*Py_EvalFunc)(PyjionJittedCode*, struct _frame*, PyThreadState*, PyjionCodeProfile*, PyTraceInfo*);


inline OptimizationFlags operator|(OptimizationFlags a, OptimizationFlags b) {
    return static_cast<OptimizationFlags>(static_cast<int>(a) | static_cast<int>(b));
}
inline OptimizationFlags operator&(OptimizationFlags a, OptimizationFlags b) {
    return static_cast<OptimizationFlags>(static_cast<int>(a) & static_cast<int>(b));
}

typedef struct PyjionSettings {
    bool pgc = true;   // Profile-guided-compilation
    bool graph = false;// Generate instruction graphs
    uint8_t optimizationLevel = 1;
    uint8_t threshold = 0;
    uint32_t recursionLimit = DEFAULT_RECURSION_LIMIT;
    uint32_t codeObjectSizeLimit = DEFAULT_CODEOBJECT_SIZE_LIMIT;
#ifdef DEBUG
    DebugMode debug = DebugMode::Debug;
#else
    DebugMode debug = DebugMode::Release;
#endif
    bool exceptionHandling = false;
    const wchar_t* clrjitpath = L"";

    // Optimizations
    OptimizationFlags optimizations = OptimizationFlags();
} PyjionSettings;

extern PyjionSettings g_pyjionSettings;
extern AttributeTable* g_attrTable;

#define OPT_ENABLED(opt) ((g_pyjionSettings.optimizations & (opt)) == (opt))
void PyjionJitFree(void* obj);

int Pyjit_CheckRecursiveCall(PyThreadState* tstate, const char* where);
static int Pyjit_EnterRecursiveCall(const char* where);
static void Pyjit_LeaveRecursiveCall();


/* Jitted code object.  This object is returned from the JIT implementation.  The JIT can allocate
a jitted code object and fill in the state for which is necessary for it to perform an evaluation. */
enum PgcStatus {
    Uncompiled = 0,
    CompiledWithProbes = 1,
    Optimized = 2
};

PgcStatus nextPgcStatus(PgcStatus status);

class PyjionJittedCode {
public:
    PY_UINT64_T j_runCount;
    bool j_failed;
    short j_compileResult;
    unsigned int j_optimizations;
    Py_EvalFunc j_addr;
    Py_EvalFunc j_genericAddr;
    uint8_t j_threshold;
    PyObject* j_code;
    PyjionCodeProfile* j_profile;
    unsigned char* j_il;
    unsigned int j_ilLen;
    unsigned long j_nativeSize;
    PgcStatus j_pgcStatus;
    SequencePoint* j_sequencePoints;
    unsigned int j_sequencePointsLen;
    CallPoint* j_callPoints;
    unsigned int j_callPointsLen;
    PyObject* j_graph;
    PyObject* j_genericGraph;
    SymbolTable j_symbols;
    bool j_tracingHooks;
    bool j_profilingHooks;
    AbstractValueKind* j_specializedKinds;
    unsigned int j_specializedKindsLen;

    explicit PyjionJittedCode(PyObject* code) {
        j_compileResult = 0;
        j_optimizations = 0;
        j_code = code;
        j_runCount = 0;
        j_failed = false;
        j_addr = nullptr;
        j_genericAddr = nullptr;
        j_threshold = g_pyjionSettings.threshold;
        j_il = nullptr;
        j_ilLen = 0;
        j_nativeSize = 0;
        j_profile = new PyjionCodeProfile();
        j_graph = Py_None;
        j_genericGraph = Py_None;
        j_pgcStatus = Uncompiled;
        j_sequencePoints = nullptr;
        j_sequencePointsLen = 0;
        j_callPoints = nullptr;
        j_callPointsLen = 0;
        j_tracingHooks = false;
        j_profilingHooks = false;
        j_specializedKinds = nullptr;
        j_specializedKindsLen = 0;
        Py_INCREF(code);
    }

    ~PyjionJittedCode();
    void reset();

    PyjionJittedCode& operator = (const PyjionJittedCode& code);
};

void setOptimizationLevel(unsigned short level);
extern PyObject* PyjionUnboxingError;
#ifdef WINDOWS
HMODULE GetClrJit();
#endif

#endif
