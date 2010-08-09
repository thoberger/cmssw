import FWCore.ParameterSet.Config as cms

L3SeedCombination = cms.EDProducer(
    "L3MuonTrajectorySeedCombiner",
    labels = cms.VInputTag(
    cms.InputTag("hltL3TrajSeedIOHit"),
    cms.InputTag("hltL3TrajSeedOIState"),
    cms.InputTag("hltL3TrajSeedOIHit")
    )
    )
