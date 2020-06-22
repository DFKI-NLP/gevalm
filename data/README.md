# GEvaLM Dataset

This folder includes the script used to generate the dataset (`create_dataset.py`),a list of lexical items used for the sentences (`list_lexical_items.txt`) as well as the actual dataset. To create the dataset, execute  `python create_dataset.py` . The dataset will be saved in `/dataset/input`. The output of the experiments can be found in `dataset/output`.

### Abbrevations

A list of Abbrevations used inside the dataset-folder. Inside the table, Subject-Verb-Agreement is abbreviated "SVA".

| Test-Case Name                                               | Test-Case Short-Name |
| ------------------------------------------------------------ | :------------------: |
| Simple sentence                                              |      SimplSent       |
| SVA in a sentential complement                               |    SVinSentCompl     |
| SVA in an object relative clause                             |     SVinObjRelC      |
| SVA across a prepositional phrase                            |         SVPP         |
| SVA across a subject relative clause                         |      SVSubjRelC      |
| SVA   across   an   object   relativeclause                  |     SVinObjRelC      |
| SVA in short VP coordinations                                |    SVshortVPCoord    |
| SVA in medium VP coordinations                               |   SVmediumVPCoord    |
| SVA in long VP coordinations                                 |    SVlongVPCoord     |
| SVA with a simple modifier                                   |      SVModifier      |
| SVA with an extended modifier                                |  SVextendedModifier  |
| Pre-field                                                    |        SVVorf        |
| Subject  RA  agreement (testing person-agreement, all accusative) |        RA_acc        |
| Subject RA agreement (testing case-agreement)                |       RA_case        |

