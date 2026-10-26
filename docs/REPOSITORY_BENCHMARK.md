# Repository structure benchmark

Observed on 26 October 2026 from the projects' own public repositories. These are established community projects selected for visible sustained development, reusable artifacts and documentation. This is a qualitative structure comparison, not a clinical-quality ranking or a claim that GitHub popularity measures safety.

| Project | Observed structure/style | Endorys adaptation |
|---|---|---|
| [3D Slicer](https://github.com/Slicer/Slicer) | Dedicated Docs, modules and testing; prominent contribution, governance, security and citation resources; short README routes readers to documentation/community | Short root page, guided docs portal and visible community files |
| [ITK](https://github.com/InsightSoftwareConsortium/ITK) | Documentation, Examples, Modules and Testing separated; GettingStarted, citation and governance entry points | Reproducible quick start, clear engineering references and citation |
| [MONAI](https://github.com/Project-MONAI/MONAI) | docs, implementation and tests separated; changelog, contribution and security files are easy to find | Changelog, project status, contributor workflow and honest runnable-example scope |
| [OpenEMR](https://github.com/openemr/openemr) | Documentation, application source, APIs and tests have distinct homes; community and security policies are exposed | Reader-specific paths and separate security reporting; no claim Endorys has comparable deployment maturity |
| [echomods](https://github.com/kelu124/echomods) | Ultrasound building blocks, module interfaces, dated experiment logs and raw-source links; scope limits explicitly distinguish a development kit from a medical scanner | Measurement contracts, experiment records, provenance and explicit research status |

## Assessment of the previous Endorys layout

Strengths: broad scope was preserved; proof gaps were explicit; technical reviews and concepts were already public.

Weaknesses: a naming table dominated the overview; research files were presented alphabetically; contribution instructions were buried; a newcomer could not quickly distinguish runnable material from future hardware or clinical capabilities.

## Changes adopted

- Overview first, details through a documentation hub.
- Reading paths for understanding, evaluating, engineering and contributing.
- Thematic catalogue covering all current material.
- Prominent maturity table, experiment priority and reproducible command.
- Root contribution, conduct, security and changelog files.
- Real issue/PR templates in GitHub's recognized locations.
- Stable existing links and no duplicated long technical sources.

## Practices deferred deliberately

Do not imitate installation instructions for a nonexistent device, copy other projects' license choices, display unsupported medical certifications, or add badges for tests not running in this repository. A polished structure cannot substitute for physical measurements. Large-scale packaging, hosted documentation builds and hardware releases should follow actual maintained artifacts.

These are structural observations and Endorys-specific judgments. They do not imply affiliation or endorsement by the projects studied.
