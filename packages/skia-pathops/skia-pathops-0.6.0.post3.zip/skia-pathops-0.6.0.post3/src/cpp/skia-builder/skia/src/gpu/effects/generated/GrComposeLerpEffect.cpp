/*
 * Copyright 2019 Google LLC.
 *
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

/**************************************************************************************************
 *** This file was autogenerated from GrComposeLerpEffect.fp; do not modify.
 **************************************************************************************************/
#include "GrComposeLerpEffect.h"

#include "include/gpu/GrTexture.h"
#include "src/gpu/glsl/GrGLSLFragmentProcessor.h"
#include "src/gpu/glsl/GrGLSLFragmentShaderBuilder.h"
#include "src/gpu/glsl/GrGLSLProgramBuilder.h"
#include "src/sksl/SkSLCPP.h"
#include "src/sksl/SkSLUtil.h"
class GrGLSLComposeLerpEffect : public GrGLSLFragmentProcessor {
public:
    GrGLSLComposeLerpEffect() {}
    void emitCode(EmitArgs& args) override {
        GrGLSLFPFragmentBuilder* fragBuilder = args.fFragBuilder;
        const GrComposeLerpEffect& _outer = args.fFp.cast<GrComposeLerpEffect>();
        (void)_outer;
        auto weight = _outer.weight;
        (void)weight;
        weightVar =
                args.fUniformHandler->addUniform(kFragment_GrShaderFlag, kFloat_GrSLType, "weight");
        SkString _sample290("_sample290");
        if (_outer.child1_index >= 0) {
            this->invokeChild(_outer.child1_index, &_sample290, args);
        } else {
            fragBuilder->codeAppendf("half4 %s;", _sample290.c_str());
        }
        SkString _sample358("_sample358");
        if (_outer.child2_index >= 0) {
            this->invokeChild(_outer.child2_index, &_sample358, args);
        } else {
            fragBuilder->codeAppendf("half4 %s;", _sample358.c_str());
        }
        fragBuilder->codeAppendf("%s = mix(%s ? %s : %s, %s ? %s : %s, half(%s));\n",
                                 args.fOutputColor, _outer.child1_index >= 0 ? "true" : "false",
                                 _sample290.c_str(), args.fInputColor,
                                 _outer.child2_index >= 0 ? "true" : "false", _sample358.c_str(),
                                 args.fInputColor, args.fUniformHandler->getUniformCStr(weightVar));
    }

private:
    void onSetData(const GrGLSLProgramDataManager& pdman,
                   const GrFragmentProcessor& _proc) override {
        const GrComposeLerpEffect& _outer = _proc.cast<GrComposeLerpEffect>();
        { pdman.set1f(weightVar, (_outer.weight)); }
    }
    UniformHandle weightVar;
};
GrGLSLFragmentProcessor* GrComposeLerpEffect::onCreateGLSLInstance() const {
    return new GrGLSLComposeLerpEffect();
}
void GrComposeLerpEffect::onGetGLSLProcessorKey(const GrShaderCaps& caps,
                                                GrProcessorKeyBuilder* b) const {}
bool GrComposeLerpEffect::onIsEqual(const GrFragmentProcessor& other) const {
    const GrComposeLerpEffect& that = other.cast<GrComposeLerpEffect>();
    (void)that;
    if (weight != that.weight) return false;
    return true;
}
GrComposeLerpEffect::GrComposeLerpEffect(const GrComposeLerpEffect& src)
        : INHERITED(kGrComposeLerpEffect_ClassID, src.optimizationFlags())
        , child1_index(src.child1_index)
        , child2_index(src.child2_index)
        , weight(src.weight) {
    if (child1_index >= 0) {
        this->registerChildProcessor(src.childProcessor(child1_index).clone());
    }
    if (child2_index >= 0) {
        this->registerChildProcessor(src.childProcessor(child2_index).clone());
    }
}
std::unique_ptr<GrFragmentProcessor> GrComposeLerpEffect::clone() const {
    return std::unique_ptr<GrFragmentProcessor>(new GrComposeLerpEffect(*this));
}
