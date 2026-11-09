# Selective openness and commercial boundaries

Adopted 6 November 2026. Maintainer: Sadhu Shobab Bollipo.

Endorys publishes selected research so others can inspect assumptions, reproduce software examples and review proposed experiments. Future commercial engineering is evaluated separately before release. This policy describes publication decisions; it does not replace file-specific licences.

## Existing permissions remain in force

The grants in [LICENSE.md](LICENSE.md), [the Acoustic Reference Test package policy](research/e001_LICENSE.md), and applicable file notices continue unchanged. Covered Apache-2.0 software and CC BY 4.0 documentation remain commercially reusable under their terms. No fee, noncommercial restriction, confidentiality condition or additional approval is imposed on that licensed reuse. Existing third-party terms remain applicable.

A future business agreement cannot promise exclusivity over rights already granted to others. This policy neither recalls public copies nor makes earlier disclosures confidential.

## What belongs in public research

- Reviewed protocols, assumptions, limitations and acceptance criteria.
- Explicitly licensed reproducibility tools, synthetic examples and reference interfaces.
- Evidence corrections, independent reviews and results approved for release, including negative findings and uncertainty.
- Clearly labelled concept illustrations, with separate asset permissions.

The immediate goal is **a reproducible acoustic phantom bench test: the Acoustic Reference Test (E001)**. Public synthetic output is not evidence of physical or clinical performance. Commercial considerations must not be used to misrepresent experimental outcomes.

## What requires separate review before publication

Potentially novel unpublished implementations, detailed hardware/CAD/manufacturing files, firmware, calibration methods, commercial product code, partner work and experimental datasets require ownership, disclosure and licensing review before release. Not all such material must remain private permanently; release is decided component by component.

Keep confidential work in a **separate private repository or appropriately controlled storage** with named access. A branch, issue, pull request, attachment or workflow artifact in a public repository is not a confidential workspace. Do not upload sensitive material first and rely on deletion later.

Do not publish employer information, partner correspondence, credentials, patient information or third-party designs without the necessary rights and authorization. Private storage is not by itself sufficient authorization for medical or personal data.

## Release boundaries by asset

| Asset | Publication approach | Permissions |
|---|---|---|
| Selected documentation and research protocols | Public after review | Existing CC BY 4.0 scope; retain attribution and limitations |
| Selected reproducibility software | Public after review | Existing Apache-2.0 scope; preserve notices |
| New hardware, firmware and commercial implementations | Private initially; component review before release | Explicit terms only after ownership review; existing dependencies keep their licences |
| Experimental datasets | Review each release separately | Record provenance, authority, metadata and explicit dataset terms |
| Partner material | Controlled access under agreed terms | No public release without authorization |
| Branding, generated visuals and third-party assets | Separate asset review | No blanket grant through the software or documentation licence |

These are publication defaults, not replacements for file-specific licences. A public repository can contain components with different permissions.

## Dataset release record

For each proposed dataset release, identify the source and evidence type (synthetic, non-biological physical, biological or clinical); collection authority and applicable consent or approvals; instrument configuration, calibration, units and processing; raw and derived files with hashes; excluded, rejected and invalid records with reasons; privacy and contractual restrictions; licence and provenance notices; limitations; and the approving maintainer, date and immutable version. No physical or clinical dataset is licensed by this checklist alone.

## Publication checklist

Before releasing a new component or dataset, record:

1. Files, version, purpose and evidence level: proposed, synthetic, physically measured, biological or clinical.
2. Author, provenance, dependencies and authority to publish and license the material.
3. Confidentiality, privacy, contractual and potentially patent-relevant disclosure checks; obtain specialist advice where needed before disclosure.
4. The intended licence and exclusions, consistent with existing grants; do not silently relicense contributed or third-party work.
5. Reproduction instructions, verification, limitations and any required consent or dataset permissions.
6. Maintainer approval, date and the release/commit identifier in the change record.

Hold release while a required rights or confidentiality question remains unresolved. This checklist does not establish patentability, freedom to operate, regulatory compliance or clinical safety.

## Contributions

Public contributions remain under the applicable existing component terms. No copyright assignment, exclusive commercial right or contributor agreement is created by submitting a contribution. Any different arrangement must be separately agreed before work begins; contributors retain their rights except for permissions they actually grant.

Discuss scope without revealing confidential implementation details. For a private collaboration enquiry, first email a non-confidential description to [sadhu.shobab@gmail.com](mailto:sadhu.shobab@gmail.com). Email contact does not itself create an NDA; agree confidentiality and access before sharing sensitive material.

## Commercial development

Endorys operates as an independent research and technology venture with selectively open documentation and reproducibility tools. The intended business model is paid R&D and potential commercial licensing of separately developed, rights-cleared technology. This is a development direction, not evidence of an available proprietary product or an incorporated company.

Potential future activities include paid engineering, integration, support and separately licensed new components. No paid offering, validated device, licence revenue or partnership is established by this document. Reuse allowed by existing public licences does not require buying a commercial agreement. Endorys branding and third-party rights remain separate.

Research contributions and commercial work should have clear scopes, ownership, access, deliverables and payment terms before work begins. Public documentation is not an offer of an exclusive licence.

## Website and hosting

The website is an informational research showcase. Its source, text, images and third-party assets require their own permissions; the platform licence does not automatically cover a separate repository. GitHub Pages is not the planned host for paid SaaS, commercial transactions, patient data or sensitive account workflows. Review hosting terms and choose suitable infrastructure before introducing those functions.

References: [GitHub licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository), [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits), [WIPO patent guidance](https://www.wipo.int/en/web/patents/faq_patents).

This original policy document is licensed CC BY 4.0 under the existing documentation scope. It does not expand the licence of any excluded asset.
