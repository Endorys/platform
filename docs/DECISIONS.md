# Architecture and repository decisions

## ADR-001: Guided documentation over a flat reading list

Date: 26 October 2026. Status: adopted for repository organization.

Context: Endorys has many branches, images and long research reviews. A long root page with historical aliases and an alphabetical file list makes first-time evaluation difficult.

Decision: keep a concise root overview; provide docs/ as the guided portal; retain detailed research/ sources and image provenance. Existing branch and research URLs remain valid.

Consequences: newcomers can choose an overview, engineering or evidence path. Maintainers must update the catalogue whenever files change. Root branch pages remain stable compatibility entry points.

## ADR-002: Evidence status before product language

Status: adopted. Separate proposed, synthetic, physical, biological and clinical evidence. Avoid build/clinical claims, passing-CI badges or endorsement logos without supporting assets. Each application needs its own intended decision and comparator.

## ADR-003: One source per substantive topic

Status: adopted. Navigation pages summarize and link; research/ retains canonical technical detail. Do not duplicate long protocols in multiple folders. Historical reviews retain their original dates and current-taxonomy caveats.

## Future decision record template

ID; date; status; context; alternatives; evidence; decision; consequences; owner; conditions for reconsideration. A repository choice is not a physical architecture validation.
