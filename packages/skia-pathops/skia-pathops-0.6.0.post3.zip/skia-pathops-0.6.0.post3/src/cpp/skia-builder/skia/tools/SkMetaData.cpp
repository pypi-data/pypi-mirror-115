/*
 * Copyright 2006 The Android Open Source Project
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

#include "tools/SkMetaData.h"

#include "include/private/SkMalloc.h"
#include "include/private/SkTo.h"

void SkMetaData::reset()
{
    Rec* rec = fRec;
    while (rec) {
        Rec* next = rec->fNext;
        Rec::Free(rec);
        rec = next;
    }
    fRec = nullptr;
}

void SkMetaData::setS32(const char name[], int32_t value)
{
    (void)this->set(name, &value, sizeof(int32_t), kS32_Type, 1);
}

void SkMetaData::setScalar(const char name[], SkScalar value)
{
    (void)this->set(name, &value, sizeof(SkScalar), kScalar_Type, 1);
}

SkScalar* SkMetaData::setScalars(const char name[], int count, const SkScalar values[])
{
    SkASSERT(count > 0);
    if (count > 0)
        return (SkScalar*)this->set(name, values, sizeof(SkScalar), kScalar_Type, count);
    return nullptr;
}

void SkMetaData::setPtr(const char name[], void* ptr) {
    (void)this->set(name, &ptr, sizeof(void*), kPtr_Type, 1);
}

void SkMetaData::setBool(const char name[], bool value)
{
    (void)this->set(name, &value, sizeof(bool), kBool_Type, 1);
}

void* SkMetaData::set(const char name[], const void* data, size_t dataSize, Type type, int count)
{
    SkASSERT(name);
    SkASSERT(dataSize);
    SkASSERT(count > 0);

    (void)this->remove(name, type);

    size_t  len = strlen(name);
    Rec*    rec = Rec::Alloc(sizeof(Rec) + dataSize * count + len + 1);

#ifndef SK_DEBUG
    rec->fType = SkToU8(type);
#else
    rec->fType = type;
#endif
    rec->fDataLen = SkToU8(dataSize);
    rec->fDataCount = SkToU16(count);
    if (data)
        memcpy(rec->data(), data, dataSize * count);
    memcpy(rec->name(), name, len + 1);

    rec->fNext = fRec;
    fRec = rec;
    return rec->data();
}

bool SkMetaData::findS32(const char name[], int32_t* value) const
{
    const Rec* rec = this->find(name, kS32_Type);
    if (rec)
    {
        SkASSERT(rec->fDataCount == 1);
        if (value)
            *value = *(const int32_t*)rec->data();
        return true;
    }
    return false;
}

bool SkMetaData::findScalar(const char name[], SkScalar* value) const
{
    const Rec* rec = this->find(name, kScalar_Type);
    if (rec)
    {
        SkASSERT(rec->fDataCount == 1);
        if (value)
            *value = *(const SkScalar*)rec->data();
        return true;
    }
    return false;
}

const SkScalar* SkMetaData::findScalars(const char name[], int* count, SkScalar values[]) const
{
    const Rec* rec = this->find(name, kScalar_Type);
    if (rec)
    {
        if (count)
            *count = rec->fDataCount;
        if (values)
            memcpy(values, rec->data(), rec->fDataCount * rec->fDataLen);
        return (const SkScalar*)rec->data();
    }
    return nullptr;
}

bool SkMetaData::findPtr(const char name[], void** ptr) const {
    const Rec* rec = this->find(name, kPtr_Type);
    if (rec) {
        SkASSERT(rec->fDataCount == 1);
        void** found = (void**)rec->data();
        if (ptr) {
            *ptr = *found;
        }
        return true;
    }
    return false;
}

bool SkMetaData::findBool(const char name[], bool* value) const
{
    const Rec* rec = this->find(name, kBool_Type);
    if (rec)
    {
        SkASSERT(rec->fDataCount == 1);
        if (value)
            *value = *(const bool*)rec->data();
        return true;
    }
    return false;
}

const SkMetaData::Rec* SkMetaData::find(const char name[], Type type) const
{
    const Rec* rec = fRec;
    while (rec)
    {
        if (rec->fType == type && !strcmp(rec->name(), name))
            return rec;
        rec = rec->fNext;
    }
    return nullptr;
}

bool SkMetaData::remove(const char name[], Type type) {
    Rec* rec = fRec;
    Rec* prev = nullptr;
    while (rec) {
        Rec* next = rec->fNext;
        if (rec->fType == type && !strcmp(rec->name(), name)) {
            if (prev) {
                prev->fNext = next;
            } else {
                fRec = next;
            }
            Rec::Free(rec);
            return true;
        }
        prev = rec;
        rec = next;
    }
    return false;
}

bool SkMetaData::removeS32(const char name[])
{
    return this->remove(name, kS32_Type);
}

bool SkMetaData::removeScalar(const char name[])
{
    return this->remove(name, kScalar_Type);
}

bool SkMetaData::removePtr(const char name[])
{
    return this->remove(name, kPtr_Type);
}

bool SkMetaData::removeBool(const char name[])
{
    return this->remove(name, kBool_Type);
}

///////////////////////////////////////////////////////////////////////////////

SkMetaData::Iter::Iter(const SkMetaData& metadata) {
    fRec = metadata.fRec;
}

void SkMetaData::Iter::reset(const SkMetaData& metadata) {
    fRec = metadata.fRec;
}

const char* SkMetaData::Iter::next(SkMetaData::Type* t, int* count) {
    const char* name = nullptr;

    if (fRec) {
        if (t) {
            *t = (SkMetaData::Type)fRec->fType;
        }
        if (count) {
            *count = fRec->fDataCount;
        }
        name = fRec->name();

        fRec = fRec->fNext;
    }
    return name;
}

///////////////////////////////////////////////////////////////////////////////

SkMetaData::Rec* SkMetaData::Rec::Alloc(size_t size) {
    return (Rec*)sk_malloc_throw(size);
}

void SkMetaData::Rec::Free(Rec* rec) {
    sk_free(rec);
}
