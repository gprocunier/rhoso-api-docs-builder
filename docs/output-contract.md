# Output Contract

The repository artifact root is `validation/`.

```text
validation/
  <rhoso-version>/
    index.md
    manifest.json
    supported-services.json
    apis/
      <friendly-service-project>/
        index.md
        metadata.json
```

The GitHub Pages artifact root is `site/`.

```text
site/
  index.html
  styles.css
  validation/
    <rhoso-version>/
      index.html
      apis/
        <friendly-service-project>/
          index.html
```

## Manifest Requirements

`manifest.json` includes:

- release mapping
- catalog snapshot date
- source citations
- all supported RHOSO services
- matched supported API references
- unmatched RHOSO-supported services
- upstream APIs excluded because RHOSO support data does not select them
- semantic, GitHub tree, and GitHub Pages URIs for every supported API
