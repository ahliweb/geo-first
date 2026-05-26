# Issue 002: BIG metadata automation

## Goal
Generate Geoportal-ready metadata automatically from project inputs using a single script.

## Scope
- Produce ISO 19139 XML with BIG-compatible content.
- Include `gmd:metadataExtensionInfo`, `gmd:useLimitation`, lineage, source, and contact.
- Ensure UUID file identifiers.
- Allow project-level metadata generation from the CLI.

## Acceptance Criteria
- A metadata file can be generated from project path, title, abstract, extent, and source parameters.
- Generated XML validates as well-formed XML.
- The file includes license and use limitation text.
- The result is suitable for PALAPA/SIMPADU upload workflows.

## Notes
- This work stays within the AW Non-Commercial License 1.0.
- Commercial use requires separate written permission.
