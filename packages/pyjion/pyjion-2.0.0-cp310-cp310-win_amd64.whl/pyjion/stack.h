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

#ifndef PYJION_STACK_H
#define PYJION_STACK_H

#include <vector>
#include <exception>

#include "block.h"


enum StackEntryKind {
    STACK_KIND_VALUE_FLOAT = 0,// An unboxed float
    STACK_KIND_VALUE_INT = 1,  // An unboxed int
    STACK_KIND_OBJECT = 2,     // A Python object, or a tagged int which might be an object
};

StackEntryKind avkAsStackEntryKind(AbstractValueKind k);
StackEntryKind lkAsStackEntryKind(LocalKind k);
LocalKind stackEntryKindAsLocalKind(StackEntryKind k);

class StackUnderflowException : public std::exception {
public:
    StackUnderflowException() : std::exception(){};
    const char* what() const noexcept override {
        return "Stack underflow";
    }
};

class ValueStack : std::vector<StackEntryKind> {

public:
    ValueStack() = default;

    ValueStack(ValueStack const& old) {
        for (size_t i = 0; i < old.size(); i++) {
            push_back(old[i]);
        }
    }

    void inc(size_t by, StackEntryKind kind);
    void dec(size_t by);

    using std::vector<StackEntryKind>::size;
    using std::vector<StackEntryKind>::rbegin;
    using std::vector<StackEntryKind>::begin;
    using std::vector<StackEntryKind>::rend;
    using std::vector<StackEntryKind>::end;
    using std::vector<StackEntryKind>::clear;

    void dup_top() {
        if (empty())
            throw StackUnderflowException();
        push_back(back());// does inc_stack
    }

    StackEntryKind peek(size_t n) {
        return std::vector<StackEntryKind>::at(size() - 1 - n);
    }
};

class BlockStack : std::vector<BlockInfo> {

public:
    BlockStack() = default;

    BlockStack(BlockStack const& old) {
        for (size_t i = 0; i < old.size(); i++) {
            push_back(old[i]);
        }
    }

    using vector<BlockInfo>::empty;
    using vector<BlockInfo>::push_back;
    using vector<BlockInfo>::emplace_back;
    using vector<BlockInfo>::size;
    using vector<BlockInfo>::rbegin;
    using vector<BlockInfo>::rend;

    void pop_back() {
        if (empty())
            throw StackUnderflowException();
        return vector<BlockInfo>::pop_back();
    }

    bool beyond(py_opindex curByte) {
        return (size() > 1 &&
                curByte >= back().EndOffset &&
                !back().Root);
    }

    BlockInfo back() {
        if (empty())
            throw StackUnderflowException();
        return vector<BlockInfo>::back();
    }

    BlockInfo get(size_t i) {
        return std::vector<BlockInfo>::at(i);
    }
};


class InterpreterStack : public std::vector<AbstractValueWithSources> {

public:
    AbstractValueWithSources top() {
        if (size() < 1)
            throw StackUnderflowException();
        return std::vector<AbstractValueWithSources>::at(size() - 1);
    }
    AbstractValueWithSources second() {
        if (size() < 2)
            throw StackUnderflowException();
        return std::vector<AbstractValueWithSources>::at(size() - 2);
    }
    AbstractValueWithSources third() {
        if (size() < 3)
            throw StackUnderflowException();
        return std::vector<AbstractValueWithSources>::at(size() - 3);
    }
    AbstractValueWithSources fourth() {
        if (size() < 4)
            throw StackUnderflowException();
        return std::vector<AbstractValueWithSources>::at(size() - 4);
    }
    AbstractValueWithSources nth(unsigned long n) {
        if (size() < n)
            throw StackUnderflowException();
        return std::vector<AbstractValueWithSources>::at(size() - n);
    }
};
#endif//PYJION_STACK_H
