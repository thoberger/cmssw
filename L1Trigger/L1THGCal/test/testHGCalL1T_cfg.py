import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('DIGI',eras.Phase2C2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D3Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D3_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedGauss_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('SingleElectronPt10_cfi nevts:10'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    #outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    outputCommands = cms.untracked.vstring(
        'keep *_*_HGCHitsEE_*',
        'keep *_*_HGCHitsHEback_*',
        'keep *_*_HGCHitsHEfront_*',
        'keep *_mix_*_*',
        'keep *_genParticles_*_*',
        'keep *_hgcalTriggerPrimitiveDigiProducer_*_*'
    ),
    fileName = cms.untracked.string('file:test.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.generator = cms.EDProducer("FlatRandomPtGunProducer",
    PGunParameters = cms.PSet(
        MaxPt = cms.double(50.01),
        MinPt = cms.double(49.99),
        PartID = cms.vint32(11),
        MaxEta = cms.double(1.5),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(3.),
        MinPhi = cms.double(-3.14159265359)
    ),
    Verbosity = cms.untracked.int32(0),
    psethack = cms.string('single electron pt 100'),
    AddAntiParticle = cms.bool(True),
    firstRun = cms.untracked.uint32(1)
)

process.mix.digitizers = cms.PSet(process.theDigitizersValid)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)

process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
# Remove best choice selection
process.hgcalTriggerPrimitiveDigiProducer.FECodec.NData = cms.uint32(999)
cluster_algo_all =  cms.PSet( AlgorithmName = cms.string('SingleCellClusterAlgo'),
                                 FECodec = process.hgcalTriggerPrimitiveDigiProducer.FECodec )
process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms = cms.VPSet( cluster_algo_all )
process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)

process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.hgcl1tpg_step,process.digi2raw_step,process.endjob_step, process.FEVTDEBUGoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
        getattr(process,path)._seq = process.generator * getattr(process,path)._seq

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023tilted

#call to customisation function cust_2023tilted imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023tilted(process)

# End of customisation functions



